from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# Conectar ao MongoDB (substitua pela sua string de conexão)
client = MongoClient("mongodb+srv://<db_Lucas>:<db_lucasrezende_4995>@cluster0.9w1tu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  
db = client["meu_banco_de_dados"]  # Nome do banco de dados

# Criar coleções
patients_collection = db["patients"]
vaccines_collection = db["vaccines"]
appointments_collection = db["appointments"]
reports_collection = db["reports"]

# Inserir um paciente
patient_data = {
    "_id": ObjectId(),
    "nome": "Lucas Paes",
    "data_nascimento": datetime(1999, 5, 20),
    "cpf": "123.456.789-00",
    "cartao_sus": "123456789012345",
    "genero": "Masculino",
    "endereco": {
        "rua": "Rua A",
        "numero": 100,
        "cidade": "Uberlândia",
        "estado": "MG",
        "cep": "38400-000"
    },
    "contato": {
        "telefone": "(34) 99999-9999",
        "email": "lucas@email.com"
    },
    "comorbidades": ["Hipertensão"],
    "alergias_vacinas": ["Nenhuma"],
    "historico_vacinal": []
}
patients_collection.insert_one(patient_data)

# Inserir uma vacina
vaccine_data = {
    "_id": ObjectId(),
    "nome": "COVID-19",
    "fabricante": "Pfizer",
    "doses": 2,
    "intervalo_dias": 21,
    "lote": "L123456",
    "validade": datetime(2025, 12, 31)
}
vaccines_collection.insert_one(vaccine_data)

# Inserir um agendamento
appointment_data = {
    "_id": ObjectId(),
    "paciente_id": patient_data["_id"],
    "vacina_id": vaccine_data["_id"],
    "data_agendamento": datetime(2025, 3, 15),
    "dose": "1ª Dose",
    "local": "Posto Central",
    "status": "Agendado"
}
appointments_collection.insert_one(appointment_data)

# Inserir um relatório
report_data = {
    "_id": ObjectId(),
    "regiao": "Sudeste",
    "vacina": "COVID-19",
    "doses_aplicadas": 10000,
    "doses_pendentes": 5000,
    "data_atualizacao": datetime.now()
}
reports_collection.insert_one(report_data)

print("Dados inseridos com sucesso!")
