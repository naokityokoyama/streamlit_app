import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import sys
sys.path.append('C:/Users/User/Documents/jobs/projeto_out/scripts')
from similar import *

st.title('Teste Similaridade')
df = pd.read_csv('C:/Users/User/Documents/jobs/projeto_out/datasets/base_nit.csv')

raio = [200,300,400,500]
min_ = [0.80, 0.85, 0.90, 0.95]
max_ = [1.05, 1.10, 1.15, 1.20]

st.sidebar.header('Filtros')
selecione_amostra = st.sidebar.selectbox('Selecione Amostra', range(0,200))

amostra = df.loc[selecione_amostra]
lat_amostra  = amostra['original_address_latitude']
long_amostra = amostra['original_address_longitude']
m2_amostra = amostra['sqrmeter_price_area_sale']

selecione_raio = st.sidebar.selectbox('Selecione Raio', raio)
selecione_min = st.sidebar.selectbox('Selecione Minimo', min_)
selecione_max = st.sidebar.selectbox('Selecione Maximo', max_)

data = similar(df, selecione_raio, selecione_min, selecione_max, m2_amostra, lat_amostra, long_amostra)
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



