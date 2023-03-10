from scrapy import Selector
import requests
import pandas as pd
from datetime import datetime

# Lista de funciones para facilitar el proceso de scraping

def get_autor(link):
    """Esta función obtiene el nombre del autor(a) que escribió el artículo obtenido.
     Su único parámetro es "link", un str con el enlace que deseo obtener el autor(a). """
    
    url = str(link)
    sel = Selector(text=requests.get(url).content)
    autor = ''.join(sel.xpath('//a[@class="url fn n"]/text()').extract())
    return autor

def get_texto(link):
    """Esta función obtiene el texto de el artículo obtenido.
     Su único parámetro es "link", un str con el enlace que deseo obtener el texto. """

    url = str(link)
    sel = Selector(text=requests.get(url).content)
    texto=' '.join(sel.xpath('//div[@class="entry-content readMoreContent moreView post"]/p/text()').extract())
    
    # El control flow a continuación se anticipa a la posibilidad que haya artículos que no tengan texto. Como por ejemplo
    # El resumen via video que Jay Fonseca publica frecuentemente.
    if texto == '':
        return "No texto disponible"
    else:
        return texto

def get_fuente_original(link):
    """Esta función obtiene la fuente original (usualmente otro periódico) de el artículo obtenido.
     Su único parámetro es "link", un str con el enlace que deseo obtener la fuente original. """

    url = str(link)
    sel = Selector(text=requests.get(url).content)
    fuente_original = ''.join(sel.xpath('//div[@class="entry-content readMoreContent moreView post"]/p/a/text()').extract())
    
    # El control flow a continuación se anticipa a la posibilidad que haya artículos cuya fuente original sea Jagual Media.
    if fuente_original == '':
        return "Jagual Media es Fuente Original"
    else:
        return fuente_original
    
    return fuente_original

def get_enlace_fuente_original(link):
    """Esta función obtiene el enlace de la fuente original (usualmente otro periódico) de el artículo obtenido.
     Su único parámetro es "link", un str con el enlace que deseo obtener la fuente original. """

    url = str(link)
    sel = Selector(text=requests.get(url).content)
    enlace_fuente_original = ''.join(sel.xpath('//div[@class="entry-content readMoreContent moreView post"]/p/a/@href').extract())
    
    # El control flow a continuación se anticipa a la posibilidad que haya artículos cuya fuente original sea Jagual Media.
    if enlace_fuente_original == '':
        return "Jagual Media es Fuente Original"
    else:
        return enlace_fuente_original

def get_jay_fonseca(initial_page_number = 0, page_number=1):

    """Función donde el usuario puede accesar, copiar y pegar, en un dataframe, el contenido de www.jayfonseca.com

    Esta función acepta dos parámetros: "initial_page_number" (cuyo valor predeterminado es 0) y "page_number" (cuyo valor predeterminado es 1).
    El usuario puede escoger las extenciones del enlace que desea obtener la información.

    Ojo: Por favor limítese a obtener no mas de 50 páginas a la vez. Una selección grande puede tumbar el servidor de la web de JF y puede
    existir la posibilidad que se prohíba un acceso futuro.

    """

    pages = list(range(initial_page_number,page_number,1))
    
    jf = []
    
    for page in pages:    
        #texto=[]
        autor=[]
        fuente_original=[]
        enlace_original=[]
        
        url = 'https://jayfonseca.com/page/' + str(page)
        sel = Selector(text=requests.get(url).content)
        titulo = sel.xpath('//h2[@class="entry-title"]/a/text()').extract()
        fecha = sel.xpath('//li[@class="meta-date"]/text()').extract()
        link = sel.xpath('//h2[@class="entry-title"]/a/@href').extract()
    
        for enlace in link:
            #texto.append(get_texto(enlace))
            autor.append(get_autor(enlace))
            fuente_original.append(get_fuente_original(enlace))
            enlace_original.append(get_enlace_fuente_original(enlace))
    
        
        x_df = pd.DataFrame({
            'fecha':fecha,
            'autor':autor,
            'titulo':titulo,
            #'texto':texto,
            'enlace':link,
            "fuente_original":fuente_original,
            'enlace_original':enlace_original
            })
        
        jf.append(x_df)
    
    jf = pd.concat(jf)
    jf['fecha']=pd.to_datetime(jf['fecha'], dayfirst= True)
    jf=jf.sort_values(by='fecha', ascending=False)
    jf=jf.drop_duplicates(subset = 'enlace')
    # print("Current page: {}".format(page))
    return jf

before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("Hora que comenzó a correr el algoritmo: {}".format(current_time))


df=pd.read_csv("jay_fonseca_completo.csv")
antes = len(df)
print("\nComenzo con {} articulos.".format(antes))
df['fecha']=pd.to_datetime(df['fecha'])
df_new=get_jay_fonseca(0,4)
# df = df_new.append(df)
df = pd.concat([df_new, df])
df=df.drop_duplicates(subset='enlace')
despues = len(df)

df.to_csv("jay_fonseca_completo.csv",index=False)
# print("Scraping culminó exitosamente \nCon {} articulos".format(len(df)))
# print('Titular del último artículo publicado: "{}"'.format(df['titulo'].iloc[0]))

now = datetime.now()
current_time1 = now.strftime("%H:%M:%S")
print("Termino con {} articulos.".format(despues))
print("Hora que terminó de correr el algoritmo: {}".format(current_time1))
print("{} Artículos añadidos luego de correr el algoritmo.".format(despues-antes))