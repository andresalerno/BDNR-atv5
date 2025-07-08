## Atividade #5 - Professor Diogo Branquinho

```powershell
# criar uma venv
python -m venv venv
```
```powershell
venv\Scripts\activate
```

```powershell
py -3 -m pip isntall -r requirements.txt
```

## Output gerado para a conexão com o Neo4j

```powershell
python .\app.py
```

```powershell
# output
Conexão com o Neo4j realizada com sucesso!
Usuário João Silva inserido com sucesso no Neo4j.
Usuário encontrado: João Silva, Email: joao@email.com, Favoritos: []
Produto Celular inserido com sucesso no Neo4j.
Produto encontrado: Celular, Descrição: iPhone 14 Pro Max
Inserindo compra com ID: edcaeed3-b72f-4cbb-917f-f2e783d913f0 e dados: {'id_usuario': 'u1', 'data': '2024-04-01', 'preco_total': 1800, 'status': 'pendente', 'itens': [{'id_produto': 'p1', 'quantidade': 1, 'preco_unitario': 1000}, {'id_produto': 'p2', 'quantidade': 1, 'preco_unitario': 800}]}
Compra edcaeed3-b72f-4cbb-917f-f2e783d913f0 inserida com sucesso no Neo4j.
```

## Trial Expired

<img src="../neo4j/img/trial-expired.png" alt="trial-expired" width="700"/>
