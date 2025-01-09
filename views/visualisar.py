import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from auxiliar.auxiliar import *
import plotly.express as px

st.set_page_config(page_title="Pró-Corpo - Visualizar Vendas", page_icon="💎",layout="wide")

vendedoras_df = get_dataframe_from_mongodb(collection_name="dados_vendedoras", database_name="rpd_db")
billcharges_df = get_dataframe_from_mongodb(collection_name="billcharges_db", database_name="dash_midia")

filtro_pagamento = ['Utilizar Crédito','Crédito Promocional','Vale Tratamento','Credito CRMBonus']
billcharges_df = billcharges_df.loc[~billcharges_df["payment_method"].isin(filtro_pagamento)]

filtro_avista = ['PIX','Cartão de Crédito à Vista','Dinheiro','Cartão de Crédito Vindi à Vista',
    'Cartão de Crédito à Vista (Link)', 'Transferência Bancária']

billcharges_df["amount"] = billcharges_df["amount"]/100
billcharges_df["due_at"] = pd.to_datetime(billcharges_df['due_at'], format="%Y-%m-%d %H:%M:%S").dt.strftime("%Y-%m-%d")
billcharges_df['due_at'] = pd.to_datetime(billcharges_df['due_at'])
billcharges_df['date'] = pd.to_datetime(billcharges_df['date'])
billcharges_df['formatted_date'] = billcharges_df['date'].dt.to_period('D')
billcharges_df['period'] = billcharges_df['date'].dt.to_period('M')
billcharges_df['avista'] = billcharges_df.apply(lambda row: row['amount'] if row['payment_method'] in filtro_avista else 0, axis=1)
billcharges_df["quote_id"] = billcharges_df["quote_id"].astype(str)
billcharges_df["customer_id"] = billcharges_df["customer_id"].astype(str)

st.title("Resumo do Mês por Vendedora")

meses = sorted(billcharges_df["period"].unique(),reverse=True)

seletor_mes = st.selectbox("Selecione um mês", meses)
billcharges_filtered_df = billcharges_df.loc[billcharges_df["period"] == seletor_mes]

groupby_vendedora = billcharges_filtered_df.groupby(['created_by']).agg({'amount': 'sum', 'avista': 'sum'}).reset_index()

st.dataframe(groupby_vendedora)

# column_config ={
#                 "amount": st.column_config.NumberColumn(
#                 "Valor Total",
#                 format="R$%.2f",
#                   ),
#                 "avista": st.column_config.NumberColumn(
#                 "Valor à Vista",
#                 format="R$%.2f",
#                 )
#               }

# st.subheader("Resumo do Dia")

# dias_seletor = billcharges_df["formatted_date"].sort_values(ascending=False).unique()
# seletor_dia = st.selectbox("Selecione um dia", dias_seletor)

# resumo_1, resumo_2 = st.columns([3,1])

# billcharges_df_dia = billcharges_df.loc[billcharges_df["formatted_date"] == seletor_dia]
# groupby_quote_dia = billcharges_df_dia.groupby(['quote_id','customer_id','customer_name','customer_email']).agg({'amount': 'sum', 'avista': 'sum'}).reset_index()

# with resumo_1:

#   st.dataframe(groupby_quote_dia,hide_index=True,use_container_width=True,column_config=column_config)

# with resumo_2:
#   total_sales_dia = groupby_quote_dia["amount"].sum()
#   total_avista_dia = groupby_quote_dia["avista"].sum()
#   total_vendas_dia = groupby_quote_dia["quote_id"].count()

#   st.metric(label="Quantidade de vendas", value=total_vendas_dia)
#   st.metric(label="Vendas Total (R$)", value=f"R$ {total_sales_dia:,.2f}")
#   st.metric(label="Vendas à vista (R$)", value=f"R$ {total_avista_dia:,.2f}")
