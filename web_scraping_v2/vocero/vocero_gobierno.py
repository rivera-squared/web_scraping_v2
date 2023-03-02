from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime
import re

def get_complete_link(enlace):
    vocero = 'https://www.elvocero.com'
    return vocero + enlace

def get_link_extension(enlace):
    sel=Selector(text=requests.get(enlace).content)
    link_extension = sel.xpath('//h3[@class="tnt-headline "]/a/@href').extract()
    
    enlace_completo=[]
    for link in link_extension:
        enlace_completo.append(get_complete_link(link))
        
    return enlace_completo


def get_title(enlace):
    
    sel=Selector(text=requests.get(enlace).content)
    titles = sel.xpath('//h3[@class="tnt-headline "]/a/text()').extract()
    
    titulo=[]
    for title in titles:
        titulo.append(title.strip())
    
    return titulo                      

def get_author(enlace):
    sel=Selector(text=requests.get(enlace).content)
    return ''.join(sel.xpath('//ul[@class="list-inline"]/li/span/a/text()').extract())

def clean_autor(autor):
    x = re.sub("(EL VOCERO)","", autor)
    y = re.sub("[>,]","", x)
    z = re.sub("/"," ", y)
    
    return z

def get_fecha(enlace):
    # enlace = 'https://www.elvocero.com/ley-y-orden/federal/relevan-de-sus-funciones-a-oficial-de-guardia-costera-que-choc-en-costas-de-dorado/article_00361b44-af8f-11ed-b3bb-0fe5f7a6525f.html'
    sel=Selector(text=requests.get(enlace).content)
    return ''.join(sel.xpath('//li[@class="hidden-print"]/time/text()').extract())

def clean_fecha(fecha):
    fecha = ''.join(re.findall("\d+/\d+/\d+", str(fecha)))   
    
    if fecha =='':
        return "No fecha"
    else:
        return ''.join(re.findall("\d+/\d+/\d+", str(fecha)))   

def clean_fecha1(fecha):
       
    if fecha != 'No fecha':
        return pd.to_datetime(fecha, dayfirst=True)
    else:
        return "No fecha"              

def get_categoria(enlace):
    x=re.sub('(https://www.elvocero.com/gobierno)','',enlace)
    y=re.sub('/\S+','',x)
    return y.title()         

def get_noticias_vocero():
    
    enlaces = ['https://www.elvocero.com/gobierno/agencias/',
                'https://www.elvocero.com/gobierno/fortaleza/',
                'https://www.elvocero.com/gobierno/legislatura/',
                'https://www.elvocero.com/gobierno/municipal/']
    enlace=[]
    titulo=[]
    for link in enlaces:
        
        titulo.append(get_title(link))
        enlace.append(get_link_extension(link))
        
        new_enlace = [x for sublist in enlace for x in sublist]
        new_titulo = [x for sublist in titulo for x in sublist]
        
    vocero = pd.DataFrame({
        "titulo":new_titulo,
        "enlace":new_enlace})
    
    autor =[]
    for enlace in vocero['enlace']:
        autor.append(get_author(enlace))
        
    vocero['autor'] = autor
    vocero['autor'] = vocero['autor'].apply(clean_autor)
    
    fechas = vocero['enlace'].apply(get_fecha)
    vocero['fecha'] = fechas
    vocero['fecha'] = vocero['fecha'].apply(clean_fecha)
    vocero['fecha'] = vocero['fecha'].apply(clean_fecha1)
    vocero['categoria']=vocero['enlace'].apply(get_categoria)
    vocero=vocero[['fecha','titulo','autor','categoria','enlace']]
    
    
    return vocero

before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("Hora que comenzo a correr el algoritmo: {}".format(current_time))
      
gobierno = pd.read_csv('vocero_gobierno.csv')
gobierno['fecha'] = pd.to_datetime(gobierno['fecha'])

antes=len(gobierno)    
gobierno_new=get_noticias_vocero()
gobierno = pd.concat([gobierno_new, gobierno])
gobierno = gobierno.drop_duplicates(subset='enlace')

gobierno.to_csv('vocero_gobierno.csv',index=False)
despues = len(gobierno)

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que termino de correr el algoritmo: {}".format(current_time1))
print("\nComenzo con {} articulos.".format(antes))
print("Termino con {} articulos.".format(despues))
print("{} Articulos a~adidos luego de correr el algoritmo.".format(despues-antes))