import numpy as np
import pandas as pd
import math

df = pd.ExcelFile('datos_salta.xlsx')
number_rows = 1800

#df1 = pd.read_excel(df, sheet_name='2013', header=1, usecols=[0, 1])
df1 = pd.read_excel(df, sheet_name='2014', header=1, usecols=[0, 1], names=["fecha", "GHI"])
#df2 = pd.read_excel(df, sheet_name='2014')
#df3 = pd.read_excel(df, sheet_name='2015')




hoja1 = df1.dropna()
hoja1 =df1[df1["GHI"] >= 0]

df1 = hoja1.values
LAT = -24.7
LONG = -65.4
GMT = -3




def get_julian_day(value):
    day = pd.Timestamp(value)
    return day.day_of_year

def column_julian_day(values):
    new_values = np.array([])
    for i in range(len(values)):
        new_values = np.append(new_values, get_julian_day(values[i][0]))
    return new_values

def daily_angle(day):
    return np.divide(np.multiply(day-1, 2.0 * math.pi),365)

def generate_clock_hour():
    hour_values = np.arange(0, stop = 0.0166666667 * number_rows , step =0.0166666667)
    return hour_values

def generate_time_equation(angles):
    new_values = np.array([])
    for i in range(len(angles)):
        H3 = angles[i]
        time_equation_value = (0.0000075+0.001868*math.cos(H3)-0.032077*math.sin(H3)-0.014615*math.cos(2*H3)-0.04089*math.sin(2*H3))*229.2
        new_values = np.append(new_values, time_equation_value)
    return new_values
    

def generate_hora_solar(clock_hour, GMT, longitud, ecuation_time):
    new_values = np.array([])
    for i in range(len(clock_hour)):

        A = 1;
        if(GMT<0):
            A = -1;
                
        new_value =  clock_hour[i] + (4*((A*15 * GMT)-(A*LONG))+ecuation_time[i])/60
        #new_value = clock_hour[i]+(4*((-15*GMT)-LONG)+ecuation_time[i])/60
        new_values = np.append(new_values, new_value)
        
    return new_values

def generate_declination(julian_days):
    new_values = np.array([])
    for i in range(len(julian_days)):
        value = 23.45 * math.sin(math.radians(360*(284 + julian_days[i]))/365)
        new_values = np.append(new_values, value)
    return new_values
    
    
def generate_hour_angle(solar_hour):
    new_values = np.multiply(12-solar_hour, 15)
    return new_values


def generate_cos_tita_z(latitud, declination_rad, hour_angle_rad ):
    new_values = np.array([])
    for i in range(len(declination_rad)):
        
        C2 = 0.017453 * latitud
        L2 = declination_rad[i]
        N2 = hour_angle_rad[i]
        value = (math.cos(C2)*math.cos(L2)*math.cos(N2))+(math.sin(C2)*math.sin(L2))
        new_values = np.append(new_values, value)
    return new_values

def generate_e0(days):
    new_values = np.array([])
    for i in range(len(days)):
        new_values = np.append(new_values,1+0.033*math.cos(2* math.pi * days[i]/365) )
    return new_values
    
def generate_irradiancia_ext(cos_tita_z, TSI, E0):
    new_values = np.array([])
    
    
    for i in range(len(cos_tita_z)):
        if(cos_tita_z[i]<0):
            
            new_values = np.append(new_values, 0)
        else:
            value = TSI * E0[i] * cos_tita_z[i]
            new_values = np.append(new_values, value )
    return new_values


def get_hour(value):
    day = pd.Timestamp(value)
    return day.hour

def column_hour(values):
    new_values = np.array([])
    for i in range(len(values)):
        new_values = np.append(new_values, get_hour(values[i][0]))
    return new_values




hoja1["Dia"] = column_julian_day(df1)
hoja1["Hora"] = column_hour(df1)
hoja2 = hoja1.groupby(["Dia","Hora"], sort=False).size().to_frame("size")


hoja3 = hoja1.groupby(["Dia","Hora"], sort=False).sum()


hoja3["cantidad"] = hoja2["size"] 
hoja3["GHI_prom"] = hoja3["GHI"]/hoja3["cantidad"]

hoja3.to_csv("data_sin_filtrar_2014.csv", sep=";")

# hoja1["Dia"] = column_julian_day(df1)
# hoja1["LONG"] = LONG
# hoja1["LAT"] = LAT 
# hoja1["Angulo"] = daily_angle(hoja1["Dia"])
# hoja1["Hora Reloj"] = generate_clock_hour()
# hoja1["Ecuación del tiempo"] = generate_time_equation(hoja1["Angulo"])
# hoja1["Hora Solar"] = generate_hora_solar(hoja1["Hora Reloj"], GMT, LONG, hoja1["Ecuación del tiempo"])
# hoja1["Declinacion"] = generate_declination(hoja1["Dia"])
# hoja1["Declinacion en Radianes"] = np.multiply(hoja1["Declinacion"],  0.017453)
# hoja1["Angulo Horario"] = generate_hour_angle(hoja1["Hora Solar"])
# hoja1["Angulo Horario en Radianes "] = np.multiply(hoja1["Angulo Horario"],  0.017453)
# hoja1["Cos Tita z"] = generate_cos_tita_z(latitud=LAT, declination_rad=hoja1["Declinacion en Radianes"], hour_angle_rad= hoja1["Angulo Horario en Radianes "])
# hoja1["E0"] = generate_e0(hoja1["Dia"])
# hoja1["Irradiancia Extr. W"] = generate_irradiancia_ext(hoja1["Cos Tita z"],1367.00, hoja1["E0"])





