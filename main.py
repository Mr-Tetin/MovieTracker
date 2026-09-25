from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def paginaInicial():
    return "MovieTracker"