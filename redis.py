import redis from pymongo import MongoClient from datetime import timedelta, datetime import json from bson import ObjectId

--- Configurações ---

REDIS_HOST = 'localhost' REDIS_PORT = 6379 MONGO_URI = "mongodb+srv://<db_username>:<db_password>@cluster0.9w1tu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 
DB_NAME = "Cluster0"

--- Conexões ---

def conectar_banco(): """Conecta aos bancos MongoDB e Redis""" try: # MongoDB mongo_client = MongoClient(MONGO_URI) db = mongo_client[DB_NAME] db.command('ping')  # Testa conexão com MongoDB

# Redis
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
        socket_connect_timeout=3
    )
    redis_client.ping()
    
    print("✅ Bancos conectados!")
    return db, redis_client
except Exception as e:
    print(f"❌ Erro de conexão: {e}")
    return None, None

--- Função Principal ---

def buscar_paciente_com_cache(paciente_id, redis_client, db): """ Busca paciente no cache (Redis), se não achar, consulta MongoDB e armazena no cache. """ if redis_client is None or db is None: raise ValueError("Conexões com bancos não estabelecidas")

CACHE_KEY = f"paciente:{paciente_id}"

try:
    # 1. Tentativa de obter do cache
    paciente_cache = redis_client.get(CACHE_KEY)
    
    if paciente_cache:
        print("🟢 Cache hit - Dados do Redis")
        return json.loads(paciente_cache)
    
    print("🔴 Cache miss - Consultando MongoDB...")
    
    # 2. Consulta ao MongoDB
    paciente = db.patients.find_one({"_id": ObjectId(paciente_id)})
    
    if not paciente:
        print("⚠️ Paciente não encontrado no MongoDB")
        return None
    
    # Converte ObjectId para string e prepara para cache
    paciente['_id'] = str(paciente['_id'])
    paciente_json = json.dumps(paciente, default=str)
    
    # 3. Armazena no Redis por 1 hora (3600 segundos)
    redis_client.setex(CACHE_KEY, timedelta(seconds=3600), paciente_json)
    
    return paciente
    
except Exception as e:
    print(f"⚠️ Erro durante operação: {e}")
    return None

--- Uso na Aplicação ---

if name == "main": # Conecta aos bancos db, redis_client = conectar_banco()

# Verificação correta das conexões
if db is not None and redis_client is not None:
    try:
        # Teste com um ID que existe no seu banco
        print("\nBusca por paciente existente:")
        paciente_id_valido = "65b8f9e4d1a27c1234567890"  # Substitua por um ID válido
        paciente = buscar_paciente_com_cache(paciente_id_valido, redis_client, db)
        print("Resultado:", paciente)
        
    finally:
        # Fecha conexões
        redis_client.close()
        db.client.close()
else:
    print("❌ Não foi possível iniciar a aplicação devido a erros de conexão")
