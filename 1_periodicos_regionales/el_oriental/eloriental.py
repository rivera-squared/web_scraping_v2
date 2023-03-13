from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import re
# import os

def get_titulo(enlace):
    # enlace = 'http://periodicoeloriental.com/category/noticias/'
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//h3[@class="entry-title td-module-title"]/a/text()').extract()

def get_enlace(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//h3[@class="entry-title td-module-title"]/a/@href').extract()

def get_fecha(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="td-module-meta-info"]/span/time/text()').extract()

def get_autor(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="td-module-meta-info"]/span[@class="td-post-author-name"]/a/text()').extract()


def get_oriental_noticias():
    
    pages = range(1,11)
    
    titulo = []
    enlaces = []
    fecha = []
    autor = []
    
    for page in pages:
        link = 'http://periodicoeloriental.com/category/noticias/page/' + str(page)
        # print(link)
        fecha.append(get_fecha(link))
        titulo.append(get_titulo(link))
        autor.append(get_autor(link))
        enlaces.append(get_enlace(link))
        
    titulo = [x for sublist in titulo for x in sublist]    
    enlaces = [x for sublist in enlaces for x in sublist]
    fecha = [x for sublist in fecha for x in sublist]
    autor = [x for sublist in autor for x in sublist]
    
    oriental = pd.DataFrame({
        "fecha":fecha,
        "titulo":titulo,
        "autor(a)":autor,
        "categoria":"Noticias",
        "periodico":"El Oriental",
        "region":"Humacao",
        "enlace":enlaces
        })
    
    oriental['fecha'] = pd.to_datetime(oriental['fecha'])
    oriental = oriental.sort_values(by = 'fecha', ascending = False)
    oriental = oriental.drop_duplicates(subset = 'enlace')
    oriental = oriental[['fecha','titulo','autor(a)','categoria','periodico', 'region', 'enlace']]
    
    return oriental

def get_oriental_municipios():
    
    pages = range(1,11)
    
    titulo = []
    enlaces = []
    fecha = []
    autor = []
    
    for page in pages:
        link = 'http://periodicoeloriental.com/category/municipios/page/' + str(page)
        # print(link)
        fecha.append(get_fecha(link))
        titulo.append(get_titulo(link))
        autor.append(get_autor(link))
        enlaces.append(get_enlace(link))
        
    titulo = [x for sublist in titulo for x in sublist]    
    enlaces = [x for sublist in enlaces for x in sublist]
    fecha = [x for sublist in fecha for x in sublist]
    autor = [x for sublist in autor for x in sublist]
    
    oriental = pd.DataFrame({
        "fecha":fecha,
        "titulo":titulo,
        "autor(a)":autor,
        "categoria":"Municipios",
        "periodico":"El Oriental",
        "region":"Humacao",
        "enlace":enlaces
        })
    
    oriental['fecha'] = pd.to_datetime(oriental['fecha'])
    oriental = oriental.sort_values(by = 'fecha', ascending = False)
    oriental = oriental.drop_duplicates(subset = 'enlace')
    oriental = oriental[['fecha','titulo','autor(a)','categoria','periodico', 'region', 'enlace']]
    
    return oriental


before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("\nHora que comenzo a correr el algoritmo: {}".format(current_time))

oriental = pd.read_csv('eloriental.csv')
oriental['fecha'] = pd.to_datetime(oriental['fecha'])
oriental = oriental.sort_values(by = 'fecha', ascending = False)
antes = len(oriental)
print("Comenzo con {} articulos.".format(antes))

oriental_municipios = get_oriental_municipios()
oriental_noticias = get_oriental_noticias()

oriental = pd.concat([oriental_noticias, oriental_municipios])
oriental['fecha'] = pd.to_datetime(oriental['fecha'])
oriental = oriental.drop_duplicates(subset = 'enlace')
oriental = oriental.sort_values(by = 'fecha', ascending = False)
despues = len(oriental)

oriental.to_csv('eloriental.csv', index = False)

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que terminó de correr el algoritmo: {}".format(current_time1))

print("Termino con {} articulos.".format(despues))
print("{} Artículos añadidos luego de correr el algoritmo.".format(despues-antes))