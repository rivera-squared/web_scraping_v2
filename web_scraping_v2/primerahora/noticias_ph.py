# Scrape para noticias (tab) PH
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
    
def get_categoria(enlace):
    x=re.sub('(http://www.primerahora.com/noticias/)','',enlace)
    y=re.sub('/\S+','',x)
    return y.title()    

def get_noticias_ph():
    
    """
    Accesa, copia y pega en un dataframe los artículos publicados por las diferentes categorias en www.primerahora.com 
    No incluye columnas de opiniones

    Esta función no acepta ningún argumento.
    """
    primerahora_new=[]
    enlaces = ['https://www.primerahora.com/noticias/puerto-rico/',
    'https://www.primerahora.com/noticias/policia-tribunales/',
    'https://www.primerahora.com/noticias/gobierno-politica/',
    'https://www.primerahora.com/noticias/consumo/',
    'https://www.primerahora.com/noticias/estados-unidos/',
    'https://www.primerahora.com/noticias/mundo/',
    'https://www.primerahora.com/noticias/ciencia-tecnologia/']
    
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
        noticias = pd.concat(primerahora_new)
        noticias['enlace']=noticias['enlace'].apply(get_complete_link)
        noticias['fecha'] = noticias['fecha'].apply(fix_date)
        noticias['fecha']=pd.to_datetime(noticias['fecha'], dayfirst=True)
        
        autor = []
        categoria=[]
        for link in noticias['enlace']:
	        
            autor.append(get_autor(link))
            categoria.append(get_categoria(link))
            
        noticias['autor'] = autor
        noticias['categoria'] = categoria
        noticias=noticias.drop_duplicates(subset = 'enlace')
        noticias=noticias[['fecha','titulo','autor','categoria','enlace']]
    return noticias    

before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("Hora que comenzó a correr el algoritmo: {}".format(current_time))

noticias=pd.read_csv('noticias_ph.csv')
antes = len(noticias)

noticias_new=get_noticias_ph()
noticias = pd.concat([noticias_new, noticias])
noticias=noticias.drop_duplicates(subset='enlace')
noticias['fecha']= pd.to_datetime(noticias['fecha'])
noticias=noticias.sort_values(by='fecha', ascending=False)
despues = len(noticias)

noticias.to_csv('noticias_ph.csv',index=False)
now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que terminó de correr el algoritmo: {}".format(current_time1))
print("\nComenzo con {} articulos.".format(antes))
print("Termino con {} articulos.".format(despues))
print("{} Artículos añadidos luego de correr el algoritmo.".format(despues-antes))