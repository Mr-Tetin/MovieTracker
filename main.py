from fastapi import FastAPI, HTTPException
from banco import conectarBanco


app = FastAPI()



#Rota da página incial
@app.get("/")
def paginaInicial():
    
    return "MovieTracker"



#Rota para ver os filmes existentes
@app.get("/Filmes")
def verFilmes():
    conexao = conectarBanco()
    return "Banco conectado com sucesso"



@app.post("/adicionarFilme")
def adicionarFilmes(nome: str, anoLancamento: int, diretor: str, nota: int):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    #cria uma variável a parte para inserção dos valores para facilitar
    sqlInserir = "INSERT INTO Filmes (Nome, AnoLancamento, Diretor, Nota) VALUES (%s, %s, %s, %s)"

    #insere os dados
    cursor.execute(sqlInserir, (nome,anoLancamento, diretor,nota))

    conexao.commit()