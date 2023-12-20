# Import of python related libraries ******************************************
import pandas as pd
import os
from os import listdir
from os.path import join
import time
import warnings
warnings.filterwarnings('ignore')
from tqdm import tqdm

# Creation of read/write paths and Basic data reading**************************
readpath = 'GPS_Data'
writepath = 'GPS_Data_individual_HDT'

datefile = [i[:-4] for i in listdir(readpath)]
pathfile = [join(readpath, f) for f in listdir(readpath)]
writefile = [join(writepath, f) for f in datefile]
for i in range(len(writefile)):
    os.makedirs(writefile[i], exist_ok=True)

# main ---- Extraction of individual HDT ***************************************
for i in tqdm(range(len(pathfile))):
    data = pd.read_csv(pathfile[i], encoding= 'utf-8')
    data = data.sort_values(by=['plate_id', 'timestamp'], axis=0, ascending=[True,True], inplace=False).reset_index(drop=True) 
    sub_data = data.groupby(['plate_id'],as_index=False)
    for group_name,group_data in tqdm(sub_data):
        group_data.to_csv(join(writefile[i], group_name+'.csv'), encoding='utf-8-sig', index=False)