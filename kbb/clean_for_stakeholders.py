import pandas as pd


data = pd.read_json('./data/data.json')

data['model_year'] = data['title'].apply(lambda x: x[x.find('20'):x.find('20')+4])
data['make'] = data['title'].apply(lambda x: x[x.find('20')+5:].split(' ')[0])
data['model'] = data['title'].apply(lambda x: ' '.join(x[x.find('20')+5:].split(' ')[1:]))
data.drop('title', axis=1, inplace=True)
data = data[['list_date', 'model_year', 'price', 'vin', 'make','model' ,'mileage','state']]

data.to_csv('./data/data.csv',index=False)
