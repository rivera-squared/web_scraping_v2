from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime
import re

def get_title():
    enlace = 'https://www.noticel.com/mundo/'
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="entry-title"]/a/h2/span/text()').extract()

def get_enlace():
    enlace = 'https://www.noticel.com/mundo/'
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="entry-title"]/a/@href').extract()

def get_fecha():
    enlace = 'https://www.noticel.com/mundo/'
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="teaser-article-pubdate"]/text()').extract()

def clean_fecha(fecha):
    x=re.sub('\w+:\s', '', str(fecha)).strip()
    y=re.sub('\s\d+:\d+\s\w+','',x).strip()
    time = pd.to_datetime(y)
    return time

def get_autor(enlace):
    
    sel=Selector(text=requests.get(enlace).content)
    return ''.join(sel.xpath('//div[@class="por"]/a/text()').extract())

def get_noticel_mundo():
    fecha = get_fecha()
    titulo = get_title()
    enlace = get_enlace()
    
    noticel_mundo = pd.DataFrame({
        "fecha":fecha,
        "titulo":titulo,
        "enlace":enlace,
        "categoria":"Mundo"
        })
    
    noticel_mundo['fecha']= noticel_mundo['fecha'].apply(clean_fecha)
    noticel_mundo['autor(a)'] = noticel_mundo['enlace'].apply(get_autor)
    
    noticel_mundo = noticel_mundo[['fecha','titulo','autor(a)', 'categoria','enlace']]
    
    return noticel_mundo


before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("\nHora que comenzó a correr el algoritmo: {}".format(current_time))

noticel = pd.read_csv('noticel_mundo.csv')
noticel['fecha'] = pd.to_datetime(noticel['fecha'])
antes = len(noticel)
print("\nComenzo con {} articulos.".format(antes))

noticel_new=get_noticel_mundo()
noticel = pd.concat([noticel_new, noticel])
noticel = noticel.drop_duplicates(subset = 'enlace')
despues = len(noticel)

noticel.to_csv('noticel.csv', index=False)

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que terminó de correr el algoritmo: {}".format(current_time1))

print("Termino con {} articulos.".format(despues))
print("{} Artículos añadidos luego de correr el algoritmo.".format(despues-antes))