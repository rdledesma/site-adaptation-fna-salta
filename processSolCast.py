# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 17:52:41 2021

@author: Dario Ledesma
"""

import numpy as np
import pandas as pd
import math

def get_julian_day(value):
    day = pd.Timestamp(value)
    return day.day_of_year

def column_julian_day(values):
    new_values = np.array([])
    for i in range(len(values)):
        new_values = np.append(new_values, get_julian_day(values[i][0]))
    return new_values


def get_hour(value):
    day = pd.Timestamp(value)
    return day.hour

def column_hour(values):
    new_values = np.array([])
    for i in range(len(values)):
        new_values = np.append(new_values, get_hour(values[i][0]))
    return new_values

#df_solcast = pd.read_csv("data_2013.csv", delimiter=",", nrows=10, usecols=["Ghi", "GHI(W/m2) medido"])





#Ghi = df_solcast["Ghi"]
#Ghi_medido = df_solcast["GHI(W/m2) medido"] 


#frecuencia_ghi = Ghi.value_counts() 
#frecuencia_acumulativa_ghi = frecuencia_ghi.cumsum()


df_solcast_2014 = pd.read_csv("solcast_salta_2014.csv", delimiter=";", usecols=["PeriodStart", "Ghi"])
df_solcast_2014["dia"] = column_julian_day(df_solcast_2014.values) 
df_solcast_2014["hora"] = column_hour(df_solcast_2014.values)

df_saltadb_2014 = pd.read_csv("data_sin_filtrar_2014.csv", delimiter=";")


df_saltadb_2014= df_saltadb_2014.where(df_saltadb_2014["cantidad"]>=30)
df_saltadb_2014 = df_saltadb_2014.dropna()

solcast_2014 = df_saltadb_2014


df_filtrado_2014 = df_solcast_2014[df_solcast_2014.set_index(['dia','hora']).index.isin(df_saltadb_2014.set_index(['Dia','Hora']).index)]

df_filtrado_2014 = df_filtrado_2014.reset_index()
df_saltadb_2014 = df_saltadb_2014.reset_index()


#Datos filtrados, match solcast - salta2014

df_saltadb_2014["Ghi estimado"] = df_filtrado_2014["Ghi"]
df_saltadb_2014["Año"] = 2014


df_solcast_2013 = pd.read_csv("solcast_salta_2013.csv", delimiter=";", usecols=["PeriodStart", "Ghi"])
df_solcast_2013["dia"] = column_julian_day(df_solcast_2013.values) 
df_solcast_2013["hora"] = column_hour(df_solcast_2013.values)

df_saltadb_2013 = pd.read_csv("data_sin_filtrar_2013.csv", delimiter=";")


df_saltadb_2013= df_saltadb_2013.where(df_saltadb_2013["cantidad"]>=30)
df_saltadb_2013 = df_saltadb_2013.dropna()

solcast_2013 = df_saltadb_2013


df_filtrado_2013 = df_solcast_2013[df_solcast_2013.set_index(['dia','hora']).index.isin(df_saltadb_2013.set_index(['Dia','Hora']).index)]

df_filtrado_2013 = df_filtrado_2013.reset_index()
df_saltadb_2013 = df_saltadb_2013.reset_index()


#Datos filtrados, match solcast - salta2013

df_saltadb_2013["Ghi estimado"] = df_filtrado_2013["Ghi"]
df_saltadb_2013["Año"] = 2013





df_saltadb_2013.to_csv("data_filtrada_2013.csv", sep=",")
df_saltadb_2014.to_csv("data_filtrada_2014.csv", sep=",")

