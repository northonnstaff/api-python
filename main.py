from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


@app.get("/")
def home():
    return {
        "mensagem": "Hello World da API Python",
        "status": "online",
        "origem": "aaaaaaaaaaaaaaaaaa"
    }


@app.get("/hello")
def hello(nome: str = "Oracle APEX"):
    return {
        "mensagem": f"Olá, {nome}!",
        "data_hora": datetime.now().isoformat()
    }


class MensagemRequest(BaseModel):
    nome: str


@app.post("/hello")
def hello_post(request: MensagemRequest):
    return {
        "mensagem": f"Olá, {request.nome}! Recebido via POST.",
        "status": "sucesso"
    }
