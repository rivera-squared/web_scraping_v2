from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import re


def get_titulo(enlace):
    # enlace = 'https://puertoricoposts.com/category/gobierno/'
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//h3[@class="jeg_post_title"]/a/text()').extract()

def get_enlace(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//h3[@class="jeg_post_title"]/a/@href').extract()

def get_autor(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="jeg_meta_author"]/a/text()').extract()

def get_fecha(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="jeg_meta_date"]/a/text()').extract()

def fix_date(date):
    """
    Modifica el formato de fecha (str de fecha como argumento) para poder luego convertir la fecha en str a formato datetime.
    """

    if ('enero' in date) == True:
        return date.replace('enero','jan')
    if ('febrero' in date) == True:
        return date.replace('febrero','feb')
    if ('marzo' in date) == True:
        return date.replace('marzo','mar')
    if ('abril' in date) == True:
        return date.replace('abril','apr')
    if ('mayo' in date) == True:
        return date.replace('mayo','may')
    if ('junio' in date) == True:
        return date.replace('junio','jun')
    if ('julio' in date) == True:
        return date.replace('julio','jul')
    if ('agosto' in date) == True:
        return date.replace('agosto','aug')
    if ('septiembre' in date) == True:
        return date.replace('septiembre','sep')
    if ('octubre' in date) == True:
        return date.replace('octubre','oct')
    if ('noviembre' in date) == True:
        return date.replace('noviembre','nov')
    if ('diciembre' in date) == True:
        return date.replace('diciembre','dec')  
    
def fix_fecha(fecha):
    fecha = fecha.strip()
    fecha = fix_date(fecha)
    return pd.to_datetime(fecha)

def get_prposts_gobierno():
    pages = range(1,6)
    titulo = []
    enlaces = []
    autor = []
    fecha = []
    for page in pages:
        enlace = 'https://puertoricoposts.com/category/gobierno/page/' + str(page)
        
        titulo.append(get_titulo(enlace))
        enlaces.append(get_enlace(enlace))
        autor.append(get_autor(enlace))
        fecha.append(get_fecha(enlace))
        
    titulo = [x for sublist in titulo for x in sublist] 
    enlaces = [x for sublist in enlaces for x in sublist]
    autor = [x for sublist in autor for x in sublist]
    fecha = [x for sublist in fecha for x in sublist]
    
    prposts_gobierno = pd.DataFrame({
        "fecha":fecha,
        "titulo":titulo,
        "autor(a)":autor,
        "categoria":"Gobierno",
        "periodico":"Puerto Rico Posts",
        "region": "Juncos",
        "enlace":enlaces
        })
    
    prposts_gobierno['fecha'] = prposts_gobierno['fecha'].apply(fix_fecha)
    prposts_gobierno['fecha'] = pd.to_datetime(prposts_gobierno['fecha'])
    prposts_gobierno = prposts_gobierno.sort_values(by = 'fecha', ascending = False)
    prposts_gobierno = prposts_gobierno[['fecha','titulo','autor(a)','categoria','periodico', 'region', 'enlace']]
    
    return prposts_gobierno

def get_prposts_locales():
    pages = range(1,6)
    titulo = []
    enlaces = []
    autor = []
    fecha = []
    for page in pages:
        enlace = 'https://puertoricoposts.com/category/locales/page/' + str(page)
        
        titulo.append(get_titulo(enlace))
        enlaces.append(get_enlace(enlace))
        autor.append(get_autor(enlace))
        fecha.append(get_fecha(enlace))
        
    titulo = [x for sublist in titulo for x in sublist] 
    enlaces = [x for sublist in enlaces for x in sublist]
    autor = [x for sublist in autor for x in sublist]
    fecha = [x for sublist in fecha for x in sublist]
    
    prposts_locales = pd.DataFrame({
        "fecha":fecha,
        "titulo":titulo,
        "autor(a)":autor,
        "categoria":"Locales",
        "periodico":"Puerto Rico Posts",
        "region": "Juncos",
        "enlace":enlaces
        })
    
    prposts_locales['fecha'] = prposts_locales['fecha'].apply(fix_fecha)
    prposts_locales['fecha'] = pd.to_datetime(prposts_locales['fecha'])
    prposts_locales = prposts_locales.sort_values(by = 'fecha', ascending = False)
    prposts_locales = prposts_locales[['fecha','titulo','autor(a)','categoria','periodico', 'region', 'enlace']]
    
    return prposts_locales

def get_prposts_seguridad():
    pages = range(1,6)
    titulo = []
    enlaces = []
    autor = []
    fecha = []
    for page in pages:
        enlace = 'https://puertoricoposts.com/category/seguridad/page/' + str(page)
        
        titulo.append(get_titulo(enlace))
        enlaces.append(get_enlace(enlace))
        autor.append(get_autor(enlace))
        fecha.append(get_fecha(enlace))
        
    titulo = [x for sublist in titulo for x in sublist] 
    enlaces = [x for sublist in enlaces for x in sublist]
    autor = [x for sublist in autor for x in sublist]
    fecha = [x for sublist in fecha for x in sublist]
    
    prposts_seguridad = pd.DataFrame({
        "fecha":fecha,
        "titulo":titulo,
        "autor(a)":autor,
        "categoria":"seguridad",
        "periodico":"Puerto Rico Posts",
        "region": "Juncos",
        "enlace":enlaces
        })
    
    prposts_seguridad['fecha'] = prposts_seguridad['fecha'].apply(fix_fecha)
    prposts_seguridad['fecha'] = pd.to_datetime(prposts_seguridad['fecha'])
    prposts_seguridad = prposts_seguridad.sort_values(by = 'fecha', ascending = False)
    prposts_seguridad = prposts_seguridad[['fecha','titulo','autor(a)','categoria','periodico', 'region', 'enlace']]
    
    return prposts_seguridad

def get_prposts_educacion():
    pages = range(1,6)
    titulo = []
    enlaces = []
    autor = []
    fecha = []
    for page in pages:
        enlace = 'https://puertoricoposts.com/category/educacion/page/' + str(page)
        
        titulo.append(get_titulo(enlace))
        enlaces.append(get_enlace(enlace))
        autor.append(get_autor(enlace))
        fecha.append(get_fecha(enlace))
        
    titulo = [x for sublist in titulo for x in sublist] 
    enlaces = [x for sublist in enlaces for x in sublist]
    autor = [x for sublist in autor for x in sublist]
    fecha = [x for sublist in fecha for x in sublist]
    
    prposts_educacion = pd.DataFrame({
        "fecha":fecha,
        "titulo":titulo,
        "autor(a)":autor,
        "categoria":"educacion",
        "periodico":"Puerto Rico Posts",
        "region": "Juncos",
        "enlace":enlaces
        })
    
    prposts_educacion['fecha'] = prposts_educacion['fecha'].apply(fix_fecha)
    prposts_educacion['fecha'] = pd.to_datetime(prposts_educacion['fecha'])
    prposts_educacion = prposts_educacion.sort_values(by = 'fecha', ascending = False)
    prposts_educacion = prposts_educacion[['fecha','titulo','autor(a)','categoria','periodico', 'region', 'enlace']]
    
    return prposts_educacion

def get_prposts_salud():
    pages = range(1,6)
    titulo = []
    enlaces = []
    autor = []
    fecha = []
    for page in pages:
        enlace = 'https://puertoricoposts.com/category/salud/page/' + str(page)
        
        titulo.append(get_titulo(enlace))
        enlaces.append(get_enlace(enlace))
        autor.append(get_autor(enlace))
        fecha.append(get_fecha(enlace))
        
    titulo = [x for sublist in titulo for x in sublist] 
    enlaces = [x for sublist in enlaces for x in sublist]
    autor = [x for sublist in autor for x in sublist]
    fecha = [x for sublist in fecha for x in sublist]
    
    prposts_salud = pd.DataFrame({
        "fecha":fecha,
        "titulo":titulo,
        "autor(a)":autor,
        "categoria":"salud",
        "periodico":"Puerto Rico Posts",
        "region": "Juncos",
        "enlace":enlaces
        })
    
    prposts_salud['fecha'] = prposts_salud['fecha'].apply(fix_fecha)
    prposts_salud['fecha'] = pd.to_datetime(prposts_salud['fecha'])
    prposts_salud = prposts_salud.sort_values(by = 'fecha', ascending = False)
    prposts_salud = prposts_salud[['fecha','titulo','autor(a)','categoria','periodico', 'region', 'enlace']]
    
    return prposts_salud

# =============================================================================
# Implementacion de algoritmo
# =============================================================================

before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("\nHora que comenzo a correr el algoritmo: {}".format(current_time))

prposts = pd.read_csv('prposts.csv')
antes = len(prposts)
print("Comenzo con {} articulos.".format(antes))

gobierno = get_prposts_gobierno()
locales = get_prposts_locales()
seguridad = get_prposts_seguridad()
salud = get_prposts_salud()
educacion = get_prposts_educacion()

prposts = pd.concat([prposts, gobierno, locales, seguridad, salud, educacion])
prposts = prposts.drop_duplicates(subset = 'enlace')
prposts['fecha'] = pd.to_datetime(prposts['fecha'])
prposts = prposts.sort_values(by = 'fecha', ascending = False)
despues = len(prposts)

prposts.to_csv('prposts.csv', index = False)

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que terminó de correr el algoritmo: {}".format(current_time1))

print("Termino con {} articulos.".format(despues))
print("{} Artículos añadidos luego de correr el algoritmo.".format(despues-antes))