import pyodbc
import requests
import json

#conexão com Banco de Dados SQL Server
dados_conexao = (
    "Driver={SQL Server};"
    "Server=Meu_Servidor;"
    "Database=RenovaBr;"
)

conexao = pyodbc.connect(dados_conexao)
print ("Conexão bem sucedida!")

cursor = conexao.cursor()   

#URL da API de Deputados
url_deputados = "https://dadosabertos.camara.leg.br/api/v2/deputados"
response_deputados = requests.get(url_deputados).json()

#Criação tabela Deputados
create_tabela_deputados = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name= 'Deputados' AND xtype='U')
CREATE TABLE Deputados (
    id INT PRIMARY KEY,
    nome NVARCHAR(255),
    siglaPartido NVARCHAR(10),
    siglaUf NVARCHAR(5),
    email NVARCHAR(255)
);
"""

cursor.execute(create_tabela_deputados)
conexao.commit()
print("Tabela Deputados criada com sucesso!")

#Alterando tamanho da coluna siglaPartido
alterar_tabela_deputados = """
ALTER TABLE Deputados
ALTER COLUMN siglaPartido NVARCHAR(50);
"""
cursor.execute(alterar_tabela_deputados)
cursor.commit()
print("Coluna siglaPartido alterada com sucesso!")

#Insere dados na tabela Deputados
insert_tabela_deputados = """
INSERT INTO Deputados (id, nome, siglaPartido, siglaUf, email)
VALUES (?, ?, ?, ?, ?)
"""

dados = response_deputados["dados"] # Pega todos os registros
for dep in dados:
    cursor.execute(insert_tabela_deputados, 
                   dep["id"], 
                   dep["nome"], 
                   dep.get("siglaPartido", None),
                   dep.get("siglaUf", None),
                   dep.get("email", None)
                   )
print("Dados inseridos com sucesso na tabela Deputados!")

cursor.commit()

#Criando tabela Despesas
create_tabela_deputados_despesas = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'Deputados_Despesas' AND xtype = 'U')
CREATE TABLE dbo.Deputados_Despesas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_deputado INT,
    ano INT,
    mes INT,
    tipoDespesa NVARCHAR(1000),
    tipoDocumento NVARCHAR(500),
    valorLiquido DECIMAL(18, 2),
    FOREIGN KEY (id_deputado) REFERENCES dbo.Deputados(id)
);
"""
cursor.execute(create_tabela_deputados_despesas)
conexao.commit()
print("Tabela Deputados_Despesas criada com sucesso!")

#URL da API de Despesas + insere dados na tabela Despesas
insert_tabela_deputados_despesas = """
INSERT INTO Deputados_Despesas (id_deputado, ano, mes, tipoDespesa, tipoDocumento, valorLiquido)
VALUES (?, ?, ?, ?, ?, ?)
"""

ids = [dep["id"]for dep in response_deputados["dados"]]

for id_deputados in ids:
    url_despesas = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_deputados}/despesas"
    response_despesas = requests.get(url_despesas).json()
    
    if response_despesas["dados"]:
        dados = response_despesas["dados"]
        for desp in dados:
            cursor.execute(insert_tabela_deputados_despesas,
                   id_deputados,
                   desp.get("ano", None),
                   desp.get("mes", None),
                   desp.get("tipoDespesa", None),
                   desp.get("tipoDocumento", None),
                   desp.get("valorLiquido", None)
                   )
            print(f"Dados inseridos com sucesso na tabela Deputados_Despesas para o deputado ID {id_deputados}!")  
cursor.commit()    
print("Todos os dados de despesas foram inseridos com sucesso na tabela Deputados_Despesas!")

#Criando tabela Ocupacoes
create_tabela_deputados_ocupacoes = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'Deputado_Ocupacoes' AND xtype = 'U' )
CREATE TABLE dbo.Deputado_Ocupacoes(
  id INT IDENTITY(1,1) PRIMARY KEY,
  id_deputado INT,
  titulo NVARCHAR(1000),
  entidade NVARCHAR(500),
  entidadeUf NVARCHAR(10),
  entidadePais NVARCHAR(100),
  anoInicio INT,
  anoFim INT,   
  FOREIGN KEY (id_deputado) REFERENCES dbo.Deputados(id)
);
"""
cursor.execute(create_tabela_deputados_ocupacoes)
conexao.commit()
print("Tabela Ocupacoes criada com sucesso!")

# Insere dados na tabela Ocupacoes
insert_tabela_deputados_ocupacoes = """
INSERT INTO Deputado_Ocupacoes (id_deputado, titulo, entidade, entidadeUf, entidadePais, anoInicio, anoFim)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

