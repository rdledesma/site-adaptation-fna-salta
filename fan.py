# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 10:39:18 2021

@author: Dario Ledesma
"""

import pandas as pd

df = pd.read_csv("Ghi_2013_2014.csv", delimiter=",")

Ghi = df["Ghi estimado"]




frecuencia_ghi = Ghi.value_counts() 
frecuencia_acumulativa_ghi = frecuencia_ghi.cumsum()