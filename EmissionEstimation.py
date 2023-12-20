# Import of python related libraries ******************************************
import pandas as pd
import numpy as np
import math
import os
from os import listdir
from os.path import isfile, join
import time
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from tqdm import tqdm
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Base data corresponding to model parameters **************************************
Btable = pd.DataFrame({"Bin":["Bin" + str(i) for i in range(1,24)], 
                       "value":[0 for i in range(1,24)]})
Btable.Bin = Btable.Bin.astype("category")

er = pd.read_csv("emissionrate.csv")
er.Bin = "Bin" + er["Bin"].astype(str)
er.Bin = er.Bin.astype("category")

binfreq = pd.read_csv("Binfrequency.csv").drop(['cartype','weight'],axis=1)

# main ---- Estimation of emissions *************************************************  
readpath_root = 'GPS_Data_individual_HDT'
readfile = [join(readpath_root, f) for f in listdir(readpath_root)] 

writepath_root = 'GPS_Data_individual_HDT_emission'
os.makedirs(writepath_root, exist_ok=True)
writefile = [join(writepath_root, f) for f in listdir(readpath_root)]
for i in range(len(writefile)):
    os.makedirs(writefile[i], exist_ok=True)

def get_Fweight(vu,vl,Vupper,Vlower):
    if Vupper == Vlower:
        y = 1
    elif (vu <= Vupper) & (vl <= Vlower):
        y = (vu-Vlower)/(Vupper-Vlower)
    elif (vu <= Vupper) & (vl >= Vlower):
        y = (vu-vl)/(Vupper-Vlower)
    elif (vu >= Vupper) & (vl >= Vlower):
        y = (Vupper-vl)/(Vupper-Vlower)
    elif (vu >= Vupper) & (vl <= Vlower):
        y = (Vupper-Vlower)/(vu-vl)
    else:
        y = 1
    return y

for date in tqdm(range(len(readfile))):    
    filelist = [join(readfile[date], f) for f in listdir(readfile[date])]     
    writelist = [join(writefile[date], f) for f in listdir(readfile[date])]     
  
    for ID in tqdm(range(len(filelist))): 
        ## Running start time record
        import time
        time_begin = time.time()
        
        raw = pd.read_csv(filelist[ID])
        raw.speed = raw.speed/3.6
        
        ## step1 ---- GPS trajectory segmentation
        dt = 30
        length = math.ceil(len(raw)/dt)
        trip_raw = []
        for i in range(length):
            raw_s = raw[dt*i:dt*(i+1)]
            trip_raw.append(raw_s)
        
        ## step2 ---- Similarity between 1/60-Hz trajectory data and 1-Hz trajectory reference dataset
        Trip_all = []
        for j in range(len(trip_raw)):
            trip = trip_raw[j]
            T = len(trip) 
            Vmean = trip.speed.values.mean()
            Vsd = trip.speed.values.std()
            Vupper = Vmean+2*Vsd
            Vlower = Vmean-2*Vsd

            if (Vupper == Vlower) & (Vupper == 0):
                for k in ['CO','HC','NOx','PM2.5','CO2']:
                    trip.loc[:,k] = 0
                Trip_all.append(trip)
                continue
            
            if T == 1:
                Vmean = trip.speed.mean()
                Vsd = 0
                Vupper = Vmean+2*Vsd
                Vlower = Vmean-2*Vsd
            
            step1 = pd.DataFrame( {"V13":[Vmean], "V14":[Vsd],
                        "vupper":[Vupper], "vlower":[Vlower]}
                        )

            step2 = binfreq[(binfreq.vmean <= Vupper) &  (binfreq.vmean >= Vlower)]
            if len(step2) == 0: 
                step2 = binfreq[(binfreq.vmean <= Vupper) &  (binfreq.vmean >= Vlower*0.2)]

            step2.loc[:,"vupper"] = step2.vmean + 2*step2.vmean
            step2.loc[:,"vlower"] = step2.vmean - 2*step2.vmean
            
            step2["Fweight"] = 1

            conditions=[
                ((step2["vupper"].values<=Vupper)&(step2["vlower"].values<=Vlower)),
            ((step2["vupper"].values<=Vupper)&(step2["vlower"].values>=Vlower)),
            ((step2["vupper"].values>=Vupper)&(step2["vlower"].values>=Vlower)),
            ((step2["vupper"].values>=Vupper)&(step2["vlower"].values<=Vlower)),    
            ]
            
            choices=[
                ((step2["vupper"].values-Vlower)/(Vupper-Vlower)),
            ((step2["vupper"].values-step2["vlower"].values)/(Vupper-Vlower)),
            ((Vupper-step2["vlower"].values)/(Vupper-Vlower)),
            ((Vupper-Vlower)/(step2["vupper"].values-step2["vlower"].values)),
            ]
            
            step2["Fweight"]=np.select(conditions,choices,default=1)
            step2["Fweight"].replace([np.inf,-np.inf], np.nan, inplace=True)
            step2["Fweight"].fillna(1,inplace = True)
            
            ## step3 ---- The normalized frequency of the Opmodes distribution
            step3 = step1.copy()
            for j in range(1,24):
                col = "Bin"+str(j)
                step2.loc[:,col] = step2[col].values * step2["Fweight"].values
                step3.loc[:,col] = step2.loc[:,col].mean(skipna=True)

            total = step3.iloc[0,4:].sum()
            
            for j in range(1,24):
                col = "Bin"+str(j)
                step3[col] = step3.loc[:,col].values/total
            
            ## step4 ---- Emission rate of different species in each trajectory 
            step4 = pd.melt(step3, id_vars = ['V13','V14','vupper','vlower'], var_name='Bin')
            step4.Bin = step4.Bin.astype("category")
            result = step4[['Bin','value']]
            summary = result.merge(er, on="Bin")
            
            ## step5 ---- Emission estimation of different species of the GPS trajectory
            for k in ['CO','HC','NOx','PM2.5','CO2']: 
                summary.loc[:,k] = summary[k]*summary.value
            summary_m =  summary[['CO','HC','NOx','PM2.5','CO2']].sum()*T*60

            for k in ['CO','HC','NOx','PM2.5','CO2']:
                trip.loc[:,k] = summary_m[k]/T
            Trip_all.append(trip)
            
        car_em = pd.concat(Trip_all) 
        car_em.to_csv(writelist[ID], encoding='utf-8-sig', index = 0)
        
        ## Running end time record
        time_end = time.time()
        time = time_end - time_begin
        print('Running time:', time)