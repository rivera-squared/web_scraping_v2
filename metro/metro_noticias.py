from scrapy import Selector
import requests
import pandas as pd

def get_title(enlace):
    # enlace = 'https://www.metro.pr/noticias/locales/'
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//h2[@class="primary-font__PrimaryFontStyles-o56yd5-0 ctbcAa headline-text"]/text()').extract()

def get_link_extension(enlace):
    # enlace = 'https://www.metro.pr/noticias/locales/'
    sel=Selector(text=requests.get(enlace).content)
    return sel.xpath('//div[@class="results-list--headline-container"]/a/@href').extract()

def get_complete_link(enlace):
    metro = 'https://www.metro.pr'
    return metro + enlace

def get_autor(enlace):
    # enlace = 'https://www.metro.pr/metro-negocios/2023/01/16/condom-world-planifica-seguir-expandiendo-su-presencia-en-florida/'
    sel=Selector(text=requests.get(enlace).content)
    autor =  ''.join(sel.xpath('//span[@class="ts-byline__names"]/a/text()').extract())
    
    if autor == '':
        return ''.join(sel.xpath('//span[@class="ts-byline__names"]/text()').extract())
    else:
        return autor
    
def get_fecha(enlace):
        # enlace='https://www.metro.pr/noticias/2023/03/03/apelaciones-determina-que-opfei-no-tiene-jurisdiccion-en-caso-de-compra-de-pruebas-de-covid-19/'
        sel=Selector(text=requests.get(enlace).content)
        return ''.join(sel.xpath('//time/text()').extract_first())

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
        a=''.join(re.findall("\d{2}\s\w{2}\s\w+\\w{2}\s\d{4}", fecha))
        b=re.sub("(de)","",a).strip()
        c=re.sub(" ","/",b)
        d=re.sub("//","/",c)
        x=fix_date(d)
        return pd.to_datetime(x, dayfirst=True)

def get_categoria(enlace):
    # enlace = 'https://www.metro.pr/noticias/2023/03/03/apelaciones-determina-que-opfei-no-tiene-jurisdiccion-en-caso-de-compra-de-pruebas-de-covid-19/'
    a=re.sub("(https://www.metro.pr/)","",enlace)
    # b=re.sub("/\d+\S+","",a)
    return a

def get_metro_noticias():
        
    enlaces = [
        'https://www.metro.pr/noticias/locales',
        'https://www.metro.pr/noticias/economia',
        'https://www.metro.pr/noticias/mundo',
        'https://www.metro.pr/metro-negocios'
        ]
    
    title=[]
    link_extension=[]
    # categoria=[]
    for count, enlace in enumerate(enlaces):
        title.append(get_title(enlace))
        link_extension.append(get_link_extension(enlace))
        
    titulo = [x for sublist in title for x in sublist]    
    enlace = [x for sublist in link_extension for x in sublist]
    
    metro_noticias = pd.DataFrame({
        'titulo':titulo,
        'enlace':enlace
        })
    
    metro_noticias['enlace']=metro_noticias['enlace'].apply(get_complete_link)
    metro_noticias['autor']=metro_noticias['enlace'].apply(get_autor)
    metro_noticias['fecha']=metro_noticias['enlace'].apply(get_fecha)
    metro_noticias['fecha']=metro_noticias['fecha'].apply(clean_fecha)
    # metro_noticias['categoria']=metro_noticias['enlace'].apply(get_categoria)
    
    metro_noticias = metro_noticias[['fecha','titulo','autor','enlace']]
    metro_noticias = metro_noticias.sort_values(by='fecha', ascending = False)

    return metro_noticias

before = datetime.now()
current_time = before.strftime("%H:%M:%S")
print("Hora que comenzo a correr el algoritmo: {}".format(current_time))

metro_noticias = pd.read_csv('metro_noticias.csv')
metro_noticias_new = get_metro_noticias()

metro_noticias.to_csv('metro_noticias.csv', index=False)
