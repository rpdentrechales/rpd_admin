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

st.write(vendedoras_df.columns)

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
    hide_index=True,
    use_container_width=True
)
