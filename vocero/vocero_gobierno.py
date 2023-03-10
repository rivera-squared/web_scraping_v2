from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime
import numpy as np
import re

def get_complete_link(enlace):
    vocero = 'https://www.elvocero.com'
    return vocero + enlace

def get_title1():
    enlace = 'https://www.elvocero.com/gobierno/'
    sel=Selector(text=requests.get(enlace).content)
    titles = sel.xpath('//h2[@class="tnt-headline "]/a/text()').extract()
    title_clean = []
    for title in titles:
        title_clean.append(title.strip())
    return title_clean

def get_title2():
    enlace = 'https://www.elvocero.com/gobierno/'
    sel=Selector(text=requests.get(enlace).content)
    titles = sel.xpath('//h3[@class="tnt-headline "]/a/text()').extract()
    title_clean = []
    for title in titles:
        title_clean.append(title.strip())
    return title_clean
        
def get_enlace1():
    enlace = 'https://www.elvocero.com/gobierno/'
    sel=Selector(text=requests.get(enlace).content)
    enlaces = sel.xpath('//h2[@class="tnt-headline "]/a/@href').extract()
    enlace_completo = []
    for x in enlaces:
        enlace_completo.append(get_complete_link(x))
    return enlace_completo

def get_enlace2():
    enlace = 'https://www.elvocero.com/gobierno/'
    sel=Selector(text=requests.get(enlace).content)
    enlaces = sel.xpath('//h3[@class="tnt-headline "]/a/@href').extract()
    enlace_completo = []
    for x in enlaces:
        enlace_completo.append(get_complete_link(x))
    return enlace_completo

def clean_fecha(fecha):
    fecha = ''.join(re.findall("\d+/\d+/\d+", str(fecha)))   
    
    if fecha =='':
        return "No fecha"
    else:
        return ''.join(re.findall("\d+/\d+/\d+", str(fecha))) 

def get_fecha(enlace):
    sel=Selector(text=requests.get(enlace).content)
    fecha = ''.join(sel.xpath('//li[@class="hidden-print"]/time/text()').extract())
        
    if fecha == '':
        return np.nan
    else:
        return pd.to_datetime(clean_fecha(fecha), dayfirst=True)
def clean_autor(autor):
    x = re.sub("(EL VOCERO)","", autor)
    y = re.sub("[>,]","", x)
    z = re.sub("/"," ", y)
    
    return z

def get_autor(enlace):
    # enlace = 'https://www.elvocero.com/gobierno/fortaleza/gobernador-llega-a-bayam-n-para-reuni-n-con-la-federaci-n-de-alcaldes/article_761c9616-b774-11ed-b67e-7f8e07bfc2c7.html'
    sel=Selector(text=requests.get(enlace).content)
    autor = ''.join(sel.xpath('//ul[@class="list-inline"]/li/span/a/text()').extract())
    
    if autor == '':
        return clean_autor(sel.xpath('//ul[@class="list-inline"]/li/span/text()').extract()[1]).strip()
    elif autor == '':
        return "No autor(a)"
    else:
        return clean_autor(autor).strip()    


# Seccion principal
def get_vocero_gobierno1():
    titulo1 = get_title1()
    enlace1 = get_enlace1()
    vocero_gobierno = pd.DataFrame({
        'titulo':titulo1,
        'enlace':enlace1,
        'categoria': "Gobierno"
        })
    vocero_gobierno['fecha'] = vocero_gobierno['enlace'].apply(get_fecha)
    vocero_gobierno['autor(a)'] = vocero_gobierno['enlace'].apply(get_autor)
    vocero_gobierno = vocero_gobierno[['fecha','titulo','autor(a)','categoria','enlace']]
    vocero_gobierno = vocero_gobierno.sort_values(by='fecha', ascending = False)
    
    return vocero_gobierno

# Seccion secundaria
def get_vocero_gobierno2():
    
    titulo2 = get_title2()
    enlace2 = get_enlace2()
    vocero_gobierno = pd.DataFrame({
        'titulo':titulo2,
        'enlace':enlace2,
        'categoria': "Gobierno"
        })
    vocero_gobierno['fecha'] = vocero_gobierno['enlace'].apply(get_fecha)
    vocero_gobierno['autor(a)'] = vocero_gobierno['enlace'].apply(get_autor)
    vocero_gobierno = vocero_gobierno[['fecha','titulo','autor(a)','categoria','enlace']]
    vocero_gobierno = vocero_gobierno.sort_values(by='fecha', ascending = False)
    
    return vocero_gobierno

def vocero_gobierno():
    vocero_gobierno_principal = get_vocero_gobierno1()
    vocero_gobierno_secundario = get_vocero_gobierno2()
    vocero_gobierno = pd.concat([vocero_gobierno_principal, vocero_gobierno_secundario])
    vocero_gobierno = vocero_gobierno.sort_values(by = 'fecha', ascending = False)
    return vocero_gobierno

# =============================================================================
# Aplicar algoritmos
# =============================================================================
before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("\nHora que comenzo a correr el algoritmo: {}".format(current_time))
      
gobierno = pd.read_csv('vocero_gobierno.csv')

antes=len(gobierno)    
print("Comenzo con {} articulos.".format(antes))

gobierno_new = vocero_gobierno()
gobierno = pd.concat([gobierno_new, gobierno])
gobierno = gobierno.drop_duplicates(subset='enlace')
gobierno['fecha'] = pd.to_datetime(gobierno['fecha'])
gobierno = gobierno.sort_values(by = 'fecha', ascending = False)
gobierno.to_csv('vocero_gobierno.csv',index=False)
despues = len(gobierno)

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que termino de correr el algoritmo: {}".format(current_time1))

print("Termino con {} articulos.".format(despues))
print("{} Articulos a~adidos luego de correr el algoritmo.".format(despues-antes))



