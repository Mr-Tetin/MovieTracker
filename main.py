from fastapi import FastAPI

app = FastAPI()

#Rota da página incial
@app.get("/")
def paginaInicial():
    return "MovieTracker"

#Rota para ver os filmes existentes
@app.get("/filmes")
def verFilmes():
    ...

@app.post("/adicionarFilme")
def adicionarFilmes():
    ...