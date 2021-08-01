import numpy
import pandas as pd

def Timeparser(_df):
    temp =[]
    for i in _df['Timestamp'].head(3):
        date,time = i.split(' ')
        tY,tM,tD = date.split('-')
        th,tm,ts = time.split(':')
        temp.append([tY,tM,tD, th, tm,ts])
    # print(pd.DataFrame(temp, columns = ['Y','M','D','h','t','s']))
    df_t = pd.DataFrame(temp, columns = ['Y','M','D','h','t','s'])

    return pd.concat([_df.head(3),df_t],axis=1)
