import requests
import pandas as pd
import sqlite3
import streamlit as st

conexao = sqlite3.connect('camara_deputados.db')
cursor = conexao.cursor()

def buscar_dados_deputado(deputado):
    query = "(SELECT id FROM Deputados WHERE nome = ?)"
    cursor.execute(query, (deputado,))
    id_deputado = cursor.fetchone()
    if id_deputado:
        return id_deputado[0]
    else:
        return None 

def buscar_despesas_deputado(id_deputado):
    df_deputados = pd.read_sql("SELECT * FROM Deputados", conexao)
    df_despesas = pd.read_sql("SELECT * FROM Deputados_Despesas", conexao)
    df_deputados_despesas = pd.merge(df_deputados, df_despesas, left_on="id", right_on="deputado_id", how="left")
    
    tres_anos = df_deputados_despesas [df_deputados_despesas['ano']>=2023]
    df_id = tres_anos[tres_anos['id_deputado']==id_deputado]
    tipo_gastos = (df_id.groupby(['id_deputado', 'nome', 'tipoDespesa'])['valorLiquido'].sum().reset_index())
    return tipo_gastos
    

st.title("Análises de gastos de deputados")

deputado = st.text_input("Digite o nome do deputado:", key="deputado")
pesquisar = st.button("Pesquisar")

if pesquisar:
    id_deputado = buscar_dados_deputado(deputado)
    deputado_despesa = buscar_despesas_deputado(id_deputado)
    if deputado_despesa:
        st.subheader(f"Tipo de Gastos do Deputado {deputado}")
        st.dataframe(deputado_despesa)
    else:
        st.error("Deputado não encontrado ou sem gastos registrados.")
             
conexao.close()