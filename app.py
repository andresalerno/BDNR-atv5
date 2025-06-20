from neo4j import GraphDatabase
from uuid import uuid4
import json
import database
import os
from dotenv import load_dotenv

# Função para conectar ao Neo4j com retries


load_dotenv()

def connect_to_neo4j():
    uri = os.getenv("NEO4J_URI")  # URI padrão do Neo4j
    username = os.getenv("NEO4J_USERNAME")  # Substitua com o nome de usuário do seu banco Neo4j
    if not username:
        username = "neo4j"  # Nome de usuário padrão do Neo4j   
    password = os.getenv("NEO4J_PASSWORD")  # Substitua com a senha do seu banco Neo4j
    driver = GraphDatabase.driver(uri, auth=(username, password))
    session = driver.session()
    # print("Conexão bem-sucedida com o Neo4j!")
    return session

# Tentativa de conexão com o banco Neo4j
try:
    session = connect_to_neo4j()                
except Exception as e:
    # Caso ocorra um erro na conexão
    print(f"Erro ao tentar conectar ao Neo4j: {e}")

# Função de inserção no Neo4j
def insert_user(session, usuario_data):
    user_id = str(uuid4())  # Gera um ID único para o usuário
    try:
        query = """
        CREATE (u:Usuario {user_id: $user_id, nome: $nome, email: $email, telefone: $telefone, tipo_usuario: $tipo_usuario, documento: $documento, dados_pessoa_fisica: $dados_pessoa_fisica, dados_empresa: $dados_empresa})
        """
        session.run(query, parameters={
            "user_id": user_id,
            "nome": usuario_data["nome"],
            "email": usuario_data["email"],
            "telefone": usuario_data["telefone"],
            "tipo_usuario": usuario_data["tipo_usuario"],
            "documento": usuario_data["documento"],
            "dados_pessoa_fisica": json.dumps(usuario_data["dados_pessoa_fisica"]),
            "dados_empresa": json.dumps(usuario_data["dados_empresa"])
        })
        print(f"Usuário {usuario_data['nome']} inserido com sucesso no Neo4j.")
        return user_id  # Retorna o ID do usuário para ser usado na criação dos relacionamentos
    except Exception as e:
        print(f"Erro ao inserir usuário {usuario_data['nome']}: {e}")
        return None

# Função de pesquisa de usuário no Neo4j
def search_user(session, user_id):
    try:
        query = """
        MATCH (u:Usuario {user_id: $user_id})
        RETURN u
        """
        result = session.run(query, parameters={"user_id": user_id})
        user = result.single()
        if user:
            print(f"Usuário encontrado: {user['u']['nome']}, Email: {user['u']['email']}")
        else:
            print("Usuário não encontrado.")
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")


# Função de inserção de produto no Neo4j
def insert_product(session, produto_data, user_id):
    produto_id = str(uuid4())  # Gera um ID único para o produto
    try:
        query = """
        CREATE (p:Produto {produto_id: $produto_id, nome: $nome, descricao: $descricao, id_vendedor: $id_vendedor, status: $status, precos: $precos})
        """
        session.run(query, parameters={
            "produto_id": produto_id,
            "nome": produto_data["nome"],
            "descricao": produto_data["descricao"],
            "id_vendedor": produto_data["id_vendedor"],
            "status": produto_data["status"],
            "precos": json.dumps(produto_data["precos"])
        })
        
        # Criar relacionamento entre Usuário e Produto (Vende)
        session.run("""
        MATCH (u:Usuario {user_id: $user_id}), (p:Produto {produto_id: $produto_id})
        CREATE (u)-[:VENDE]->(p)
        """, parameters={"user_id": user_id, "produto_id": produto_id})
        
        print(f"Produto {produto_data['nome']} inserido com sucesso no Neo4j.")
        return produto_id  # Retorna o ID do produto para ser usado na criação dos relacionamentos
    except Exception as e:
        print(f"Erro ao inserir produto {produto_data['nome']}: {e}")
        return None

