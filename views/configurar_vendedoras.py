import streamlit as st
import pandas as pd
import datetime
from auxiliar.auxiliar import *
import hashlib

def convert_name_to_id(name):
  id = hashlib.md5(name.encode()).hexdigest()[:12]
  return id

st.set_page_config(page_title="RPD - Configurar Vendedoras", page_icon="💎",layout="wide")

st.title("Dados das Vendedoras")

vendedoras_df = get_dataframe_from_mongodb(collection_name="dados_vendedoras", database_name="rpd_db")

vendedora_url = "https://rpd-visualizar.streamlit.app/visualisar?id="

colunas = ["id_vendedora","nome_vendedora","EMAIL","LOJA","meta","status_vendedora"]
column_order = ["nome_vendedora","LOJA","meta","EMAIL","url_vendedora"]

vendedoras_df["url_vendedora"] = vendedoras_df["id_vendedora"].apply(lambda x: vendedora_url + x)

lojas = ['TATUAPÉ', 'MOOCA', 'SANTO AMARO', 'SANTOS', 'COPACABANA',
       'LAPA', 'MOEMA', 'JARDINS', 'CAMPINAS', 'TIJUCA', 'TUCURUVI',
       'IPIRANGA', 'LONDRINA', 'SÃO BERNARDO', 'SOROCABA', 'OSASCO',
       'ALPHAVILLE', 'RIBEIRÃO PRETO']

column_config = {
        "LOJA": st.column_config.SelectboxColumn(
            "loja",
            options=lojas
        )
    }

st.data_editor(
    vendedoras_df,
    column_config=column_config,
    column_order = column_order,
    hide_index=True,
    use_container_width=True
)
