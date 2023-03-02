import pandas as pd

df=pd.read_csv('jay_fonseca_completo.csv')
df['fecha']=pd.to_datetime(df['fecha'])

# I stopped at page 820. Go back one or two pages to ensure you are getting all articles published
df_new=get_jay_fonseca(821,861)
df = df.append(df_new)
df.to_csv("jay_fonseca_completo.csv",index=False)

# La columna de "autor" sale como "No autor" en el 2020. Lo mas probable sea por la composición de la página web en si.
# Cuando haya terminado el proceso completo de scraping, tengo que crear otra función con la sintaxia que logre recopilar
# la información del autor(a) del artículo.