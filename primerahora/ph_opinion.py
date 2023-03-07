from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime
import re

def get_complete_link(link):
    """
    Concatena el url de primerahora y la extensión del enlace de cada artículo.

    Esta función acepta un argumento, link (<str>) la extensión del enlace del artículo.
    """
    ph = 'http://www.primerahora.com'
    complete_link = ph + link
    return complete_link

def get_title(enlace):
    # enlace = 'https://www.primerahora.com/opinion/celimar-adames-casalduc/'
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//h3[@class="ListItemTeaser__title TeaserTitle u-italic"]/text()').extract()

def get_link_extension(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="ListItemTeaser__column"]/a/@href').extract()

def get_fecha(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="ListItemTeaser__date"]/text()').extract()

def get_autor(enlace):
    
    a = re.sub("(http://www.primerahora.com/opinion/)","",enlace)
    b = re.sub("/\S+","",a)
    c = re.sub("-"," ", b)
    return c.title()

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
    
def get_ph_opinion():    

    enlaces=[
        'https://www.primerahora.com/opinion/celimar-adames-casalduc/', 
        'https://www.primerahora.com/opinion/norwill-fragoso/',
        'https://www.primerahora.com/opinion/normando-valentin/',
        'https://www.primerahora.com/opinion/juan-dalmau/',
        'https://www.primerahora.com/opinion/el-desahogo/',
        'https://www.primerahora.com/opinion/tayna-rivera-llavona/'
        ]
    
    primerahora=[]
    for enlace in enlaces:
        title=get_title(enlace)
        link_extension=get_link_extension(enlace)
        fecha = get_fecha(enlace)
        ph = pd.DataFrame({
            'fecha':fecha,
            'titulo':title,
            'enlace':link_extension
            })
        primerahora.append(ph)
        
    primerahora = pd.concat(primerahora)    
    
    primerahora['enlace'] = primerahora['enlace'].apply(get_complete_link)
    primerahora['autor(a)'] = primerahora['enlace'].apply(get_autor)
    primerahora['fecha'] = primerahora['fecha'].apply(fix_date)
    primerahora['fecha'] = pd.to_datetime(primerahora['fecha'], dayfirst=True)
    primerahora['categoria'] = "Opinion"
    primerahora = primerahora.sort_values(by='fecha', ascending = False)
    primerahora = primerahora[['fecha','titulo','autor(a)','categoria','enlace']]
    
    return primerahora
before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("\nHora que comenzó a correr el algoritmo: {}".format(current_time))

ph_opinion = pd.read_csv('ph_opinion.csv')
antes = len(ph_opinion)
print("\nComenzo con {} articulos.".format(antes))

ph_opinion_new = get_ph_opinion()
ph_opinion = pd.concat([ph_opinion_new, ph_opinion])
ph_opinion = ph_opinion.drop_duplicates(subset='enlace')
ph_opinion['fecha'] = pd.to_datetime(ph_opinion['fecha'])
despues = len(ph_opinion)

ph_opinion.to_csv('ph_opinion.csv', index = False)

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que terminó de correr el algoritmo: {}".format(current_time1))
print("Termino con {} articulos.".format(despues))
print("{} Artículos añadidos luego de correr el algoritmo.".format(despues-antes))