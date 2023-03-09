from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime
import re


def clean_fecha(fecha):
	
    x=re.sub('\w+:\s', '', str(fecha)).strip()
    y=re.sub('\s\d+:\d+\s\w+','',x).strip()
    time = pd.to_datetime(y)
    
    return time

def get_autor(enlace):
    
    sel=Selector(text=requests.get(enlace).content)
    return ''.join(sel.xpath('//div[@class="por"]/a/text()').extract())

def get_categoria(enlace):
    
    x = re.sub('(https://www.noticel.com/)','', enlace)
    y = re.sub('/\S+','',x)
    categoria=y.title()
    return categoria

def get_noticel():
    
    enlace = 'https://www.noticel.com/'
    sel=Selector(text=requests.get(enlace).content)
    title=sel.xpath('//div[@class="entry-title"]/a/h2[@class="teaser__headline"]/span[@class="teaser__headline-marker"]/text()').extract()
    date=sel.xpath('//div[@class="teaser-content image col-md-8"]/div[@class="teaser-article-date"]/div[@class="teaser-article-pubdate"]/text()').extract()
    link=sel.xpath('//div[@class="entry-title"]/a/@href').extract()
    noticel_dict = {'fecha':date,
                    'titulo':title,
                    'enlace':link}
    noticel = pd.DataFrame(noticel_dict)
    
    date=[]
    for fecha in noticel['fecha']:
        date.append(clean_fecha(fecha))
    
    autor=[]
    categoria=[]
    for enlace in noticel['enlace']:
        autor.append(get_autor(enlace))
        categoria.append(get_categoria(enlace))
        
    noticel['fecha'] = date
    noticel['autor'] = autor
    noticel['categoria'] = categoria
    
    noticel = noticel[['fecha','titulo','autor','categoria','enlace']]
    noticel = noticel.sort_values(by='fecha', ascending = False)

    return noticel
    
before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("Hora que comenzó a correr el algoritmo: {}".format(current_time))

noticel = pd.read_csv('noticel.csv')
noticel['fecha'] = pd.to_datetime(noticel['fecha'])
antes = len(noticel)
print("\nComenzo con {} articulos.".format(antes))
noticel_new=get_noticel()
noticel = pd.concat([noticel_new, noticel])
noticel = noticel.drop_duplicates(subset = 'enlace')
despues = len(noticel)

noticel.to_csv('noticel.csv', index=False)

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que terminó de correr el algoritmo: {}".format(current_time1))

print("Termino con {} articulos.".format(despues))
print("{} Artículos añadidos luego de correr el algoritmo.".format(despues-antes))