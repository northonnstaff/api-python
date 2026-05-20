from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import requests
import os

# --- IMPORTANTE: Importar o driver nativo da Oracle ---
import oracledb 

app = FastAPI()

ORDS_URL = "https://geae26552a5af32-dbng.adb.sa-vinhedo-1.oraclecloudapps.com/ords/teste/ng_cidade/"

# Configurações para a conexão direta
DB_USER = "ADMIN"
DB_PASSWORD = "SuaSenhaSeguraAqui"  # Substitua pela senha real do seu banco DBNG

# String de conexão explícita baseada no seu banco DBNG em Vinhedo (Porta TCPS 1522)
DB_DSN = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCPS)(HOST=adb.sa-vinhedo-1.oraclecloudapps.com)(PORT=1522))(CONNECT_DATA=(SERVICE_NAME=dbng_low.adb.oraclecloud.com)))"


@app.get("/")
def home():
    return {"status": "online"}

@app.get("/cidades")
def listar_cidades():
    # Sua rota antiga via ORDS (continua funcionando)
    resposta = requests.get(ORDS_URL, timeout=10)
    return resposta.json()


# --- NOVA ROTA: TESTE DE CONEXÃO DIRETA (SQL) ---
@app.get("/conexao-direta")
def testar_conexao_direta():
    connection = None
    cursor = None
    try:
        # Iniciando o oracledb no modo THIN (True) -> Dispensa Wallet e Instant Client
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN,
            thin=True
        )
        
        cursor = connection.cursor()
        # Executa um comando SQL direto no banco de dados
        cursor.execute("SELECT banner FROM v$version WHERE rownum = 1")
        versao_banco = cursor.fetchone()[0]
        
        return {
            "status": "Sucesso",
            "tipo_conexao": "Direta (python-oracledb Thin Mode)",
            "mensagem": "Conexão estabelecida com sucesso sem uso de Wallet!",
            "detalhes_do_banco": versao_banco,
            "data_teste": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Falha na conexão direta com o banco: {str(e)}"
        )
    finally:
        # Garante que as conexões sempre serão fechadas para não estourar o limite do banco
        if cursor:
            cursor.close()
        if connection:
            connection.close()

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