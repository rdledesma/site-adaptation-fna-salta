# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 15:30:25 2021

@author: Dario Ledesma
"""
import numpy as np
import pandas as pd
import math


class Extraterrestre:
    def __init__(self, dataFrame, lat, long, GMT):
        self.GMT = GMT
        self.LAT = lat
        self.LONG = long
        self.dataFrame = dataFrame
        self.dataFrame['LAT'] = lat
        self.dataFrame['LONG'] = long
        self.dataFrame['GMT'] = GMT
        self.dataFrame['Dia juliano'] = self.column_julian_day(self.dataFrame['Fecha'])
        self.dataFrame['Hora'] = self.column_hour(self.dataFrame['Fecha'])
        self.dataFrame['Angulo diario'] = self.daily_angle(self.dataFrame['Dia juliano'])
        self.dataFrame['Hora reloj'] = self.generate_clock_hour()
        self.dataFrame['Ecuacion del tiempo'] = self.generate_time_equation(self.dataFrame['Angulo diario'])
        self.dataFrame['Hora solar'] = self.generate_hora_solar(self.dataFrame['Hora reloj'], self.dataFrame['Ecuacion del tiempo']  )
        self.dataFrame['Declinacion'] = self.generate_declination(self.dataFrame['Dia juliano'])
        self.dataFrame['Declimacion en radianes'] = np.multiply(self.dataFrame["Declinacion"],  0.017453)
        self.dataFrame['Angulo horario'] = self.generate_hour_angle(self.dataFrame['Hora solar'])
        self.dataFrame['Angulo horario en radianes'] = np.multiply(self.dataFrame["Angulo horario"],  0.017453)
        self.dataFrame['Cos tita z'] = self.generate_cos_tita_z(self.dataFrame['Declimacion en radianes'], self.dataFrame["Angulo horario en radianes"])
        self.dataFrame['E0'] = self.generate_e0(self.dataFrame['Dia juliano'])
        self.dataFrame['Irr ext w'] = self.generate_irradiancia_ext(self.dataFrame['Cos tita z'] , 1367.00, self.dataFrame['E0'])
        self.dataFrame['Noche'] = self.dataFrame['Irr ext w'] <=0 
    
    
    def get_julian_day(self, value):
        day = pd.Timestamp(value)
        return day.day_of_year

    def column_julian_day(self,values):
        new_values = np.array([])
        for i in range(len(values)):
            new_values = np.append(new_values, self.get_julian_day(values[i]))
        return new_values
    
    def append_column(self, data, name):
        self.dataFrame[name] = data
    
    def daily_angle(self, day):
        return np.divide(np.multiply(day-1, 2.0 * math.pi),365)
    
    def generate_clock_hour(self):
        hour_values = np.arange(0, stop = 0.0166666667 *  len(self.dataFrame) , step =0.0166666667)
        return hour_values
    
    def generate_time_equation(self, angles):
        new_values = np.array([])
        for i in range(len(angles)):
            H3 = angles[i]
            time_equation_value = (0.0000075+0.001868*math.cos(H3)-0.032077*math.sin(H3)-0.014615*math.cos(2*H3)-0.04089*math.sin(2*H3))*229.2
            new_values = np.append(new_values, time_equation_value)
        return new_values
    
    def generate_hora_solar(self, clock_hour, ecuation_time):
        new_values = np.array([])
        for i in range(len(clock_hour)):
    
            A = 1;
            if(self.GMT<0):
                A = -1;
                    
            new_value =  clock_hour[i] + (4*((A*15 * self.GMT)-(A*self.LONG))+ ecuation_time[i])/60
            #new_value = clock_hour[i]+(4*((-15*GMT)-LONG)+ecuation_time[i])/60
            new_values = np.append(new_values, new_value)
        
        return new_values
    
    def generate_declination(self, julian_days):
        new_values = np.array([])
        for i in range(len(julian_days)):
            value = 23.45 * math.sin(math.radians(360*(284 + julian_days[i]))/365)
            new_values = np.append(new_values, value)
        return new_values
    
    def generate_hour_angle(self, solar_hour):
        new_values = np.multiply(12-solar_hour, 15)
        return new_values
    
    def generate_cos_tita_z(self, declination_rad, hour_angle_rad ):
        new_values = np.array([])
        for i in range(len(declination_rad)):
            
            C2 = 0.017453 * self.LAT
            L2 = declination_rad[i]
            N2 = hour_angle_rad[i]
            value = (math.cos(C2)*math.cos(L2)*math.cos(N2))+(math.sin(C2)*math.sin(L2))
            new_values = np.append(new_values, value)
        return new_values
    
    def generate_e0(self, days):
        new_values = np.array([])
        for i in range(len(days)):
            new_values = np.append(new_values,1+0.033*math.cos(2* math.pi * days[i]/365) )
        return new_values
    
    def generate_irradiancia_ext(self, cos_tita_z, TSI, E0):
        new_values = np.array([])
        
        for i in range(len(cos_tita_z)):
            if(cos_tita_z[i]<0):
                
                new_values = np.append(new_values, 0)
            else:
                value = TSI * E0[i] * cos_tita_z[i]
                new_values = np.append(new_values, value )
        return new_values
    
    def get_hour(self,value):
        day = pd.Timestamp(value)
        return day.hour

    def column_hour(self,values):
        new_values = np.array([])
        for i in range(len(values)):
            new_values = np.append(new_values, self.get_hour(values[i]))
        return new_values
