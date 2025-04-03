import redis
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# --- Configurações --- #
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
MONGO_URI = "mongodb+srv://Lucas:<db_password>@cluster0.9w1tu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Cluster0"

# --- Conexões --- #
def conectar_banco():
    try:
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client[DB_NAME]
        db.command('ping')

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

# --- Bitmap (Acesso a Prontuários) --- #
def marcar_acesso_paciente(paciente_id, redis_client):
    BITMAP_KEY = "acesso_pacientes"
    hash_id = hash(paciente_id) % 1000000  # Mantém um tamanho razoável
    redis_client.setbit(BITMAP_KEY, hash_id, 1)

def checar_acesso_paciente(paciente_id, redis_client):
    BITMAP_KEY = "acesso_pacientes"
    hash_id = hash(paciente_id) % 1000000
    return redis_client.getbit(BITMAP_KEY, hash_id) == 1

# --- Bloom Filter (Evitar Busca Desnecessária de Prontuários) --- #
def adicionar_paciente_bloom(paciente_id, redis_client):
    BLOOM_KEY = "bloom:pacientes"
    redis_client.bf().add(BLOOM_KEY, paciente_id)

def verificar_paciente_bloom(paciente_id, redis_client):
    BLOOM_KEY = "bloom:pacientes"
    return redis_client.bf().exists(BLOOM_KEY, paciente_id)

# --- Uso na Aplicação --- #
if __name__ == "__main__":
    db, redis_client = conectar_banco()

    if db is not None and redis_client is not None:
        try:
            paciente = "pac_12345"
            
            # Bitmap - Marcar e verificar acesso ao prontuário
            print("\n=== BITMAP (Acesso a Prontuários) ===")
            marcar_acesso_paciente(paciente, redis_client)
            print(f"O prontuário do paciente {paciente} já foi acessado?", checar_acesso_paciente(paciente, redis_client))
            
            # Bloom Filter - Adicionar e verificar existência
            print("\n=== BLOOM FILTER (Prontuários Cadastrados) ===")
            adicionar_paciente_bloom(paciente, redis_client)
            print(f"O paciente {paciente} tem prontuário no sistema?", verificar_paciente_bloom(paciente, redis_client))
        
        finally:
            redis_client.close()
            db.client.close()
