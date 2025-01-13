import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from auxiliar.auxiliar import *
import plotly.express as px

st.set_page_config(page_title="Pró-Corpo - Visualizar Vendas", page_icon="💎",layout="wide")

projection = {"payment_method": 1, "amount": 1, "date": 1,"created_by":1,"_id": 0}
billcharges_df = get_dataframe_from_mongodb(collection_name="billcharges_db", database_name="dash_midia", projection=projection)

filtro_pagamento = ['Utilizar Crédito','Crédito Promocional','Vale Tratamento','Credito CRMBonus']
billcharges_df = billcharges_df.loc[~billcharges_df["payment_method"].isin(filtro_pagamento)]

filtro_avista = ['PIX','Cartão de Crédito à Vista','Dinheiro','Cartão de Crédito Vindi à Vista',
    'Cartão de Crédito à Vista (Link)', 'Transferência Bancária']

billcharges_df["amount"] = billcharges_df["amount"]/100
billcharges_df['date'] = pd.to_datetime(billcharges_df['date'])
billcharges_df['formatted_date'] = billcharges_df['date'].dt.to_period('D')
billcharges_df['period'] = billcharges_df['date'].dt.to_period('M')
billcharges_df['avista'] = billcharges_df.apply(lambda row: row['amount'] if row['payment_method'] in filtro_avista else 0, axis=1)

st.title("Resumo do Mês por Vendedora")

meses = sorted(billcharges_df["period"].unique(),reverse=True)

seletor_mes = st.selectbox("Selecione um mês", meses)
billcharges_filtered_df = billcharges_df.loc[billcharges_df["period"] == seletor_mes]

groupby_vendedora = billcharges_filtered_df.groupby(['created_by']).agg({'amount': 'sum', 'avista': 'sum'}).reset_index()

column_config ={
                "amount": st.column_config.NumberColumn(
                "Valor Total",
                format="R$%.2f",
                  ),
                "avista": st.column_config.NumberColumn(
                "Valor à Vista",
                format="R$%.2f",
                ),
                'created_by': 'nome_vendedora'
              }

st.dataframe(groupby_vendedora,use_container_width=True,hide_index=True,column_config=column_config)
