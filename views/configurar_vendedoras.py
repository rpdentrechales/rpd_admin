import streamlit as st
import pandas as pd
import datetime
from auxiliar.auxiliar import *

st.set_page_config(page_title="RPD - Configurar Vendedoras", page_icon="💎",layout="wide")

st.title("Testes - Link das vendedoras")

vendedoras_df = get_dataframe_from_mongodb(collection_name="dados_vendedoras", database_name="rpd_db")

st.dataframe(vendedoras_df,hide_index=True,use_cotainer_width=True)
