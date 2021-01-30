# -*- coding: utf-8 -*-
"""
@author: Sebastián Vázquez
"""
from utils.fun import *
import time

if __name__ == '__main__' :
    t = time.time()
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
    plt.rcParams['font.sans-serif'] = 'Calibri' #Calibri or another you want
    plt.rcParams["figure.figsize"] = [12,8.5] #this controls the size of the plots

    #----------This creates the output folder-------
    Ruta = os.getcwd() + '\\'
    directory =  Ruta + 'Plots_Output'
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = directory + '\\'

    # Name of the file
    file_name=input('plt file name?: ')

    #-------------------------------------reading the *.plt file----------------------------------------------
    nivel=pd.read_csv(Ruta+file_name,sep=' ',encoding = "ISO-8859-1",names=[0,1,2,3,4,5,6],skiprows=2)

    #------------------------Para guardar los nombres-----------------------------

    name=nombre(nivel)

    #-----------------------index------------------------------

    indice_sim, indice_obs=indices(nivel)
                
    #-------------------important dates-----------------
    fecha_ini=dt.date.toordinal(date(1999,12,31)) #the initial date minus 1 (in this case is an example of 01/01/2000)
    #date.fromordinal(aux)

    #----------------------------date for the calibration and validation separation--------------------------------
    #fecha_cal=dt.datetime(2015,3,1)
                
    #-----------------------------guardar los datos sim y obs------------------------
    #ticks = [dt.datetime(i, 1, 1) for i in range(2000, 2004, 1)]#control the ticks, add an extra year for the latest in order to get the information of it
    for i in tqdm(range(0,len(indice_sim),1)):
        obs, sim, tiempo_obs, tiempo_sim=datos(nivel,indice_sim,indice_obs,i)
        tiempo_obs=To_Date(tiempo_obs,fecha_ini)
        tiempo_sim=To_Date(tiempo_sim,fecha_ini)
        #-----------------index of both calibration and validation---------------------
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
        dif=ymax-ymin #This is important because of the different behaviours of the wells
        if dif>100:
            delta=dif+50
        else:
            delta=100
        ymin=ymin-(delta-(dif))/2
        ymax=ymax+(delta-(dif))/2
        monthsFmt = mdates.DateFormatter("%b-%Y")
        #----------------set the x axis as you want----------------------
        #minor = mdates.YearLocator(1)
        #years = mdates.YearLocator(2,month=1, day=1)
        #ax.xaxis.set_minor_locator(minor)
        #ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(monthsFmt)
        #------------------------------------------------------
        ax.yaxis.set_minor_locator(tkr.MultipleLocator(5))
        ax.yaxis.set_major_locator(tkr.MultipleLocator(10))
        #------------plot the data--------------------------------
        #ax.set_xticks(ticks)
        ax.plot(tiempo_obs,obs,'bd',tiempo_sim,sim,'r-', markerfacecolor='none')
        #-------------- set the dates if you want----------------------------
        #tiempomin=dt.datetime(2000,1,1)
        #tiempomax=dt.datetime(2002,12,31)
        #ax.set_xlim(tiempomin,tiempomax) #use this if you know your dates
        #------------------------------------------------------------
        ax.set_ylim(ymin, ymax)
        plt.xlabel('Tiempo')
        plt.ylabel('Nivel (m.s.n.m)')
        plt.title(name[i])
        plt.grid( which='both',linestyle='dotted')
        plt.grid(linestyle='dotted')
        plt.legend(('Observado', 'Simulado'),loc=8,bbox_to_anchor=(0.5, -0.2),ncol=2)
        fig.autofmt_xdate()
        if name[i].find('/')!=-1:
            n=name[i].find('/')
            name[i]=name[i][:n]+'-'+name[i][n+1:]
        plt.savefig(directory + name[i] + '.png', dpi=400, bbox_inches='tight')
        plt.close(fig)
        
    #-----------elapsed time---------------------------------------------
    print('Tiempo de corrida: '+str((time.time()-t)//60)+' minutos y '+('%.1f' %((time.time()-t)-60*((time.time()-t)//60)))+' segundos.')