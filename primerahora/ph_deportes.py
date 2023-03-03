# Scrape para deportes (tab) PH
from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime

def get_complete_link(link):
    """
    Concatena el url de primerahora y la extensión del enlace de cada artículo.

    Esta función acepta un argumento, link (<str>) la extensión del enlace del artículo.
    """
    ph = 'http://www.primerahora.com'
    complete_link = ph + link
    return complete_link

def get_autor(link):
    """
    Obtiene el numbre del autor(a)

    Esta función acepta un argumento, link (<str>) el enlace completo.
    """
    url = str(link)
    sel = Selector(text=requests.get(url).content)
    autor = ''.join(sel.xpath('//div[@class="ArticleByline__authors"]/span/a/text()').extract())
    
    if autor == '':
        return "No autor"
    else:
        return autor
    
def fix_date(date):
    """
    Modifica el formato de la fecha usado por Primerahora para facilitar la conversion de fechas a formato datetime.

    La función toma un argumento, date, la fecha en formato (str) como publica Primerahora en sus artículos.
    """
    if ('ene' in date) == True:
        return date.replace('ene','jan')
    if ('feb' in date) == True:
        return date.replace('feb','feb')
    if ('mar' in date) == True:
        return date.replace('mar','mar')
    if ('abr' in date) == True:
        return date.replace('abr','apr')
    if ('mayo' in date) == True:
        return date.replace('mayo','may')
    if ('junio' in date) == True:
        return date.replace('junio','jun')
    if ('julio' in date) == True:
        return date.replace('julio','jul')
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

def get_deportes_ph():
    
    """
    Accesa, copia y pega en un dataframe los artículos publicados por las diferentes categorias en www.primerahora.com 
    No incluye columnas de opiniones

    Esta función no acepta ningún argumento.
    """
    primerahora_new=[]
    enlaces = ['https://www.primerahora.com/deportes/baloncesto/',
    'https://www.primerahora.com/deportes/beisbol/',
    'https://www.primerahora.com/deportes/boxeo/',
    'https://www.primerahora.com/deportes/voleibol/',
    'https://www.primerahora.com/deportes/hipismo/',
    'https://www.primerahora.com/deportes/futbol/',
    'https://www.primerahora.com/deportes/otros/']
    
    for enlace in enlaces:
        sel=Selector(text=requests.get(enlace).content)
        title = sel.xpath('//h3/text()').extract()
        date = sel.xpath('//div[@class="ListItemTeaser__date"]/text()').extract()
        link_extension = sel.xpath('//div[@class="ListItemTeaser__column"]/a/@href').extract()
        primerahora_dict = {'fecha':date,
	                        'titulo':title,
	                        'enlace':link_extension}
        primerahora_df = pd.DataFrame(primerahora_dict)
        primerahora_new.append(primerahora_df)
        deportes = pd.concat(primerahora_new)
        deportes['enlace']=deportes['enlace'].apply(get_complete_link)
        deportes['fecha'] = deportes['fecha'].apply(fix_date)
        deportes['fecha']=pd.to_datetime(deportes['fecha'], dayfirst=True)
        autor = []
        for link in deportes['enlace']:
	        autor.append(get_autor(link))
        deportes['autor'] = autor
        deportes=deportes.drop_duplicates(subset = 'enlace')
    return deportes

before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("Hora que comenzó a correr el algoritmo: {}".format(current_time))

deportes=pd.read_csv('ph_deportes.csv')
antes = len(deportes)

deportes_new=get_deportes_ph()
deportes = pd.concat([deportes_new, deportes])
deportes=deportes.drop_duplicates(subset='enlace')
despues = len(deportes)

deportes.to_csv('ph_deportes.csv',index=False)
now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que terminó de correr el algoritmo: {}".format(current_time1))
print("{} Artículos añadidos luego de correr el algoritmo.".format(despues-antes))