import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def carregarBanco():
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
