import argparse
import pickle
import lhAddColumn
from lhPath import *
import lhAddColumn
import sys
import math;
import os
import pandas as pd
import numpy as np
#//////////////////////////////
#사용시 12, 20, 23의 path수정
#//////////////////////////////

# def GetArgument():
#     ap = argparse.ArgumentParser()
#     ap.add_argument("--path", help="csv directory path", default= r"./../doc/xlsx/Strange_Weblog.csv")
#     args = vars(ap.parse_args())
#     return str(args['path'])
def toXlsx(_df, col , _path=r'./../doc/xlsx/' ,filename="temp", num_seperate = 500000):
    print("수정해야됨")
    return
    #필요한 컬럼만 추출
    if (type(col) == "NoneType"):
        col = _df.columns
    df_to = _df[col]
    for i in range(0,df_to.shape[0],num_seperate):
        if i+num_seperate>df_to.shape[0]:
            print('Document Separating %i: %i ~ %i' % (round(i/ num_seperate), i, df_to.shape[0]))
            df_to.iloc[i:i+df_to.shape[0]].to_excel(_path +"/" + filename + "["+str(round(i/num_seperate))+"].xlsx")
        else:
            print('Document Separating %i: %i ~ %i' % (round(i / num_seperate), i, i + num_seperate))
            df_to.iloc[i:i + num_seperate].to_excel(
                _path + "/" + filename + "[" + str(round(i / num_seperate, 0)) + "].xlsx")

def toCsv(_df, col=None , _path='./' ,filename="values_counts", num_seperate = 500000, _sep=',', _index= False):
    # #필요한 컬럼만 추출
    if(col is None) :
        col = _df.columns
    df_to = _df[col]
    for i in range(0,df_to.shape[0],num_seperate):
        if i+num_seperate>df_to.shape[0]:
            print('Document Separating %i: %i ~ %i' % (round(i/ num_seperate), i, df_to.shape[0]))
            df_to.iloc[i:i + df_to.shape[0]].to_csv(_path +"/" + str(filename) + "["+str(round(i/num_seperate))+"].csv",index=_index,sep=_sep)
        else:
            print('Document Separating %i: %i ~ %i' % (round(i / num_seperate), i, i + num_seperate))
            df_to.iloc[i:i + num_seperate].to_csv(
                _path + "/" + filename + "[" + str(round(i / num_seperate)) + "].csv", sep=_sep,index=_index)

def dict(_path, temp):
    with open(_path, 'wb') as fw:
        print("Writing dict file at " + _path)
        pickle.dump(temp, fw)

def unique(_df, _string):
    print(_df.columns)
    if(_string in _df.columns):
        # pd.Series.unique()
        print(_df[_string].unique())
        toCsv(pd.DataFrame(_df[_string].unique()),filename="unique_"+_string+".csv")
    else:
        print("lhExport : unique : No column " + _string)
        return -1

# def main():
#     global df_ori, path_proj
#     ori = pd.read_csv(r"./../doc/xlsx/Strange_Weblog.csv")
#     print(ori.columns)
#

    # toCsv(ori,ori.columns,filename="Strange_Weblog")


def addlabeledCSV(_df, _filename="Strange_Weblog_Labeled"):
    # print("[labeled] : ", _df.columns)
    list_label=[]
    list_label_except=[]
    # lhAddColumn.addlabel(_df)
    for i in range(_df.shape[0]):
        if(_df['Index_ori'].iloc[i] in lhAddColumn.dict_label):
            list_label.append(lhAddColumn.dict_label[_df['Index_ori'].iloc[i]])
        else:
            list_label.append(None)
            list_label_except.append(i)


    pd_lable = pd.DataFrame(list_label, columns=["Label"])
    _df = pd.concat([_df, pd_lable], axis=1)
    toCsv(_df,_df.columns,_path=D_LABELED, filename=_filename)
    # print("num label : ", _df.shape[0] - len(list_label_except))