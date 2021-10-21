import pandas as pd
from haversine import haversine
from sklearn.metrics.pairwise import euclidean_distances, haversine_distances, manhattan_distances
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings
warnings.filterwarnings("ignore")

def haver(dataset, num):
    lista_haver = []
    distancia1 = [dataset.loc[num]['original_address_latitude'], dataset.loc[num]['original_address_longitude']]
    
    for i in range(dataset.shape[0]):
        lista_haver.append(haversine(distancia1, (dataset.loc[i]['original_address_latitude'], dataset.loc[i]['original_address_longitude'])))
    return lista_haver  

def euclidian(dataset, num):
    lista_euclidiana = []
    id = dataset.index
    min = MinMaxScaler()
    dataset = min.fit_transform(dataset)
    dataset = pd.DataFrame(dataset).set_index(id)
    for index, row in dataset.iterrows():
        X = dataset.loc[num]
        lista_euclidiana.append(euclidean_distances([X],[row.values]))
    lista_euclidiana_ = [x[0][0].round(2) for x in lista_euclidiana] 
    return lista_euclidiana_

def manhattan(dataset, num):
    lista_manhattan = []
    for index, row in dataset.iterrows():
        X = dataset.loc[num]
        lista_manhattan.append(manhattan_distances([X],[row.values]))
    lista_manhattan_ = [x[0][0].round(2) for x in lista_manhattan] 
    return lista_manhattan_

def similar(dataset , num, s=None, raio=200, similar=0.5):
    '''  
        dataset = dataset a ser pesquisado,
        num = amostra,
        s=None retorna dataset completo s=1 retorna dataset somente com a distancia,
        raio = 200 default,
        similar = 0.5 default,
    '''
    lista_haver = haver(dataset, num)

    dataset['haver'] = lista_haver
    query = dataset['haver']<= raio/800
    data = dataset[query][['features_bedroom', 'total_area', 'features_garage', 'haver']]
    
    if s == 1:
        return data
    else:    
        data['id1'] = euclidian(data, num)
        dataset = dataset.loc[data.index]
        dataset['id1'] = data['id1']
        
        data['id2'] = manhattan(data, num)
        dataset = dataset.loc[data.index]
        dataset['id2'] = data['id2']
        return dataset[dataset['id1']<=similar].sort_values(by='id1')    