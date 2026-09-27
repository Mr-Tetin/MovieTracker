<div align="center">

# 🎬 MovieTracker

**Seu catálogo pessoal de filmes — cadastre, avalie, edite e acompanhe tudo o que já assistiu.**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

</div>

---

## 📖 Sobre o projeto

**MovieTracker** é uma aplicação full-stack para organizar seu catálogo pessoal de filmes: adicionar, avaliar com nota e comentário, editar campos e excluir registros, além de filtrar por nome, gênero, diretor, ano e faixa de nota.

O **back-end** é uma API REST construída com **FastAPI** e **PostgreSQL**, e o **front-end** é uma interface web em **HTML, CSS e JavaScript puro**, com identidade visual preto e laranja.

> 🛠️ **Autoria:** o back-end (API, regras de negócio, modelagem e banco de dados) foi desenvolvido integralmente por mim. O front-end foi construído com o auxílio de IA (Claude), a partir dos endpoints que eu já tinha pronto.

---

## ✨ Funcionalidades

| Ação | Descrição |
|---|---|
| 🎞️ **Listar filmes** | Busca com filtros por nome, gênero, diretor, ano (a partir de) e faixa de nota (mínima/máxima) |
| ➕ **Adicionar filme** | Cadastra nome, gênero, ano de lançamento e diretor |
| ⭐ **Avaliar filme** | Define nota (0–10) e escreve uma avaliação em texto |
| ✏️ **Editar filme** | Atualiza um campo específico (nome, gênero, ano ou diretor) |
| 🗑️ **Excluir filme** | Remove um filme do catálogo, com confirmação |
| 🌱 **Popular exemplos** | Preenche o catálogo com ~50 filmes de exemplo para testes rápidos |

---

## 🧰 Tecnologias utilizadas

### Back-end
- **[Python 3.11](https://www.python.org/)**
- **[FastAPI](https://fastapi.tiangolo.com/)** — framework da API REST
- **[Uvicorn](https://www.uvicorn.org/)** — servidor ASGI
- **[Pydantic](https://docs.pydantic.dev/)** — validação dos dados de entrada
- **[PostgreSQL](https://www.postgresql.org/)** — banco de dados relacional
- **[Psycopg 3](https://www.psycopg.org/psycopg3/)** — driver de conexão com o Postgres
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — variáveis de ambiente

### Front-end
- **HTML5** semântico
- **CSS3** puro (Grid, Flexbox, variáveis CSS, responsivo)
- **JavaScript** puro (ES6+), sem frameworks — consumindo a API via `fetch`

---

## 🗂️ Estrutura do projeto

```
MovieTracker/
├── main.py                      # Ponto de entrada da API (rotas FastAPI)
├── requirements.txt              # Dependências do back-end
├── .env                          # Variáveis de ambiente (não versionado)
│
├── Backend/
│   ├── Banco/
│   │   └── banco.py               # Conexão e queries no PostgreSQL
│   └── Modelos/
│       └── modelos.py             # Schemas Pydantic (validação)
│
└── Frontend/
    ├── index.html                 # Interface web
    ├── css/
    │   └── style.css              # Identidade visual (preto + laranja)
    ├── js/
    │   └── app.js                 # Consumo da API (fetch, filtros, modais)
    └── assets/
        └── favicon.svg            # Ícone da aba do navegador
```

---

## 🔌 Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Health check da API |
| `GET` | `/verFilmes` | Lista filmes, com filtros opcionais: `nome`, `genero`, `anoLancamento`, `diretor`, `notaMinima`, `notaMaxima` |
| `POST` | `/adicionarFilme` | Adiciona um filme (`nome`, `genero`, `anoLancamento`, `diretor`) |
| `POST` | `/testarfilmes` | Popula o banco com filmes de exemplo |
| `PUT` | `/avaliarFilme` | Avalia um filme (`nomeFilme`, `avaliacao`, `nota`) |
| `PUT` | `/editarFilme` | Edita um campo do filme (`nomeFilme`, `colunaFilme`, `valorNovo`) |
| `PUT` | `/excluirFilme` | Remove um filme (`nomeFilme`) |

---

## 🚀 Como rodar o projeto

### Pré-requisitos
- [Python 3.11+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/) instalado e rodando
- Um navegador (Chrome, Firefox, Edge...)

### 1. Clone o repositório

```bash
git clone https://github.com/Mr-Tetin/MovieTracker.git
cd MovieTracker
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Crie um banco no PostgreSQL (ex.: `movietracker`) e, na raiz do projeto, crie/edite o arquivo `.env` com os dados de conexão:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=movietracker
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

> A tabela `Filmes` é criada automaticamente na primeira execução da API — não precisa rodar nenhum script de criação manualmente.

### 5. Suba a API

```bash
uvicorn main:app --reload
```

A API vai subir em **http://127.0.0.1:8000**. Deixe esse terminal aberto.

### 6. Abra o front-end

Dê duplo clique em `Frontend/index.html` (ou abra pelo navegador). Não precisa de servidor nem instalação — é tudo estático.

No canto superior direito da página, o indicador de status deve mostrar **"API conectada"**. Se estiver diferente do padrão (`http://127.0.0.1:8000`), clique em **⚙ API** e ajuste o endereço.

### 7. (Opcional) Popular com filmes de exemplo

Clique em **"Popular com filmes de exemplo"** na interface para testar rapidamente com ~50 filmes já cadastrados no `banco.py`.

---

<div align="center">

Feito por **Raimundo Porto de Melo Neto (Neto)** ·
[GitHub](https://github.com/Mr-Tetin) ·
[LinkedIn](https://www.linkedin.com/in/raimundo-porto)

</div>
