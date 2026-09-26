from fastapi import FastAPI
from Banco.banco import criarBanco, gerarfilmes, adicionarFilmes, verFilmes, avaliarFilme
from Modelos.modelos import adicionarFilme, filmeAvaliar


#cria o app(Inicia a API)
app = FastAPI()

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

    return verFilmes(nome, genero, anoLancamento, diretor, nota)

@app.post("/adicionarFilme")
def chamarAdicionarFilmes(filme : adicionarFilme):
    return adicionarFilmes(filme.nome, filme.genero, filme.anoLancamento, filme.diretor)

@app.post("/testarfilmes")
def chamarTestefilmes():
    return gerarfilmes()

@app.put("/avaliarFilme")
def chamarAvaliarFilme(filme : filmeAvaliar):
    return avaliarFilme(filme.nomeFilme, filme.avaliacao, filme.nota)