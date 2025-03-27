import redis
import json

# Conectar ao Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Dados do paciente (adaptado para Redis)
patient_key = "patient:65b8f9e4d1a27c1234567890"
patient_data = {
    "nome": "Lucas Paes de Rezende",
    "data_nascimento": "1999-05-15",
    "cpf": "123.456.789-00",
    "cartao_sus": "987654321000",
    "genero": "Masculino",
    "endereco": json.dumps({
        "rua": "Av. João Naves de Ávila",
        "numero": "123",
        "cidade": "Uberlândia",
        "estado": "MG",
        "cep": "38400-000"
    }),
    "contato": json.dumps({
        "telefone": "(34) 98765-4321",
        "email": "lucas@email.com"
    }),
    "comorbidades": json.dumps(["Não"]),
    "alergias_vacinas": json.dumps(["Não"])
}

# Salvar paciente no Redis como Hash
r.hset(patient_key, mapping=patient_data)

# Salvar histórico vacinal como Lista
historico_vacinal_key = f"{patient_key}:historico_vacinal"
historico_vacinal = {
    "vacina_id": "659a123bde4f56789abc0123",
    "data_aplicacao": "2021-10-02",
    "dose": "1ª dose",
    "local": "UBS Centro",
    "profissional": "Dr. José Silva"
}
r.rpush(historico_vacinal_key, json.dumps(historico_vacinal))

# Salvar informações da vacina como Hash
vaccine_key = "vaccine:659a123bde4f56789abc0123"
vaccine_data = {
    "nome": "COVID-19 (Pfizer)",
    "fabricante": "Pfizer",
    "doses": "2",
    "intervalo_dias": "21",
    "lote": "ABC12345",
    "validade": "2025-04-05"
}
r.hset(vaccine_key, mapping=vaccine_data)

# Salvar um agendamento como Hash
appointment_key = "appointment:660bcd123e4f56789abc4567"
appointment_data = {
    "paciente_id": "65b8f9e4d1a27c1234567890",
    "vacina_id": "659a123bde4f56789abc0123",
    "data_agendamento": "2025-03-04",
    "dose": "2ª dose",
    "local": "UBS Centro",
    "status": "Pendente"
}
r.hset(appointment_key, mapping=appointment_data)

print("Dados armazenados no Redis com sucesso!")

criar um hash

r.hset(patient_key, mapping=patient_data)

criar chave patient

HSET patient:65b8f9e4d1a27c1234567890 nome "Lucas Paes de Rezende"
