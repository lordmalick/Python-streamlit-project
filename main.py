import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time
import numpy as np        
import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from datetime import timedelta
import pandas_datareader as pdr
from Historic_Crypto import HistoricalData
from Historic_Crypto import Cryptocurrencies
from Historic_Crypto import LiveCryptoData
from Historic_Crypto import Cryptocurrencies

st.set_page_config(
    page_title="Crypto App",
    page_icon="random",
    layout="wide",
   initial_sidebar_state="expanded",
        )


#---------------------------------#
# Titre


image = Image.open('app.jpg')

st.image(image, width = 700)


st.markdown(
    """
    <h1 style="text-align:center; font-size:50px;font-family: 'Times New Roman', Times, serif;color:#ff1493;">CRYPTOCURRENCY WEB APP</h1>
    
    """,
    unsafe_allow_html=True,
)
st.markdown("""
Top 100 des cryptomonnaies
* credit:**CoinMarketCap**!
""")
#---------------------------------#
# About
expander_bar = st.beta_expander("About")
expander_bar.markdown("""
* **Toute les tendances des derniers Moments**
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
* Le But de ce site web est uniquement d'afficher des informations concernant l'evolution des cryptomonnaies sur le marché.
 Il n'est pas destiné à offrir l'acces a l'un de ces produits ou services. [Binance](http://binance.com) Pour acceder à ces services.
""")


#---------------------------------#

col3 = st.sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 300px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 500px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
col2, col1 = st.beta_columns((3,2))

#---------------------------------#
# Sidebar + Main panel
col1.header('Options de Saisie')

currency_price_unit = col1.selectbox('Sélectionnez la devise pour le prix', ('USD', 'BTC', 'ETH'))

def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    return listings
   
def crypto_values():
    data=load_data()
    cpt_name=[]
    cpt_price=[]
    cpt_symbol=[]
    cpt_market_cap=[]
    
    for i in data:
       cpt_name.append(i['name'])
       cpt_price.append(i['quote'][currency_price_unit]['price'])
       cpt_symbol.append(i['symbol'])
       cpt_market_cap.append(i['quote'][currency_price_unit]['marketCap'])
    
    dataframe=pd.DataFrame(columns=['Nom','symbole','prix','Market cap'])
    dataframe['Nom']=cpt_name
    dataframe['symbole']=cpt_symbol
    dataframe['prix']=cpt_price
    dataframe['Market cap']=cpt_market_cap
    return dataframe

def crypto_percent_change():
  data=load_data()
  cpt_percent_change_24h=[]
  cpt_percent_change_7d=[]
  cpt_percent_change_30d=[]
  cpt_percent_change_60d=[]  
  cpt_percent_change_90d=[]
  cpt_name=[]


  for i in data:
     cpt_percent_change_24h.append(i['quote'][currency_price_unit]['percentChange24h'])
     cpt_percent_change_7d.append(i['quote'][currency_price_unit]['percentChange7d'])
     cpt_percent_change_30d.append(i['quote'][currency_price_unit]['percentChange30d'])
     cpt_percent_change_60d.append(i['quote'][currency_price_unit]['percentChange60d']) 
     cpt_percent_change_90d.append(i['quote'][currency_price_unit]['percentChange90d'])
     cpt_name.append(i['name'])
 
  
     
  dataframe=pd.DataFrame(columns=['Nom','percent_24h','percent_7jours','percent_Mois','percent_2mois','percent_3mois'])
  dataframe['Nom']=cpt_name
  dataframe['percent_24h']=cpt_percent_change_24h
  dataframe['percent_7jours']=cpt_percent_change_7d
  dataframe['percent_Mois']=cpt_percent_change_30d
  dataframe['percent_2mois']=cpt_percent_change_60d
  dataframe['percent_3mois']=cpt_percent_change_90d
  return dataframe  


def getData(cryptocurrency):
  
    now = datetime.now()
    en = str(now.strftime("%Y-%m-%d-%H-%M"))
    start = str((now - timedelta(days=365)).strftime("%Y-%m-%d-%H-%M"))
    data = HistoricalData(cryptocurrency+'-USD', 86400, '2021-01-01-00-00', en).retrieve_data()
    

    return data

df=crypto_values()
sorted_coin = sorted( df['symbole'] )
num_coin = col1.slider('liste Cryptomonnaies à afficher (limite 100)', 1, 100, 100)
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)
df_selected_coin = df[df['symbole'].isin(selected_coin)]
df_coins = df_selected_coin[:num_coin]




