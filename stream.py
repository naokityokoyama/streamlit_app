import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

from similar import *

st.title('Teste Similaridade')
df = pd.read_csv('base_nit.csv')

query = (df['features_bedroom']==0) & \
        (df['features_bathroom']==0)
df = df.drop(df[query].index).reset_index(drop=True)    

similaridade = [0.5, 0.1, 0.2, 0.3, 0.4, 1, 1.5]

st.sidebar.header('Filtros')
selecione_amostra = st.sidebar.selectbox('Selecione Amostra (amostra selecionada leva em consideração (localização,  \
        numero de quartos e numero de vagas))', range(0,200))

selecione_similaridade = st.sidebar.selectbox('Selecione Similaridade - Menor mais Similar', similaridade)

data = similar(df, selecione_amostra, similar=selecione_similaridade)
#checkbox
carregar_dados = st.sidebar.checkbox('Carregar dados')

if carregar_dados:
        st.subheader('Dados')
        dados=st.dataframe(data)

#st.dataframe(data)

map = folium.Map(location=[df['original_address_latitude'].mean(), df['original_address_longitude'].mean()],defaul_zoom_start=10)
make_cluster = MarkerCluster().add_to(map)

for index, row in data.iterrows():
    folium.Marker([row['original_address_latitude'], row['original_address_longitude']], 
    popup='Preço R$ {0}, Metragem {1}, Quartos {2}'.format(
        row['transaction_sale'], row['total_area'], row['features_bedroom'])).add_to(make_cluster)
    
folium_static(map)    



