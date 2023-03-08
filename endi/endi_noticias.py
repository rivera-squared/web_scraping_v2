# Web scraping script para El Nuevo Día noticias

from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime
import re

def get_complete_link(link):
    """
    Concatena el link extension con el url principal
    Funcion acepta enlace como argumento.

    """
    endi = 'https://www.elnuevodia.com'
    complete_link = endi + link
    return complete_link

def get_autor(enlace):
    sel=Selector(text=requests.get(enlace).content)
    autor = ''.join(sel.xpath('//div[@class="toolbar-item item-author"]/p/span/a/text()').extract())
    
    # Los articulos que son solo video no listaran autor alguno
    if autor == '':
        # Sin embargo, hay articulos que no contienen video pero el comando en "autor" no funciona. Lo mas probable haya sido 
        # haya un error de la persona a cargo del website. El control flow de abajo ayuda a obtener el nombre del autor
        # si la palabra 'videos' no se encuentra dentro del enlace

        if (bool(re.search('(videos)', enlace))) == False: 
            return ''.join(sel.xpath('//div[@class="toolbar-item item-author"]/p/span/text()').extract())
        return "No autor"
    else:
        return autor
    
def get_fecha(enlace):
    
    sel=Selector(text=requests.get(enlace).content)
    fecha = ''.join(sel.xpath('//div[@class="toolbar-item item-date"]/p/text()').extract())
    
    # De la manera que esta disenada la pagina, la sintaxia del comando de "fecha" cambia si el articulo es solo un video.
    # El control flow de abajo ayuda a obtener la fecha aun si el articulo es solo un video.

    if fecha == '':
        if (bool(re.search('(videos)', enlace))) == True:
            return ''.join(sel.xpath('//div[@class="toolbar-item"]/p/text()').extract())
        elif(bool(re.search('(videos)', enlace))) == False:
            return ''.join(sel.xpath('//div[@class="toolbar-item item-date update"]/p/text()').extract_first())
        
        else:
            return 'No fecha'
    else:
        return fecha

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

def clean_fecha(fecha):
    
    x=re.sub('\w+\,', '', str(fecha)).strip()
    y=re.sub('(de)', '/',x).strip()
    z=fix_date(y)
    z=''.join(re.findall("\d+\s/\s\w+\s/\s\d{4}", z))
    time=pd.to_datetime(z, dayfirst=True)
    return time

def get_categoria(enlace):
    x=re.sub('(https://www.elnuevodia.com/noticias/)','',enlace)
    y=re.sub('/\S+','',x)
    return y.title()



def get_endi():
                        
    endi_new=[]
    enlaces = ['https://www.elnuevodia.com/noticias/locales/',
    'https://www.elnuevodia.com/noticias/gobierno/',
    'https://www.elnuevodia.com/noticias/legislatura/',
    'https://www.elnuevodia.com/noticias/politica/',
    'https://www.elnuevodia.com/noticias/seguridad/',
    'https://www.elnuevodia.com/noticias/tribunales/']
    
    
    for enlace in enlaces:
        sel=Selector(text=requests.get(enlace).content)
        titulo=sel.xpath('//h1[@class="story-tease-title"]/a/text()').extract()
        link_extension=sel.xpath('//h1[@class="story-tease-title"]/a/@href').extract()
        endi_dict = {'titulo':titulo, 'enlace':link_extension}
        endi_df = pd.DataFrame(endi_dict)
        endi_new.append(endi_df)
        
    noticias = pd.concat(endi_new)
    noticias['enlace']= noticias['enlace'].apply(get_complete_link)
    
    fecha=[]
    autor=[]
    categoria=[]
    for enlace in noticias['enlace']:
        sel=Selector(text=requests.get(enlace).content)
        autor.append(get_autor(enlace))
        fecha.append(get_fecha(enlace))
        categoria.append(get_categoria(enlace))
    
    noticias['autor']=autor
    noticias['fecha']=fecha
    noticias['fecha']=noticias['fecha'].apply(clean_fecha)
    noticias['categoria']=categoria
    
    noticias=noticias.sort_values(by='fecha',ascending=False)
    noticias=noticias[['fecha','titulo','autor','categoria','enlace']]
    return noticias

before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("Hora que comenzo a correr el algoritmo: {}".format(current_time))

noticias=pd.read_csv('endi_noticias.csv')
noticias['fecha']= pd.to_datetime(noticias['fecha'])
antes=len(noticias)

noticias_new = get_endi()
noticias = pd.concat([noticias_new, noticias])
noticias=noticias.drop_duplicates(subset='enlace')
# noticias=noticias[['fecha','titulo','enlace','autor']]
noticias.to_csv('endi_noticias.csv',index=False)
despues = len(noticias)

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Hora que termino de correr el algoritmo: {}".format(current_time1))
print("\nComenzo con {} articulos.".format(antes))
print("Termino con {} articulos.".format(despues))
print("{} Articulos anadidos luego de correr el algoritmo.".format(despues-antes))