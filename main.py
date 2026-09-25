from fastapi import FastAPI, HTTPException
from banco import carregarBanco


app = FastAPI()

#Rota da página incial
@app.get("/")
def paginaInicial():
    return "MovieTracker"

#Rota para ver os filmes existentes
@app.get("/filmes")
def verFilmes():
    conexao = carregarBanco()
    return "Banco conectado com sucesso"

@app.post("/adicionarFilme")
def adicionarFilmes():
    ...