df1=crypto_percent_change()
col2.subheader('Toutes les valeurs en **'+currency_price_unit+'**')
col2.dataframe(df_coins,height=768)
col2.subheader('les Taux d\' evolution')
col2.dataframe(df1[:num_coin],height=900)
col2.markdown(
    """
    <br>
    """, unsafe_allow_html=True
)
col2.markdown("""
<h2> Graphiques avancés de crypto-monnaie.</h2> 
 <span>Affichez les données de crypto-monnaie et comparez-les à d'autres cryptos, actions et bourses. from the <a href="http://coinmarketcap.com">CoinMarketCap</a></span>
""",
unsafe_allow_html=True
)

CURRENCY = 'USD'
sym=st.selectbox('Symbole',df['symbole'])
CRYPTO =sym
df2=getData(CRYPTO)
st.subheader('**Line Chart**:Evoluton des Prix')
st.line_chart(df2['close'])
# Sidebar - Taux de Change

col3.subheader(' % Taux de Change')
percent_timeframe = col3.radio('',['24h','7d', 'Mois'])
percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]


#   diagrammetaux de change
df_change = pd.concat([df_coins.symbole, df1.percent_24h,df1.percent_7jours,df1.percent_Mois], axis=1)
df_change = df_change.set_index('symbole')

if percent_timeframe == '7d':
    df_change = df_change.sort_values(by=['percent_7jours'])
    col3.write('*perriode de 7 jours*')
    plt.figure(figsize=(6,14))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_7jours'].plot(kind='barh', color=(df_change['percent_7jours']>0).map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == '24h':
    df_change = df_change.sort_values(by=['percent_24h'])
    col3.write('*periode de 24h*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_24h'].plot(kind='barh', color=(df_change['percent_24h']>0).map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
else:
    df_change = df_change.sort_values(by=['percent_Mois'])
    col3.write('*periode d\'un mois*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_Mois'].plot(kind='barh', color=(df_change['percent_Mois']>0).map({True: 'g', False: 'r'}))
    col3.pyplot(plt)

from cryptocmd import CmcScraper
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
symbole_select=""
smb=[]
for i in df['symbole']:
    smb.append(i)

symbole_select = st.sidebar.selectbox("Selectionner un symbole de cryptomonnaie (i.e. BTC, ETH, LINK, etc.)", smb)
@st.cache
def load_data(selected_ticker):
	init_scraper = CmcScraper(symbole_select)
	df = init_scraper.get_dataframe()
	return df

### chargement des données
data_load_state = st.sidebar.text('chargement...')
df = load_data(symbole_select)
data_load_state.text('chargement... terminé!')    

data = df
### Apperçue des dernieres tendances
st.subheader('Overview')
st.write(data)

### les tracés réguliers (Données brutes)
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
	fig.layout.update(title_text='Données de séries temporelles avec Rangeslider', xaxis_rangeslider_visible=True, width=900,height=500)
	st.plotly_chart(fig)

def plot_raw_data_log():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
	fig.update_yaxes(type="log")
	fig.layout.update(title_text='Données de séries temporelles avec Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
###checkbox
select = st.checkbox(" Tracer à l'echelle Logarithmique")
if select:
	plot_raw_data_log()
else:
	plot_raw_data()

st.markdown("""
<h2> Prediction des futures evolutions des crypto-monnaies.</h2> 
 <span>Dans cette section vous pouvez obtenir les prochaines tendances de l'evolution des crypto-monnaies.
       Cependant notez qu'il puisse y avoir une marge avec les vraies valeurs en temps réel.
       L'exactitude des valeurs n'est donc pas garanties.</span>
""",
unsafe_allow_html=True
)
st.markdown("""<br>""",
unsafe_allow_html=True
)
###prediction
if st.button("Predire"):

	### data
	df_train = data[['Date','Close']]
	df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

	### Create Prophet model
	m = Prophet(
		changepoint_range=0.8, 
		yearly_seasonality='auto', 
		weekly_seasonality='auto', 
		daily_seasonality=False, 
		seasonality_mode='multiplicative' 
	)
	
	m.fit(df_train)
  
	### Predict using the model
	future = m.make_future_dataframe(periods=365)
	previsions = m.predict(future)

	### Show and plot forecast
	st.subheader('Données de prévision')
	st.write(previsions.head())
	    
	st.subheader(f'Données de prévision pour 365 jours')
	fig1 = plot_plotly(m, previsions)
	if select:
		fig1.update_yaxes(type="log")
	st.plotly_chart(fig1)

	st.subheader("Composants de prévision")
	fig2 = m.plot_components(previsions)
	st.write(fig2)
