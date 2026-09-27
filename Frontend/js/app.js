const COLUNAS = ["nome", "genero", "anoLancamento", "diretor", "nota", "avaliacao"];
const STORAGE_KEY = "movietracker_base_url";
const DEFAULT_BASE_URL = "http://127.0.0.1:8000";

// Mensagens de texto que o backend devolve com status 200 mesmo quando a
// operação falhou (ele não usa HTTPException para essas regras de negócio).
const MENSAGENS_FALHA = new Set([
  "Insira uma nota válida",
  "Insira um nome válido!",
  "Filme não encontrado!",
  "Insira uma coluna válida para edição!",
]);

let currentMovies = [];
let movieBeingEdited = null; // nome do filme alvo dos modais de avaliar/editar/excluir

/* ---------------------------- Utilidades DOM ---------------------------- */

const $ = (id) => document.getElementById(id);

function getBaseUrl() {
  return (localStorage.getItem(STORAGE_KEY) || DEFAULT_BASE_URL).replace(/\/+$/, "");
}

function setBaseUrl(url) {
  localStorage.setItem(STORAGE_KEY, url.replace(/\/+$/, ""));
}

function showToast(message, type = "info") {
  const stack = $("toastStack");
  const toast = document.createElement("div");
  toast.className = `toast${type === "error" ? " toast--error" : type === "success" ? " toast--success" : ""}`;
  toast.textContent = message;
  stack.appendChild(toast);
  setTimeout(() => toast.remove(), 4200);
}

function openModal(id) {
  $(id).hidden = false;
}
function closeModal(id) {
  $(id).hidden = true;
}
document.querySelectorAll("[data-close]").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const overlay = e.target.closest(".modal-overlay");
    if (overlay) overlay.hidden = true;
  });
});
document.querySelectorAll(".modal-overlay").forEach((overlay) => {
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) overlay.hidden = true;
  });
});

function setFieldError(id, message) {
  const el = $(id);
  if (!message) {
    el.hidden = true;
    el.textContent = "";
  } else {
    el.hidden = false;
    el.textContent = message;
  }
}

/* ------------------------------ Chamadas API ----------------------------- */

