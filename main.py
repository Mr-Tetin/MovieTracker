from fastapi import FastAPI, HTTPException
from banco import criarBanco, testarfilmes, adicionarFilmes, verFilmes, avaliarFilme


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
def chamarVerFilme(nome : str | None = None, genero: str | None = None, anoLancamento : int | None = None, diretor : str | None = None, nota : int | None = None):
    return verFilmes(nome, genero, anoLancamento, diretor, nota)

@app.post("/adicionarFilme")
def chamarAdicionarFilmes(nome: str, genero: str, anoLancamento: int, diretor: str, nota: int):
    return adicionarFilmes(nome, genero, anoLancamento, diretor, nota)

@app.post("/testarfilmes")
def chamarTestefilmes():
    return testarfilmes()

@app.put("/avaliarFilme")
def chamarAvaliarFilme(nomeFilme, avaliacao, nota):
    return avaliarFilme(nomeFilme, avaliacao, nota)