#URL da API de Ocupacoes + insere dados na tabela Ocupacoes
ids_ocup = [ocup["id"]for ocup in response_deputados["dados"]]

for id_deputados in ids_ocup:
    url_ocupacoes = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_deputados}/ocupacoes"
    response_ocupacoes = requests.get(url_ocupacoes).json()
    
    if response_ocupacoes["dados"]:
        dados = response_ocupacoes["dados"]
        for ocup in dados:
            cursor.execute(insert_tabela_deputados_ocupacoes,
                   id_deputados,
                   ocup.get("title", None),
                   ocup.get("entidade", None),
                   ocup.get("entidadeUf", None),
                   ocup.get("entidadePais", None),
                   ocup.get("anoInicio", None),
                   ocup.get("anoFim", None)
                   )
            print(f"Dados inseridos com sucesso na tabela Deputados_Ocupacoes para o deputado ID {id_deputados}!")  
cursor.commit()    
print("Todos os dados de ocupações foram inseridos com sucesso na tabela Deputados_Ocupacoes!")

#URL da API de Votacoes
url_votacoes = "https://dadosabertos.camara.leg.br/api/v2/votacoes"
response_votacoes = requests.get(url_votacoes).json()

#Criando tabela Votacoes
create_tabela_votacoes = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'Votacoes' AND xtype = 'U')
CREATE TABLE dbo.Votacoes (
       id NVARCHAR(50) PRIMARY KEY,
       descricao NVARCHAR(500),
       data DATE,
       siglaOrgao NVARCHAR(20)
);
"""
cursor.execute(create_tabela_votacoes)
conexao.commit()
print("Tabela Votacoes criada com sucesso!")

#Insere dados na tabela Votacoes
insert_tabela_votacoes = """
INSERT INTO Votacoes (id, descricao, data, siglaOrgao)
VALUES (?, ?, ?, ?)
"""

dados = response_votacoes["dados"]
for vot in dados:
    cursor.execute(insert_tabela_votacoes, 
                   vot["id"], 
                   vot.get("descricao", None),
                   vot.get("data", None),
                   vot.get("siglaOrgao", None)
                   )

cursor.commit()
print("Todos os dados de votações foram inseridos com sucesso na tabela Votacoes!")

#Criação tabela Votos
create_tabela_votos = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'Votos' AND xtype = 'U')
CREATE TABLE dbo.Votos (
   id INT IDENTITY(1,1) PRIMARY KEY,
   tipoVoto NVARCHAR(100),
   siglaPartido NVARCHAR(10),
   id_votacao NVARCHAR(50),
   id_deputado INT,
   FOREIGN KEY (id_votacao) REFERENCES dbo.Votacoes(id),
   FOREIGN KEY (id_deputado) REFERENCES dbo.Deputados(id)
);
"""
cursor.execute(create_tabela_votos)
conexao.commit()
print("Tabela Votos criada com sucesso!")

#Insere dados na tabela Votos
insert_tabela_votos = """
insert into Votos (tipoVoto, siglaPartido, id_votacao, id_deputado)
values (?, ?, ?, ?)
""" 

ids_votos = [votos["id"] for votos in response_votacoes["dados"]]
for id_votacoes in ids_votos:
    url_votos = f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{id_votacoes}/votos"
    response_votos = requests.get(url_votos).json()
    
    if response_votos.get("dados"):
        dados = response_votos["dados"]
        for voto in dados:
            cursor.execute(insert_tabela_votos,
                voto.get("tipoVoto", None),
                voto.get("siglaPartido", None),
                id_votacoes,
                voto.get("deputado", {}).get("id", None)
            )
            print(f"Dados inseridos com sucesso na tabela Votos para a votação ID {id_votacoes}!")
cursor.commit()
print("Todos os dados de votos foram inseridos com sucesso na tabela Votos!")


cursor.close()
conexao.close()
print("Conexão encerrada.")