async function apiFetch(path, options = {}) {
  const url = `${getBaseUrl()}${path}`;
  let response;
  try {
    response = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (erro) {
    throw new ApiError(
      "Não foi possível conectar à API. Verifique se o backend está rodando e se o endereço em ⚙ API está correto, ou se essa ação já foi realizada.",
      0
    );
  }

  let corpo = null;
  try {
    corpo = await response.json();
  } catch (_) {
    /* resposta sem corpo JSON */
  }

  if (response.status === 422) {
    const detalhes = (corpo && corpo.detail) || [];
    const texto = Array.isArray(detalhes)
      ? detalhes.map((d) => d.msg).join(" · ")
      : "Dados inválidos enviados para a API.";
    throw new ApiError(texto || "Dados inválidos.", 422);
  }

  if (response.status >= 500) {
    throw new ApiError(
      "A API retornou um erro interno ao processar esta ação (ver observação sobre o endpoint /editarFilme no README).",
      response.status
    );
  }

  if (!response.ok) {
    throw new ApiError(
      (corpo && (corpo.detail || corpo.message)) || `A API retornou um erro (status ${response.status}).`,
      response.status
    );
  }

  return corpo;
}

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

/* -------------------------- Verificação de status ------------------------ */

async function checkConnection() {
  const status = $("connectionStatus");
  status.dataset.state = "checking";
  status.querySelector(".status__label").textContent = "verificando API…";
  try {
    const res = await fetch(`${getBaseUrl()}/`, { method: "GET" });
    if (res.ok) {
      status.dataset.state = "online";
      status.querySelector(".status__label").textContent = "API conectada";
      return true;
    }
    throw new Error("offline");
  } catch (_) {
    status.dataset.state = "offline";
    status.querySelector(".status__label").textContent = "API offline";
    return false;
  }
}

/* --------------------------------- Filmes -------------------------------- */

function mapTuplaParaFilme(tupla) {
  const filme = {};
  COLUNAS.forEach((coluna, i) => (filme[coluna] = tupla[i]));
  return filme;
}

function buildFiltroQuery() {
  const params = new URLSearchParams();
  const nome = $("fNome").value.trim();
  const genero = $("fGenero").value.trim();
  const diretor = $("fDiretor").value.trim();
  const ano = $("fAno").value.trim();
  const notaMinima = $("fNotaMin").value.trim();
  const notaMaxima = $("fNotaMax").value.trim();

  if (nome) params.set("nome", nome);
  if (genero) params.set("genero", genero);
  if (diretor) params.set("diretor", diretor);
  if (ano) params.set("anoLancamento", ano);
  if (notaMinima) params.set("notaMinima", notaMinima);
  if (notaMaxima) params.set("notaMaxima", notaMaxima);

  return params;
}

async function carregarFilmes() {
  $("loadingState").hidden = false;
  $("emptyState").hidden = true;
  $("movieGrid").innerHTML = "";

  try {
    const query = buildFiltroQuery();
    const qs = query.toString();
    const dados = await apiFetch(`/verFilmes${qs ? `?${qs}` : ""}`);
    currentMovies = Array.isArray(dados) ? dados.map(mapTuplaParaFilme) : [];
    renderizarFilmes();
  } catch (erro) {
    showToast(erro.message, "error");
    currentMovies = [];
    renderizarFilmes();
  } finally {
    $("loadingState").hidden = true;
  }
}

function renderizarFilmes() {
  const grid = $("movieGrid");
  const empty = $("emptyState");
  grid.innerHTML = "";

  $("resultCount").textContent =
    currentMovies.length === 1 ? "1 filme encontrado" : `${currentMovies.length} filmes encontrados`;

  if (currentMovies.length === 0) {
    empty.hidden = false;
    return;
  }
  empty.hidden = true;

  const frag = document.createDocumentFragment();
  currentMovies.forEach((filme) => frag.appendChild(criarCardFilme(filme)));
  grid.appendChild(frag);
}

function criarCardFilme(filme) {
  const card = document.createElement("article");
  card.className = "card";

  const temNota = filme.nota !== null && filme.nota !== undefined;

  card.innerHTML = `
    <div class="card__edge"></div>
    <div class="card__body">
      <div class="card__top">
        <h3 class="card__title">${escapeHtml(filme.nome)}</h3>
        <div class="badge-score ${temNota ? "" : "badge-score--empty"}">${temNota ? filme.nota : "—"}</div>
      </div>
      <div class="card__meta">
        <span>🎬 <strong>${escapeHtml(filme.genero)}</strong></span>
        <span>📅 <strong>${escapeHtml(String(filme.anoLancamento))}</strong></span>
        <span>🎥 <strong>${escapeHtml(filme.diretor)}</strong></span>
      </div>
      ${filme.avaliacao ? `<p class="card__review">“${escapeHtml(filme.avaliacao)}”</p>` : ""}
    </div>
    <div class="card__actions">
      <button class="btn btn--outline" data-action="rate">Avaliar</button>
      <button class="btn btn--ghost" data-action="edit">Editar</button>
      <button class="btn btn--ghost" data-action="delete">Excluir</button>
    </div>
  `;

  card.querySelector('[data-action="rate"]').addEventListener("click", () => abrirModalAvaliar(filme));
  card.querySelector('[data-action="edit"]').addEventListener("click", () => abrirModalEditar(filme));
  card.querySelector('[data-action="delete"]').addEventListener("click", () => abrirModalExcluir(filme));

  return card;
}

function escapeHtml(valor) {
  const div = document.createElement("div");
  div.textContent = valor ?? "";
  return div.innerHTML;
}

/* ------------------------------ Adicionar filme --------------------------- */

$("btnAddMovie").addEventListener("click", () => {
  $("formMovie").reset();
  setFieldError("movieFormError", "");
  $("modalMovieTitle").textContent = "Adicionar filme";
  openModal("modalMovie");
});

$("formMovie").addEventListener("submit", async (e) => {
  e.preventDefault();
  setFieldError("movieFormError", "");

  const nome = $("mNome").value.trim();
  const genero = $("mGenero").value.trim();
  const anoLancamento = Number($("mAno").value);
  const diretor = $("mDiretor").value.trim();

  if (!nome || !genero || !diretor) {
    setFieldError("movieFormError", "Preencha todos os campos.");
    return;
  }
  if (anoLancamento < 1895 || anoLancamento > 2999) {
    setFieldError("movieFormError", "O ano de lançamento deve estar entre 1895 e 2999.");
    return;
  }

  const btn = $("btnSubmitMovie");
  btn.disabled = true;
  try {
    const resultado = await apiFetch("/adicionarFilme", {
      method: "POST",
      body: JSON.stringify({ nome, genero, anoLancamento, diretor }),
    });
    if (typeof resultado === "string" && MENSAGENS_FALHA.has(resultado)) {
      setFieldError("movieFormError", resultado);
      return;
    }
    showToast(typeof resultado === "string" ? resultado : "Filme adicionado!", "success");
    closeModal("modalMovie");
    carregarFilmes();
  } catch (erro) {
    setFieldError("movieFormError", erro.message);
  } finally {
    btn.disabled = false;
  }
});

/* -------------------------------- Avaliar --------------------------------- */

function abrirModalAvaliar(filme) {
  movieBeingEdited = filme.nome;
  $("modalRateTitle").textContent = `Avaliar "${filme.nome}"`;
  $("rNota").value = filme.nota ?? 5;
  $("rNotaValue").textContent = filme.nota ?? 5;
  $("rAvaliacao").value = filme.avaliacao ?? "";
  setFieldError("rateFormError", "");
  openModal("modalRate");
}

$("rNota").addEventListener("input", (e) => {
  $("rNotaValue").textContent = e.target.value;
});

$("formRate").addEventListener("submit", async (e) => {
  e.preventDefault();
  setFieldError("rateFormError", "");

  const nota = Number($("rNota").value);
  const avaliacao = $("rAvaliacao").value.trim();
  if (!avaliacao) {
    setFieldError("rateFormError", "Escreva sua avaliação.");
    return;
  }

  try {
    const resultado = await apiFetch("/avaliarFilme", {
      method: "PUT",
      body: JSON.stringify({ nomeFilme: movieBeingEdited, avaliacao, nota }),
    });
    if (typeof resultado === "string" && MENSAGENS_FALHA.has(resultado)) {
      setFieldError("rateFormError", resultado);
      return;
    }
    showToast(typeof resultado === "string" ? resultado : "Avaliação salva!", "success");
    closeModal("modalRate");
    carregarFilmes();
  } catch (erro) {
    setFieldError("rateFormError", erro.message);
  }
});

/* --------------------------------- Editar ---------------------------------- */

function abrirModalEditar(filme) {
  movieBeingEdited = filme.nome;
  $("modalEditTitle").textContent = `Editar "${filme.nome}"`;
  $("eColuna").value = "nome";
  $("eValor").value = "";
  setFieldError("editFormError", "");
  openModal("modalEdit");
}

$("formEdit").addEventListener("submit", async (e) => {
  e.preventDefault();
  setFieldError("editFormError", "");

  const colunaFilme = $("eColuna").value;
  const valorNovo = $("eValor").value.trim();
  if (!valorNovo) {
    setFieldError("editFormError", "Informe o novo valor.");
    return;
  }
  if (colunaFilme === "anoLancamento" && !/^\d{1,4}$/.test(valorNovo)) {
    setFieldError("editFormError", "Informe um ano válido (apenas números).");
    return;
  }

  try {
    const resultado = await apiFetch("/editarFilme", {
      method: "PUT",
      body: JSON.stringify({ nomeFilme: movieBeingEdited, colunaFilme, valorNovo }),
    });
    if (typeof resultado === "string" && MENSAGENS_FALHA.has(resultado)) {
      setFieldError("editFormError", resultado);
      return;
    }
    showToast(typeof resultado === "string" ? resultado : "Filme editado!", "success");
    closeModal("modalEdit");
    carregarFilmes();
  } catch (erro) {
    setFieldError("editFormError", erro.message);
  }
});

/* --------------------------------- Excluir ---------------------------------- */

function abrirModalExcluir(filme) {
  movieBeingEdited = filme.nome;
  $("deleteConfirmText").textContent = `Tem certeza que deseja excluir "${filme.nome}" do seu catálogo? Essa ação não pode ser desfeita.`;
  setFieldError("deleteFormError", "");
  openModal("modalDelete");
}

$("btnConfirmDelete").addEventListener("click", async () => {
  setFieldError("deleteFormError", "");
  try {
    const resultado = await apiFetch("/excluirFilme", {
      method: "PUT",
      body: JSON.stringify({ nomeFilme: movieBeingEdited }),
    });
    if (typeof resultado === "string" && MENSAGENS_FALHA.has(resultado)) {
      setFieldError("deleteFormError", resultado);
      return;
    }
    showToast(typeof resultado === "string" ? resultado : "Filme excluído.", "success");
    closeModal("modalDelete");
    carregarFilmes();
  } catch (erro) {
    setFieldError("deleteFormError", erro.message);
  }
});

/* --------------------------------- Filtros ---------------------------------- */

$("btnFilter").addEventListener("click", carregarFilmes);
$("btnClearFilter").addEventListener("click", () => {
  ["fNome", "fGenero", "fDiretor", "fAno", "fNotaMin", "fNotaMax"].forEach((id) => ($(id).value = ""));
  carregarFilmes();
});
["fNome", "fGenero", "fDiretor", "fAno", "fNotaMin", "fNotaMax"].forEach((id) => {
  $(id).addEventListener("keydown", (e) => {
    if (e.key === "Enter") carregarFilmes();
  });
});

/* ------------------------------ Popular exemplo ------------------------------ */

$("btnSeed").addEventListener("click", async () => {
  const btn = $("btnSeed");
  btn.disabled = true;
  try {
    const resultado = await apiFetch("/testarFilmes", { method: "POST" });
    showToast(typeof resultado === "string" ? resultado : "Filmes de exemplo adicionados!", "success");
    carregarFilmes();
  } catch (erro) {
    showToast(erro.message, "error");
  } finally {
    btn.disabled = false;
  }
});

/* -------------------------------- Configurações -------------------------------- */

$("btnSettings").addEventListener("click", () => {
  $("sBaseUrl").value = getBaseUrl();
  openModal("modalSettings");
});

$("formSettings").addEventListener("submit", async (e) => {
  e.preventDefault();
  const valor = $("sBaseUrl").value.trim() || DEFAULT_BASE_URL;
  setBaseUrl(valor);
  closeModal("modalSettings");
  await checkConnection();
  carregarFilmes();
});

/* ----------------------------------- Início ------------------------------------ */

(async function iniciar() {
  await checkConnection();
  carregarFilmes();
})();
