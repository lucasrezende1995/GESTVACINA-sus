from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Conectar ao MongoDB
client = MongoClient("mongodb+srv://<db_Lucas>:<db_lucas_rezende4995>@cluster0.9w1tu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["meu_banco_de_dados"]
patients_collection = db["patients"]

# Criar aplicação FastAPI
app = FastAPI()

# Modelo de resposta
class PatientResponse(BaseModel):
    id: str
    nome: str
    data_nascimento: datetime
    cpf: str
    cartao_sus: str
    genero: str
    endereco: dict
    contato: dict
    comorbidades: List[str]
    alergias_vacinas: List[str]
    historico_vacinal: List[dict]

# Endpoint para buscar paciente pelo CPF
@app.get("/pacientes/{cpf}", response_model=Optional[PatientResponse])
def get_patient(cpf: str):
    patient = patients_collection.find_one({"cpf": cpf})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    # Converter ObjectId para string
    patient["id"] = str(patient["_id"])
    del patient["_id"]
    
    return patient
