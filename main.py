from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import requests  # Biblioteca para fazer a requisição HTTP para o ORDS

app = FastAPI()

# URL que você gerou ativando o REST na tabela ng_cidade
ORDS_URL = "https://geae26552a5af32-dbng.adb.sa-vinhedo-1.oraclecloudapps.com/ords/teste/ng_cidade/"

@app.get("/")
def home():
    return {
        "mensagem": "Hello World da API Python",
        "status": "online",
        "origem": "aaaaaaaaaaaaaaaaaa"
    }

# --- NOVA ROTA PARA TESTAR A CONEXÃO COM O APEX/ORDS ---
@app.get("/cidades")
def listar_cidades():
    try:
        # O Python faz uma requisição GET segura (HTTPS) para a nuvem da Oracle
        resposta = requests.get(ORDS_URL, timeout=10)
        
        # Se a Oracle retornar algum erro (ex: 404, 500), o Python captura aqui
        resposta.raise_for_status()
        
        # Converte o resultado JSON vindo do banco de dados
        dados_oracle = resposta.json()
        
        # O ORDS joga as linhas da tabela sempre dentro de uma chave chamada 'items'
        linhas_da_tabela = dados_oracle.get("items", [])
        
        return {
            "status": "sucesso",
            "origem": "Oracle Cloud (ORDS)",
            "total_registros": len(linhas_da_tabela),
            "dados": linhas_da_tabela
        }
        
    except requests.exceptions.RequestException as e:
        # Se der erro de rede, timeout ou permissão, retorna o motivo para você debugar
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao conectar no Oracle APEX/ORDS: {str(e)}"
        )

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