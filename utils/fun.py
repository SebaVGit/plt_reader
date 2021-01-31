
import sys
import glob
import os
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date
from datetime import timedelta
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
import locale
from collections import OrderedDict
from tqdm import tqdm
import time
#-------------------skip matplotlib warning-------------------------------
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#------------------------Function------------------------------------------
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