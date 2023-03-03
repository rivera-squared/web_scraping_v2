# Merging PrimeraHora
import pandas as pd

noticias = pd.read_csv('noticias_ph.csv')
entretenimiento = pd.read_csv('entretenimiento.csv')
deportes = pd.read_csv('deportes_ph.csv')

primerahora = pd.concat([noticias, entretenimiento, deportes])
primerahora.to_csv("primerahora.csv", index=False)

print("Total de articulos de noticias: {}".format(len(noticias)))
print("Total de articulos de entretenimiento: {}".format(len(entretenimiento)))
print("Total de articulos de deportes: {}".format(len(deportes)))
print("Total de articulos: {}".format(len(noticias) + len(entretenimiento) + len(deportes)))
