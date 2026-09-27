from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.Banco.banco import criarBanco, gerarfilmesBanco, adicionarFilmesBanco, verFilmesBanco, avaliarFilmeBanco, editarFilmeBanco, excluirFilmeBanco
from Backend.Modelos.modelos import adicionarFilmeModelo, avaliarFilmeModelo, editarFilmeModelo, excluirFilmeModelo


#cria o app(Inicia a API)
app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#cria o banco
criarBanco()


#Rota da página incial
@app.get("/")
def paginaInicial():
    
    return "MovieTracker"

#Rota para ver os filmes existentes
@app.get("/verFilmes")
def chamarVerFilme(nome: str | None = None,
    genero: str | None = None,
    anoLancamento: int | None = None,
    diretor: str | None = None,
    nota: int | None = None):

    return verFilmesBanco(nome, genero, anoLancamento, diretor, nota)

@app.post("/adicionarFilme")
def chamarAdicionarFilmes(filme : adicionarFilmeModelo):
    return adicionarFilmesBanco(filme.nome, filme.genero, filme.anoLancamento, filme.diretor)

@app.post("/testarfilmes")
def chamarTestefilmes():
    return gerarfilmesBanco()

@app.put("/avaliarFilme")
def chamarAvaliarFilme(filme : avaliarFilmeModelo):
    return avaliarFilmeBanco(filme.nomeFilme, filme.avaliacao, filme.nota)

@app.put("/editarFilme")
def chamarEditarFilme(filme : editarFilmeModelo):
    return editarFilmeBanco(filme.nomeFilme, filme.colunaFilme, filme.valorNovo)

@app.put("/excluirFilme")
def chamarExcluirFilme(filme : excluirFilmeModelo):
    return excluirFilmeBanco(filme.nomeFilme)