# Função de pesquisa de produto no Neo4j
def search_product(session, produto_id):
    try:
        query = """
        MATCH (p:Produto {produto_id: $produto_id})
        RETURN p
        """
        result = session.run(query, parameters={"produto_id": produto_id})
        product = result.single()
        if product:
            print(f"Produto encontrado: {product['p']['nome']}, Descrição: {product['p']['descricao']}")
        else:
            print("Produto não encontrado.")
    except Exception as e:
        print(f"Erro ao buscar produto: {e}")

def search_user_by_product(session, produto_id):
    print(f"Buscando usuário que vende o produto com ID: {produto_id}")
    try:
        query = """
        MATCH (p:Produto {produto_id: $produto_id})<-[:VENDE]-(u:Usuario)
        RETURN u
        """
        result = session.run(query, parameters={"produto_id": produto_id})
        user = result.single()  # Obtém o primeiro resultado da consulta
        if user:
            print(f"Usuário encontrado: {user['u']['nome']}, Email: {user['u']['email']}")
        else:
            print("Nenhum usuário encontrado para este produto.")
    except Exception as e:
        print(f"Erro ao buscar usuário do produto: {e}")


def search_products_by_purchase(session, compra_id):
    print(f"Buscando produtos da compra com ID: {compra_id}")
    try:
        query = """
        MATCH (c:Compra {compra_id: $compra_id})-[:CONTÉM]->(p:Produto)
        RETURN p
        """
        result = session.run(query, parameters={"compra_id": compra_id})
        products = result.fetchall()  # Obtém todos os resultados
        if products:
            for product in products:
                print(f"Produto encontrado: Nome: {product['p']['nome']}, Descrição: {product['p']['descricao']}")
        else:
            print("Nenhum produto encontrado para esta compra.")
    except Exception as e:
        print(f"Erro ao buscar produtos da compra: {e}")



# Função de inserção de compra no Neo4j
def insert_purchase(session, compra_data, user_id, produto_ids):
    compra_id = str(uuid4())  # Gera um ID único para a compra
    try:
        print(f"Inserindo compra com ID: {compra_id} e dados: {compra_data}")
        
        # Query para criar o nó da compra
        query = """
        CREATE (c:Compra {compra_id: $compra_id, id_usuario: $id_usuario, data: $data, preco_total: $preco_total, status: $status, itens: $itens})
        """
        session.run(query, parameters={
            "compra_id": compra_id,
            "id_usuario": compra_data["id_usuario"],
            "data": compra_data["data"],
            "preco_total": compra_data["preco_total"],
            "status": compra_data["status"],
            "itens": json.dumps(compra_data["itens"])
        })
        print(f"Compra {compra_id} inserida com sucesso no Neo4j.")
        
        # Criar relacionamento entre Compra e Produto (Contém)
        for produto_id in produto_ids:
            session.run("""
            MATCH (c:Compra {compra_id: $compra_id}), (p:Produto {produto_id: $produto_id})
            CREATE (c)-[:CONTÉM]->(p)
            """, parameters={"compra_id": compra_id, "produto_id": produto_id})
        
        # Criar relacionamento entre Usuário e Compra (Fez)
        session.run("""
        MATCH (u:Usuario {user_id: $user_id}), (c:Compra {compra_id: $compra_id})
        CREATE (u)-[:FEZ]->(c)
        """, parameters={"user_id": user_id, "compra_id": compra_id})
        
        return compra_id  # Retorna o ID da compra
    except Exception as e:
        print(f"Erro ao inserir compra {compra_id}: {e}")
        return None






# Função de pesquisa de compra no Neo4j
def search_purchase(session, compra_id):
    print(f"Buscando compra com ID: {compra_id}")
    try:
        query = """
        MATCH (c:Compra {compra_id: $compra_id})
        RETURN c
        """
        result = session.run(query, parameters={"compra_id": compra_id})
        purchase = result.single()  # Obtém o primeiro resultado da consulta
        if purchase:
            print(f"Compra encontrada: ID Usuário: {purchase['c']['id_usuario']}, Preço Total: {purchase['c']['preco_total']}")
            print(f"Itens: {purchase['c']['itens']}")
        else:
            print("Compra não encontrada.")
    except Exception as e:
        print(f"Erro ao buscar compra: {e}")

