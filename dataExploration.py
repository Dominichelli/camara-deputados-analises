# Explorando a API de Dados Abertos da Câmara dos Deputados, para analisar quais dados são relevantes para o projeto

import requests
import json

url = "https://dadosabertos.camara.leg.br/api/v2/votacoes"
response = requests.get(url).json()

dados = response["dados"][:10] # Pega apenas os primeiros 10 registros para exemplo

print(json.dumps(response, indent=4, ensure_ascii=False)) #Torna os dados legíveis

#Verificando quais deputados tem base de despesas
#ids = [dep["id"] for dep in response["dados"]]
#print(ids)

#for id_deputado in ids:  
    #url_despesas = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_deputado}/despesas"
    #despesas = requests.get(url_despesas).json()
    
    #if despesas:
       # print(f"Deputado ID {id_deputado} possui despesas.")

#verificando quais proposições tem tramitação
#ids_prop = [prop["id"] for prop in response ["dados"]]
#print(ids_prop)

#for id_prop in ids_prop:
    #url_tramitacoes = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id_prop}/tramitacoes"
    #tramitacoes = requests.get(url_tramitacoes).json()
    
#if tramitacoes:
    #print(f"Proposicao ID {id_prop} possui tramitacoes.")
    
#verificando quais votacoes possuem votos

# ids_votacoes = [votacoes["id"] for votacoes in response ["dados"]]
# print(ids_votacoes)

# for id_votos in ids_votacoes:
#     url_votos = f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{id_votos}/votos"
#     response_votos = requests.get(url_votos).json()

#     if response_votos["dados"]:
#         print(f"votos ID {id_votos} possui votos.")

