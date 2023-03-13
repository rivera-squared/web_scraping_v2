from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import re
# import os

def get_title(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="T5UMT5 WD_8WI post-title blog-hover-container-element-color blog-post-category-title-color blog-post-category-title-font _wPn3X"]/p/text()').extract()

def get_enlace(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="JMCi2v blog-post-category-link-hashtag-hover-color so9KdE TBrkhx I5nSmk"]/a/@href').extract()

def get_autor(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="dZs5e3 htMcyB"]/span/span/@title').extract()

def fix_date(date):
    """
    Modifica el formato de fecha (str de fecha como argumento) para poder luego convertir la fecha en str a formato datetime.
    """

    if ('ene' in date) == True:
        return date.replace('ene','jan')
    if ('feb' in date) == True:
        return date.replace('feb','feb')
    if ('mar' in date) == True:
        return date.replace('mar','mar')
    if ('abr' in date) == True:
        return date.replace('abr','apr')
    if ('may' in date) == True:
        return date.replace('may','may')
    if ('jun' in date) == True:
        return date.replace('jun','jun')
    if ('jul' in date) == True:
        return date.replace('jul','jul')
    if ('ago' in date) == True:
        return date.replace('ago','aug')
    if ('sep' in date) == True:
        return date.replace('sep','sep')
    if ('oct' in date) == True:
        return date.replace('oct','oct')
    if ('nov' in date) == True:
        return date.replace('nov','nov')
    if ('dic' in date) == True:
        return date.replace('dic','dec')   

def get_fecha(enlace):
    
    sel=Selector(text=requests.get(enlace).content)
    fecha = sel.xpath('//li[@class="UZa2Xr"]/span/text()').extract()[0]
    return fecha

def fix_fecha(fecha, year = 2023):
    if ('hace' in fecha) == False:
        a = fix_date(fecha)
        b = re.sub(" ", '/', a)
        c = b + "/" + str(year)
        return pd.to_datetime(c, dayfirst=True)
    else:
        return np.nan
    
def get_semana_locales():
    pages = range(1, 11)
    title = []
    links = []
    authors = []
    
    for page in pages:
        
        link = 'https://www.lasemanapr.com/noticias/categories/locales/page/' + str(page)
        title.append(get_title(link))
        links.append(get_enlace(link))
        authors.append(get_autor(link))
        
    titulo = [x for sublist in title for x in sublist]
    enlace = [x for sublist in links for x in sublist]
    autor = [x for sublist in authors for x in sublist]    
    
    semana_locales = pd.DataFrame({
        "titulo":titulo,
        "enlace":enlace,
        "autor(a)": autor,
        "categoria": "Locales",
        "periodico": "La Semana",
        "region":"Caguas"
        })
    
    semana_locales['fecha'] = semana_locales['enlace'].apply(get_fecha)
    semana_locales['fecha'] = semana_locales['fecha'].apply(fix_fecha)
    semana_locales = semana_locales[['fecha','titulo','autor(a)','categoria','periodico', 'region', 'enlace']]
    semana_locales = semana_locales.sort_values(by = 'fecha', ascending = False)
    return semana_locales

def get_semana_municipales():
    pages = range(1, 11)
    title = []
    links = []
    authors = []
    
    for page in pages:
        
        link = 'https://www.lasemanapr.com/noticias/categories/municipales/page/' + str(page)
        title.append(get_title(link))
        links.append(get_enlace(link))
        authors.append(get_autor(link))
        
    titulo = [x for sublist in title for x in sublist]
    enlace = [x for sublist in links for x in sublist]
    autor = [x for sublist in authors for x in sublist]    
    
    semana_municipales = pd.DataFrame({
        "titulo":titulo,
        "enlace":enlace,
        "autor(a)": autor,
        "categoria": "municipales",
        "periodico": "La Semana",
        "region":"Caguas"
        })
    
    semana_municipales['fecha'] = semana_municipales['enlace'].apply(get_fecha)
    semana_municipales['fecha'] = semana_municipales['fecha'].apply(fix_fecha)
    semana_municipales = semana_municipales[['fecha','titulo','autor(a)','categoria','periodico', 'region', 'enlace']]
    semana_municipales = semana_municipales.sort_values(by = 'fecha', ascending = False)
    return semana_municipales

def get_semana_seguridad():
    pages = range(1, 6)
    title = []
    links = []
    authors = []
    
    for page in pages:
        
        link = 'https://www.lasemanapr.com/noticias/categories/seguridad/page/' + str(page)
        title.append(get_title(link))
        links.append(get_enlace(link))
        authors.append(get_autor(link))
        
    titulo = [x for sublist in title for x in sublist]
    enlace = [x for sublist in links for x in sublist]
    autor = [x for sublist in authors for x in sublist]    
    
    semana_seguridad = pd.DataFrame({
        "titulo":titulo,
        "enlace":enlace,
        "autor(a)": autor,
        "categoria": "seguridad",
        "periodico": "La Semana",
        "region":"Caguas"
        })
    
    semana_seguridad['fecha'] = semana_seguridad['enlace'].apply(get_fecha)
    semana_seguridad['fecha'] = semana_seguridad['fecha'].apply(fix_fecha)
    semana_seguridad = semana_seguridad[['fecha','titulo','autor(a)','categoria','periodico', 'region', 'enlace']]
    semana_seguridad = semana_seguridad.sort_values(by = 'fecha', ascending = False)
    return semana_seguridad

before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("\nHora que comenzo a correr el algoritmo: {}".format(current_time))

semana = pd.read_csv('semana.csv')
semana['fecha'] = pd.to_datetime(semana['fecha'])
semana = semana.sort_values(by ='fecha', ascending = False)
antes = len(semana)
print("Comenzo con {} articulos.".format(antes))

semana_locales = get_semana_locales()
semana_municipales = get_semana_municipales()
semana_seguridad = get_semana_seguridad()

semana = pd.concat([semana, semana_locales, semana_municipales, semana_seguridad])
semana = pd.to_datetime(semana['fecha'])
semana = semana.sort_values(by = 'fecha', ascending = False)
semana =  semana.drop_duplicates(subset = 'enlace')
despues = len(semana)


semana.to_csv('semana.csv', index = False)

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que terminó de correr el algoritmo: {}".format(current_time1))

print("Termino con {} articulos.".format(despues))
print("{} Artículos añadidos luego de correr el algoritmo.\n".format(despues-antes))