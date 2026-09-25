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