def search_purchases_by_user(session, user_id):
    print(f"Buscando compras do usuário com ID: {user_id}")
    try:
        query = """
        MATCH (u:Usuario {user_id: $user_id})-[:FEZ]->(c:Compra)
        RETURN c
        """
        result = session.run(query, parameters={"user_id": user_id})
        purchases = result.fetchall()  # Obtém todos os resultados
        if purchases:
            for purchase in purchases:
                print(f"Compra encontrada: ID Compra: {purchase['c']['compra_id']}, Preço Total: {purchase['c']['preco_total']}")
                print(f"Itens: {purchase['c']['itens']}")
        else:
            print("Nenhuma compra encontrada para este usuário.")
    except Exception as e:
        print(f"Erro ao buscar compras do usuário: {e}")

def search_products_in_purchase(session, compra_id):
    print(f"Buscando produtos da compra com ID: {compra_id}")
    try:
        query = """
        MATCH (c:Compra {compra_id: $compra_id})-[:CONTÉM]->(p:Produto)
        RETURN p
        """
        result = session.run(query, parameters={"compra_id": compra_id})
        products = result.fetchall()  # Obtém todos os resultados
        if products:
            for product in products:
                print(f"Produto encontrado: Nome: {product['p']['nome']}, Descrição: {product['p']['descricao']}")
        else:
            print("Nenhum produto encontrado para esta compra.")
    except Exception as e:
        print(f"Erro ao buscar produtos da compra: {e}")



# Função principal para inicializar e executar as ações
def main():
    # Conectar ao Neo4j
    session = connect_to_neo4j()

    # Exemplo de inserção de usuário
    usuario_data = {
        "nome": "João Silva",
        "email": "joao@email.com",
        "telefone": "1234567890",
        "tipo_usuario": "pessoa_fisica",
        "documento": "123.456.789-00",
        "dados_pessoa_fisica": {"cpf": "123.456.789-00", "data_nascimento": "1990-01-01", "endereco": "Rua X, 123"},
        "dados_empresa": None
    }
    user_id = insert_user(session, usuario_data)

    # Exemplo de pesquisa de usuário
    if user_id:  # Verifique se o ID foi retornado com sucesso
        search_user(session, user_id)  # Passar o ID do usuário inserido

    # Exemplo de inserção de produto
    produto_data = {
        "nome": "Celular",
        "descricao": "iPhone 14 Pro Max",
        "id_vendedor": "u1",
        "status": "ativo",
        "precos": [
            {"preco": 1000, "data_inicio": "2024-01-01", "data_fim": "2024-05-01"},
            {"preco": 900, "data_inicio": "2024-05-02", "data_fim": None}
        ]
    }
    produto_id = insert_product(session, produto_data, user_id)

    # Exemplo de pesquisa de produto
    if produto_id:  # Verifique se o ID foi retornado com sucesso
        search_product(session, produto_id)  # Passar o ID do produto inserido

    # Exemplo de inserção de compra
    compra_data = {
        "id_usuario": "u1",
        "data": "2024-04-01",
        "preco_total": 1800,
        "status": "pendente",
        "itens": [
            {"id_produto": "p1", "quantidade": 1, "preco_unitario": 1000},
            {"id_produto": "p2", "quantidade": 1, "preco_unitario": 800}
        ]
    }

    user_id = "u1"  # Este é o ID do usuário
    produto_ids = ["p1", "p2"]  # IDs dos produtos que estão sendo comprados
    compra_id = insert_purchase(session, compra_data, user_id, produto_ids)  # Passando o user_id e produto_ids

if __name__ == "__main__":
    main()
