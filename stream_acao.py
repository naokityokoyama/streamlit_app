
import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go

dt_start = datetime.today() - timedelta(days=30)
dt_end = datetime.today()
intervals = ['Daily', 'Weekly', 'Monthly']
countries = ['brazil', 'united states']
acoes = ip.get_stocks_list(country='brazil')

@st.cache
def consulta_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(stock=stock, 
                                country=country,
                                from_date=from_date,
                                to_date=to_date,
                                interval=interval)
    return df  

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)       

def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x':df.index,
        'open': df.Open,
        'close':df.Close, 
        'high': df.High, 
        'low': df.Low, 
        'type' : 'candlestick',
        'name': acao, 
        'showlegend': False
            }
    data = [trace1]
    layout = go.Layout()
    fig = go.Figure(data=data, layout=layout)
    return fig   

#criando barra lateral

country_select = st.sidebar.selectbox('Selecione o pais', countries)     
acoes= ip.get_stocks_list(country=country_select)              

acao_select = st.sidebar.selectbox('Selecione o ativo', acoes)   

#data
from_date = st.sidebar.date_input('De:', dt_start)
to_date = st.sidebar.date_input('Para:', dt_end)

#interval
interval_select = st.sidebar.selectbox("Selecione o intervalo", intervals)

#checkbox
carregar_dados = st.sidebar.checkbox('Carregar dados')

st.title('Stock Monitor') #h1
st.header('Acões') #h2
st.subheader('Visualização Grafica') #h3

if from_date > to_date:
    st.sidebar.error('A data inicial é maior que a final')

else:
    df = consulta_acao(acao_select, country_select, format_date(from_date), format_date(to_date), interval_select) 

#grafico
    try:
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_line = st.line_chart(df.Close)

        #usando o checkbox
        if carregar_dados:
            st.subheader('Dados')
            dados=st.dataframe(df)

    except Exception as e:
        st.error(e)            
