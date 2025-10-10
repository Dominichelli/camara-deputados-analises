import sqlite3
import requests

# Criação do banco de Dados
conexao = sqlite3.connect('camara_deputados.db')
cursor = conexao.cursor()
print("Conexão bem sucedida!")

#URL da API de Deputados
url_deputados = "https://dadosabertos.camara.leg.br/api/v2/deputados"
response_deputados = requests.get(url_deputados).json()

#Criação tabela Deputados
create_tabela_deputados = """
    CREATE TABLE Deputados (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    siglaPartido TEXT,
    siglaUf TEXT,
    email TEXT
);
"""

cursor.execute(create_tabela_deputados)
conexao.commit()
print("Tabela Deputados criada com sucesso!")

insert_tabela_deputados = """
INSERT OR IGNORE INTO Deputados (id, nome, siglaPartido, siglaUf, email)
VALUES (?, ?, ?, ?, ?)
"""

dados_deputados = response_deputados["dados"]
for dep in dados_deputados:
    cursor.execute(insert_tabela_deputados, (
                   dep["id"],
                   dep["nome"],
                   dep.get("siglaPartido", None),
                   dep.get("siglaUf", None),
                   dep.get("email", None)
                   ))

conexao.commit()
print("Dados inseridos com sucesso na tabela Deputados!")

#Criando tabela Despesas
create_tabela_deputados_despesas = """
CREATE TABLE Deputados_Despesas (
    id INTEGER PRIMARY KEY,
    id_deputado INTEGER,
    ano INTEGER,
    mes INTEGER,
    tipoDespesa TEXT,
    tipoDocumento TEXT,
    valorLiquido REAL,
    FOREIGN KEY (id_deputado) REFERENCES Deputados(id)
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
            cursor.execute(insert_tabela_deputados_despesas,(
                   id_deputados,
                   desp.get("ano", None),
                   desp.get("mes", None),
                   desp.get("tipoDespesa", None),
                   desp.get("tipoDocumento", None),
                   desp.get("valorLiquido", None)
                   ))
            print(f"Dados inseridos com sucesso na tabela Deputados_Despesas para o deputado ID {id_deputados}!")  
conexao.commit()  
print("Todos os dados de despesas foram inseridos com sucesso na tabela Deputados_Despesas!")

#Criando tabela Ocupacoes
create_tabela_deputados_ocupacoes = """
CREATE TABLE Deputado_Ocupacoes(
  id INTEGER PRIMARY KEY,
  id_deputado INTEGER,
  titulo TEXT,
  entidade TEXT,
  entidadeUf TEXT,
  entidadePais TEXT,
  anoInicio INTEGER,
  anoFim INTEGER,
  FOREIGN KEY (id_deputado) REFERENCES Deputados(id)
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
insert_tabela_deputados_ocupacoes = """
INSERT INTO Deputado_Ocupacoes 
(id_deputado, titulo, entidade, entidadeUf, entidadePais, anoInicio, anoFim)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

ids_ocup = [ocup["id"] for ocup in response_deputados["dados"]]

for id_deputado in ids_ocup:
    url_ocupacoes = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_deputado}/ocupacoes"
    response_ocupacoes = requests.get(url_ocupacoes).json()
    
    if response_ocupacoes.get("dados"):
        dados = response_ocupacoes["dados"]
        for ocup in dados:
            cursor.execute(insert_tabela_deputados_ocupacoes, (
                id_deputado,
                ocup.get("titulo", None),
                ocup.get("entidade", None),
                ocup.get("entidadeUf", None),
                ocup.get("entidadePais", None),
                ocup.get("anoInicio", None),
                ocup.get("anoFim", None)
            ))
            print(f"Dados inseridos com sucesso na tabela Deputado_Ocupacoes para o deputado ID {id_deputado}!")

conexao.commit()
print("Todos os dados de ocupações foram inseridos com sucesso na tabela Deputado_Ocupacoes!")

#URL da API de Votacoes
url_votacoes = "https://dadosabertos.camara.leg.br/api/v2/votacoes"
response_votacoes = requests.get(url_votacoes).json()

#Criando tabela Votacoes
create_tabela_votacoes = """
CREATE TABLE Votacoes (
       id TEXT PRIMARY KEY,
       descricao TEXT,
       data DATE,
       siglaOrgao TEXT
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
    cursor.execute(insert_tabela_votacoes, (
                   vot["id"], 
                   vot.get("descricao", None),
                   vot.get("data", None),
                   vot.get("siglaOrgao", None)
                   ))

conexao.commit()
print("Todos os dados de votações foram inseridos com sucesso na tabela Votacoes!")

#Criação tabela Votos
create_tabela_votos = """
CREATE TABLE Votos (
   id INTEGER PRIMARY KEY,
   tipoVoto TEXT,
   siglaPartido TEXT,
   id_votacao TEXT,
   id_deputado INTEGER,
   FOREIGN KEY (id_votacao) REFERENCES Votacoes(id),
   FOREIGN KEY (id_deputado) REFERENCES Deputados(id)
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
            cursor.execute(insert_tabela_votos, (
    voto.get("tipoVoto", None),
    voto.get("siglaPartido", None),
    id_votacoes,
    voto.get("deputado", {}).get("id", None)
))

            print(f"Dados inseridos com sucesso na tabela Votos para a votação ID {id_votacoes}!")
conexao.commit()
print("Todos os dados de votos foram inseridos com sucesso na tabela Votos!")

#Fechando a conexão
cursor.close()
conexao.close()
print("Conexão encerrada.")
