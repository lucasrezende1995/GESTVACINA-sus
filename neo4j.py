from neo4j import GraphDatabase
from pymongo import MongoClient
from bson import ObjectId

# === CONFIGS ===
NEO4J_URI = "neo4j+s://f44d6125.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "EPdlZt8PCE-CUz0tSvm3m6OdfHrw7hB7WXHnbksyP8M"

mongo_client = MongoClient(mongodb+srv://lucasrezende1995_:<db_password>@cluster0.9w1tu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0)
mongo_db = mongo_client["sus_db"]
pacientes = mongo_db["pacientes"]
profissionais = mongo_db["profissionais"]
unidades = mongo_db["unidades"]
atendimentos = mongo_db["atendimentos"]

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# === FUNÇÕES ===

def criar_paciente(tx, paciente):
    tx.run("""
        MERGE (p:Paciente {cpf: $cpf})
        SET p.nome = $nome, p.nascimento = $nascimento
    """, cpf=paciente["cpf"], nome=paciente["nome"], nascimento=paciente["nascimento"])

def criar_profissional(tx, profissional):
    tx.run("""
        MERGE (pr:Profissional {nome: $nome})
        SET pr.especialidade = $especialidade
    """, nome=profissional["nome"], especialidade=profissional["especialidade"])

def criar_unidade(tx, unidade):
    tx.run("""
        MERGE (u:Unidade {nome: $nome})
        SET u.tipo = $tipo
    """, nome=unidade["nome"], tipo=unidade["tipo"])

def criar_atendimento(tx, atendimento):
    tx.run("""
        MERGE (a:Atendimento {id: $id})
        SET a.tipo = $tipo
    """, id=str(atendimento["_id"]), tipo=atendimento["tipo"])

    tx.run("""
        MATCH (p:Paciente {cpf: $cpf}),
              (pr:Profissional {nome: $profissional}),
              (u:Unidade {nome: $unidade})
        MERGE (a:Atendimento {id: $id})
        MERGE (p)-[:REALIZOU]->(a)
        MERGE (a)-[:FOI_FEITO_POR]->(pr)
        MERGE (a)-[:OCORREU_EM]->(u)
    """, cpf=atendimento["cpf_paciente"],
         profissional=atendimento["profissional"],
         unidade=atendimento["unidade"],
         id=str(atendimento["_id"]))

    if "diagnostico" in atendimento:
        tx.run("""
            MERGE (d:Diagnostico {nome: $diag})
            MERGE (a:Atendimento {id: $id})-[:GEROU_DIAGNOSTICO]->(d)
        """, diag=atendimento["diagnostico"], id=str(atendimento["_id"]))

    if "data" in atendimento:
        tx.run("""
            MERGE (dt:Data {data: $data})
            MERGE (a:Atendimento {id: $id})-[:NA_DATA]->(dt)
        """, data=atendimento["data"], id=str(atendimento["_id"]))


# === EXECUÇÃO ===

with neo4j_driver.session() as session:
    print(session.run("RETURN 'Neo4j conectado com sucesso!' AS msg").single()["msg"])

    for paciente in pacientes.find():
        session.execute_write(criar_paciente, paciente)

    for profissional in profissionais.find():
        session.execute_write(criar_profissional, profissional)

    for unidade in unidades.find():
        session.execute_write(criar_unidade, unidade)

    for atendimento in atendimentos.find():
        session.execute_write(criar_atendimento, atendimento)

print("✅ Dados importados com sucesso para o Neo4j!")
neo4j_driver.close()
