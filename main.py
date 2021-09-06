import numpy as np
import pandas as pd
import math

from ExtraterrestreClass import Extraterrestre as ext


#Inicio Leer base de datos datos observados.
#El archivo debe estar en formato .xlxs
#El archivo debe contener las columnas en la siguiente disposición
#Fecha, GHI, UVE


# df = pd.ExcelFile('datos_salta.xlsx')
# number_rows = 10000
# names = df.sheet_names

# df1 = pd.read_excel(df, sheet_name=None, header=0, usecols=[0,1,2])
# for name in names:
#     df1[name]['Year'] = name

# df = pd.concat(df1, ignore_index=1)


# #se convierte el archivo a csv, para mejor uso
# df.to_csv('datos_salta.csv', sep=';', index=False)

#Fin Leer base de datos datos observados.

df = pd.read_csv('datos_salta.csv', delimiter=";" , nrows=10000)

df.columns = ['Fecha', 'GHI obs', 'UVE', 'Year']


LAT = -24.7
LONG = -65.4
GMT = -3

dataObject = ext(dataFrame=df, lat=LAT, long=LONG, GMT = GMT)
df = dataObject.dataFrame












