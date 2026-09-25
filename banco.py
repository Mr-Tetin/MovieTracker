import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def conectarBanco():
    try:
        conexao = psycopg.connect(
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD")
        )
        return conexao
    except Exception as erro:
        print(f"Erro ao conectar no banco.\n\nErro: {erro}")
        raise erro


def criarBanco():
    conexao = conectarBanco()
    cursor = conexao.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Filmes (
            Nome VARCHAR NOT NULL PRIMARY KEY,
            AnoLancamento INTEGER CHECK (AnoLancamento >= 0 AND AnoLancamento <= 9999),
            Diretor VARCHAR NOT NULL,
            Nota INTEGER CHECK (Nota >= 0 AND Nota <= 10)
            )
        """)
    
    #confirma que a alteração foi feita
    conexao.commit()


    #fecha a conexao
    conexao.close()



#TIRAR DEPOIS
def testarfilmes(tupla):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    #cria uma variável a parte para inserção dos valores para facilitar
    sqlInserir = "INSERT INTO Filmes (Nome, AnoLancamento, Diretor, Nota) VALUES (%s, %s, %s, %s)"
    
    #insere os dados
    cursor.execute(sqlInserir, (tupla[0],tupla[1], tupla[2],tupla[3]))

    #confirma que a alteração foi feita
    conexao.commit()

    #fecha a conexao
    conexao.close()