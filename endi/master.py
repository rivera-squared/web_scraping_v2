# Merging the different tables
import pandas as pd

noticias = pd.read_csv('noticias_endi.csv')
negocios = pd.read_csv('negocios_endi.csv')
master = pd.concat([noticias, negocios])

master.to_csv('endi.csv', index = False)

print("Articulos de noticias: {}".format(len(noticias)))
print("Articulos de negocios: {}".format(len(negocios)))
print("Total de articulos de ENDI: {}".format(len(noticias) + len(negocios)))