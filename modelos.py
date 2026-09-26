from pydantic import BaseModel, Field

class adicionarFilme(BaseModel):
    nome : str = Field(min_length=1, max_length=1000)
    genero : str = Field(min_length=1, max_length=200)
    anoLancamento : int = Field(ge=1895, le=2999, ) #1895 porque o primeiro filme do mundo foi em 1895
    diretor : str = Field(min_length=1, max_length=250)

class filmeAvaliar(BaseModel):
    nomeFilme : str = Field(min_length=1, max_length=1000)
    avaliacao : str = Field(min_length=1, max_length=3000)
    nota : int = Field(ge=0, le=10)