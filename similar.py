import pandas as pd
from haversine import haversine
import warnings
warnings.filterwarnings("ignore")

def avaliar(dataset, num):
    '''
    dataset = dataframe
    num = numero da amostra 
    '''
    return dataset.loc[num]
    

def aval_localizacao(dataset, num):
    '''
    dataset = dataframe desejado
        num = numero da amostra
        retorna indice 0 latitude 
        indice 1 longitude
        '''

    return dataset.loc[num]['original_address_latitude'] , dataset.loc[num]['original_address_longitude']   

def haver(x, y, a=0, b=0):
    return haversine((a ,b), (x ,y))

def similar(dataset, raio, min, max, val_m2, lat_val, long_val):

  ''' dataset = dataframe desejado
      raio = raio de distancia EX:200 metros
      min valor do m2 com decrecimo percentual EX: m2 * 0.9
      max valor do m2 com acrescimo percentual EX: m2 * 1.10'''
  
  lista= []
  for i in range(dataset.shape[0]):
    lista.append(haver(lat_val, long_val, dataset['original_address_latitude'][i], dataset['original_address_longitude'][i]))
  dataset['dist'] = lista

  dataset['prox'] = dataset['dist'].apply(lambda x: 1 if x <=raio/1000 else 0)
  ok1 = dataset[dataset['prox']==1]
  Ranger = (dataset['sqrmeter_price_area_sale'] >=val_m2 * min) & \
          (dataset['sqrmeter_price_area_sale'] <=val_m2 * max)

  return ok1[Ranger].drop('prox', axis=1).sort_values(by='dist')

