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
def verFilmes(nome : str | None = None, genero: str | None = None, anoLancamento : int | None = None, diretor : str | None = None, nota : int | None = None,):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    sqlConsulta = "SELECT * FROM Filmes"
    
    #onde as condições vão ficar
    condicao = []
    #os valores dos argumentos
    valores = []
    
    if (nome):
        condicao.append("nome = %s")
        valores.append(nome)
    if(genero):
         condicao.append("genero = %s")
         valores.append(genero)
    if (anoLancamento is not None):
        condicao.append("anoLancamento >= %s")
        valores.append(anoLancamento)
    if (diretor):
            condicao.append("diretor = %s")
            valores.append(diretor)
    if (nota is not None):
            condicao.append("nota >= %s")
            valores.append(nota)

    if(condicao):
        sqlConsulta += " WHERE " + " AND ".join(condicao)

    cursor.execute(sqlConsulta, valores)
    filmes = cursor.fetchall()
    conexao.close()

    return filmes
    

@app.post("/adicionarFilme")
def adicionarFilmes(nome: str, genero: str, anoLancamento: int, diretor: str, nota: int):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    #cria uma variável a parte para inserção dos valores para facilitar
    sqlInserir = "INSERT INTO Filmes (Nome, Genero, AnoLancamento, Diretor, Nota) VALUES (%s, %s, %s, %s, %s)"

    #insere os dados
    cursor.execute(sqlInserir, (nome, genero, anoLancamento, diretor,nota))

    conexao.commit()

    conexao.close()

@app.post("/testarfilmes")
def testefilmes():
    filmes = [
        ("Interestelar", "Ficção científica", 2014, "Christopher Nolan", 10),
        ("O Poderoso Chefão", "Crime", 1972, "Francis Ford Coppola", 10),
        ("Clube da Luta", "Drama", 1999, "David Fincher", 9),
        ("Matrix", "Ficção científica", 1999, "Lana Wachowski e Lilly Wachowski", 9),
        ("Pulp Fiction", "Crime", 1994, "Quentin Tarantino", 9),
        ("O Senhor dos Anéis: A Sociedade do Anel", "Fantasia", 2001, "Peter Jackson", 10),
        ("O Senhor dos Anéis: As Duas Torres", "Fantasia", 2002, "Peter Jackson", 9),
        ("O Senhor dos Anéis: O Retorno do Rei", "Fantasia", 2003, "Peter Jackson", 10),
        ("Batman: O Cavaleiro das Trevas", "Ação", 2008, "Christopher Nolan", 10),
        ("Forrest Gump", "Drama", 1994, "Robert Zemeckis", 9),
        ("Clube dos Cinco", "Comédia", 1985, "John Hughes", 8),
        ("Gladiador", "Ação", 2000, "Ridley Scott", 9),
        ("O Silêncio dos Inocentes", "Terror", 1991, "Jonathan Demme", 9),
        ("Parasita", "Drama", 2019, "Bong Joon-ho", 10),
        ("Whiplash", "Drama", 2014, "Damien Chazelle", 9),
        ("Django Livre", "Faroeste", 2012, "Quentin Tarantino", 9),
        ("Vingadores: Ultimato", "Ação", 2019, "Anthony Russo e Joe Russo", 8),
        ("Homem-Aranha 2", "Ação", 2004, "Sam Raimi", 9),
        ("O Iluminado", "Terror", 1980, "Stanley Kubrick", 9),
        ("De Volta para o Futuro", "Ficção científica", 1985, "Robert Zemeckis", 9),
        ("Titanic", "Romance", 1997, "James Cameron", 9),
        ("Oppenheimer", "Drama", 2023, "Christopher Nolan", 10),
        ("A Origem", "Ficção científica", 2010, "Christopher Nolan", 10),
        ("Os Infiltrados", "Crime", 2006, "Martin Scorsese", 9),
        ("Ilha do Medo", "Suspense", 2010, "Martin Scorsese", 9),
        ("Coringa", "Drama", 2019, "Todd Phillips", 9),
        ("Toy Story", "Animação", 1995, "John Lasseter", 9),
        ("Shrek", "Animação", 2001, "Andrew Adamson e Vicky Jenson", 9),
        ("O Rei Leão", "Animação", 1994, "Roger Allers e Rob Minkoff", 9),
        ("Homens de Preto", "Ficção científica", 1997, "Barry Sonnenfeld", 8),
        ("Jurassic Park", "Ficção científica", 1993, "Steven Spielberg", 9),
        ("Tubarão", "Terror", 1975, "Steven Spielberg", 9),
        ("O Exorcista", "Terror", 1973, "William Friedkin", 9),
        ("Psicose", "Terror", 1960, "Alfred Hitchcock", 10),
        ("Janela Indiscreta", "Suspense", 1954, "Alfred Hitchcock", 9),
        ("À Espera de um Milagre", "Drama", 1999, "Frank Darabont", 9),
        ("Um Sonho de Liberdade", "Drama", 1994, "Frank Darabont", 10),
        ("O Resgate do Soldado Ryan", "Guerra", 1998, "Steven Spielberg", 9),
        ("Até o Último Homem", "Guerra", 2016, "Mel Gibson", 9),
        ("Top Gun: Maverick", "Ação", 2022, "Joseph Kosinski", 9),
        ("Mad Max: Estrada da Fúria", "Ação", 2015, "George Miller", 9),
        ("John Wick", "Ação", 2014, "Chad Stahelski", 8),
        ("Guardiões da Galáxia", "Ação", 2014, "James Gunn", 9),
        ("Homem de Ferro", "Ação", 2008, "Jon Favreau", 8),
        ("Pantera Negra", "Ação", 2018, "Ryan Coogler", 8),
        ("O Lobo de Wall Street", "Comédia", 2013, "Martin Scorsese", 9),
        ("O Grande Truque", "Drama", 2006, "Christopher Nolan", 9),
        ("Memento", "Suspense", 2000, "Christopher Nolan", 9),
        ("Cisne Negro", "Drama", 2010, "Darren Aronofsky", 9),
        ("Her", "Romance", 2013, "Spike Jonze", 9)
    ]

    for filmes in filmes:
        testarfilmes(filmes)

    return "Filmes Adicionados!"