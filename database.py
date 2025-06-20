from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

# URI do Neo4j
URI = os.getenv("NEO4J_URI")
# Substitua pelos seus dados de autenticação
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

# Tentativa de conexão com o banco Neo4j
try:
    # Cria o driver de conexão
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        # Verifica a conectividade
        driver.verify_connectivity()
        print("Conexão com o Neo4j realizada com sucesso!")
except Exception as e:
    # Caso ocorra um erro na conexão
    print(f"Erro ao tentar conectar ao Neo4j: {e}")
