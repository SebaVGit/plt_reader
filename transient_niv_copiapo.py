# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 15:15:31 2019

@author: Sebastian_Hidrica
"""


import csv
import sys
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date
from datetime import timedelta  
from numpy import genfromtxt
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
import locale
from collections import OrderedDict
from tqdm import tqdm
#-------------------skip matplotlib warning-------------------------------
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#------------------------Funciones------------------------------------------
def suma_lista(lista,a):
    lista=[x+a for x in lista]
    return lista

def corte(array):
    for i in range(0,len(array[4]),1):
        if array[2][i]=='Concentration':
            aux=i
            break
    array=array.drop(array.index[aux:])#en este caso borra todo lo que encuentra después de "Concentration"
    array.reset_index(drop=True, inplace=True)
    return array

def nombre(array):
    name=[]
    for i in range(0,len(array[4]),1):
        if (array[4][i] not in name)==True:
            if array[0][i]=='ZONE':
                name.append(array[4][i][:-2])    
    name=list(OrderedDict.fromkeys(name)) #remover duplicados
    return name

def indices(array):
    indice_sim=[]
    indice_obs=[]
    for i in range(0,len(array[4]),1):
        if type(array[1][i])==str:
            if array[1][i][3:]=='Simulated':
                indice_sim.append(i)
            elif array[1][i][3:]=='Observed':
                indice_obs.append(i)
    return indice_sim, indice_obs

def datos(array,indice_sim,indice_obs,i):
    obs=[]
    sim=[]
    tiempo_obs=[]
    tiempo_sim=[]
    for j in range(0,len(array[4]),1):
        if i<len(indice_sim)-1:
            if j>=indice_sim[i]+1 and j<=indice_obs[i]-1:
                sim.append(float(array[4][j]))
                tiempo_sim.append(float(array[2][j]))
            if j>=indice_obs[i]+1 and j<=indice_sim[i+1]-1:
                obs.append(float(array[4][j]))
                tiempo_obs.append(float(array[2][j]))
        else:
            if j>=indice_sim[i]+1 and j<=indice_obs[i]-1:
                sim.append(float(array[4][j]))
                tiempo_sim.append(float(array[2][j]))
            if j>=indice_obs[i]+1 and j<=len(array[4]):
                obs.append(float(array[4][j]))
                tiempo_obs.append(float(array[2][j]))
    return obs, sim, tiempo_obs, tiempo_sim

def To_Date(lista,fecha_ini):
    for k in range(0,len(lista),1):
        lista[k]=date.fromordinal(fecha_ini+int(lista[k]))
    return lista

def ID_particion(lista,fecha):
    booleano=np.array(lista,dtype='datetime64')<np.array(fecha,dtype='datetime64')
    index=0
    for b in booleano:
        index=index+1
        if b==False:
            break
    index=index-1
    return index

def clear_list(lista):
    lista=[]
    return lista

#---------------------set locale------------------------
locale.setlocale(locale.LC_NUMERIC, "esp_esp")
locale.setlocale(locale.LC_TIME, 'esp_esp')
#-----------------------------Set matplotlib----------------
plt.rcdefaults()

# Tell matplotlib to use the locale we set above
plt.rcParams['axes.formatter.use_locale'] = True
# Tell matploblib tu use a customize rcParams
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = '12'
plt.rcParams['font.sans-serif'] = 'Calibri' #Calibri pues es el que se usa en HC
plt.rcParams["figure.figsize"] = [12,8.5] #da la dimension que tendrán los plots

#---------------------------------------------------


import time
t = time.time()
#--------------Presentación-------------------------------
presentacion='Developed by Sebastián V. G.\nVersión CalVal Copiapó 1.5'
print(presentacion)

#----------crea el directorio adecuado-------
Ruta = os.getcwd() + '\\'
directory =  Ruta + 'Formato_Informe_Niv'
if not os.path.exists(directory):
    os.makedirs(directory)
directory = directory + '\\'

#-------------------------------------leer archivo----------------------------------------------
nivel=pd.read_csv(Ruta+'BASE.plt',sep=' ',encoding = "ISO-8859-1",names=[0,1,2,3,4,5,6],skiprows=2)

#------------------------Para guardar los nombres-----------------------------

name=nombre(nivel)

#-----------------------indices------------------------------

indice_sim, indice_obs=indices(nivel)
            
#-------------------Fechas importantes-----------------
fecha_ini=dt.date.toordinal(date(1992,12,31))
#date.fromordinal(aux)

#--------------------------------CalVal--------------------------------
fecha_cal=dt.datetime(2015,3,1)
            
#-----------------------------guardar los datos sim y obs------------------------


ticks = [dt.datetime(i, 1, 1) for i in range(1993, 2019, 2)]#control the ticks, un año más del final (era el 2019) para poder plotear el últimno
for i in tqdm(range(0,len(indice_sim),1)):
    obs, sim, tiempo_obs, tiempo_sim=datos(nivel,indice_sim,indice_obs,i)
    tiempo_obs=To_Date(tiempo_obs,fecha_ini)
    tiempo_sim=To_Date(tiempo_sim,fecha_ini)
    #-----------------Analizar periodo---------------------
    #index=ID_particion(tiempo_sim,fecha_cal)
    #-------------------------------------------------------
    fig,ax = plt.subplots(1)
    #X and Y axis boundaries
    obsmin=min(obs)
    obsmax=max(obs)
    simmin=min(sim)
    simmax=max(sim)
    ymin=min(obsmin,simmin)
    ymax=max(obsmax,simmax)
    dif=ymax-ymin #importante pues hay algunos pozos que tienen una bajada bien pronunciada
    if dif>100:
        delta=dif+50
    else:
        delta=100
    ymin=ymin-(delta-(dif))/2
    ymax=ymax+(delta-(dif))/2
    tiempomin=dt.datetime(1993,1,1)
    tiempomax=dt.datetime(2017,12,31)
    monthsFmt = mdates.DateFormatter("%b-%Y")
    majorFormatter = FormatStrFormatter('%.2f')
    minor = mdates.YearLocator(1)
    years = mdates.YearLocator(2,month=1, day=1)
    ax.xaxis.set_major_formatter(monthsFmt)   
    ax.xaxis.set_minor_locator(minor)
    ax.xaxis.set_major_locator(years)
    ax.yaxis.set_minor_locator(tkr.MultipleLocator(5))
    ax.yaxis.set_major_locator(tkr.MultipleLocator(10))
    # plot the data
    ax.set_xticks(ticks)
    ax.plot(tiempo_obs,obs,'bd',tiempo_sim,sim,'r-', markerfacecolor='none')
    ax.set_xlim(tiempomin,tiempomax)
    ax.set_ylim(ymin, ymax)
    plt.xlabel('Tiempo')
    plt.ylabel('Nivel (m.s.n.m)')
    plt.title(name[i])
    plt.grid( which='both',linestyle='dotted')
    plt.grid(linestyle='dotted')
    plt.legend(('Observado', 'Simulado'),loc=8,bbox_to_anchor=(0.5, -0.2),ncol=2)
    fig.autofmt_xdate()
    #plt.show()
    if name[i].find('/')!=-1:
        n=name[i].find('/')
        name[i]=name[i][:n]+'-'+name[i][n+1:]
    plt.savefig(directory + name[i] + '.png', dpi=400, bbox_inches='tight')
    plt.close(fig)
    
#-----------elapsed time---------------------------------------------
print('Tiempo de corrida: '+str((time.time()-t)//60)+' minutos y '+('%.1f' %((time.time()-t)-60*((time.time()-t)//60)))+' segundos.')