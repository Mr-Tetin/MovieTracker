from fastapi import FastAPI, HTTPException
from banco import conectarBanco, criarBanco, testarfilmes


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
def verFilmes():
    conexao = conectarBanco()
    cursor = conexao.cursor()

    sqlInserir = "SELECT * FROM Filmes"

    #Executa o sql e pega os dados
    cursor.execute(sqlInserir)
    filmes = cursor.fetchall()

    conexao.close()

    return filmes

@app.post("/adicionarFilme")
def adicionarFilmes(nome: str, anoLancamento: int, diretor: str, nota: int):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    #cria uma variável a parte para inserção dos valores para facilitar
    sqlInserir = "INSERT INTO Filmes (Nome, AnoLancamento, Diretor, Nota) VALUES (%s, %s, %s, %s)"

    #insere os dados
    cursor.execute(sqlInserir, (nome,anoLancamento, diretor,nota))

    conexao.commit()

    conexao.close()

@app.post("/testarfilmes")
def testefilmes():
    filmes = [
        ("Interestelar", 2014, "Christopher Nolan", 10),
        ("O Poderoso Chefão", 1972, "Francis Ford Coppola", 10),
        ("Clube da Luta", 1999, "David Fincher", 9),
        ("Matrix", 1999, "Lana Wachowski e Lilly Wachowski", 9),
        ("Pulp Fiction", 1994, "Quentin Tarantino", 9),
        ("O Senhor dos Anéis: A Sociedade do Anel", 2001, "Peter Jackson", 10),
        ("O Senhor dos Anéis: As Duas Torres", 2002, "Peter Jackson", 9),
        ("O Senhor dos Anéis: O Retorno do Rei", 2003, "Peter Jackson", 10),
        ("Batman: O Cavaleiro das Trevas", 2008, "Christopher Nolan", 10),
        ("Forrest Gump", 1994, "Robert Zemeckis", 9),
        ("Clube dos Cinco", 1985, "John Hughes", 8),
        ("Gladiador", 2000, "Ridley Scott", 9),
        ("O Silêncio dos Inocentes", 1991, "Jonathan Demme", 9),
        ("Parasita", 2019, "Bong Joon-ho", 10),
        ("Whiplash", 2014, "Damien Chazelle", 9),
        ("Django Livre", 2012, "Quentin Tarantino", 9),
        ("Vingadores: Ultimato", 2019, "Anthony Russo e Joe Russo", 8),
        ("Homem-Aranha 2", 2004, "Sam Raimi", 9),
        ("O Iluminado", 1980, "Stanley Kubrick", 9),
        ("De Volta para o Futuro", 1985, "Robert Zemeckis", 9)
    ]

    for filmes in filmes:
        testarfilmes(filmes)