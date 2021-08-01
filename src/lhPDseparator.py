import lhExport
from lhPath import *
import pandas as pd
import pickle
def Host(_df, host):
    # df_ip = _df['Host'].value_counts().head(3)
    # # print(type(df_ip))
    # for i in df_ip.index:
    #     # temp = pd.DataFrame(ori.loc[ori['Host'] == i],columns=["col"])
    #     temp = _df.loc[_df['Host'] == host]
    #     temp, filename=str(i + "zzz"))
    return _df.loc[_df['Host']==host]

def allHost(_df):
    print("[allHost]")
    # sol 1
    # list = []
    # df_ip = _df['Host'].value_counts()
    # for ind,i in enumerate(df_ip.index):
    #     print("[allHost] (" +str(ind) +"/"+str(len( df_ip.index)) + ") make dataframe :" + i)
    #     temp = pd.DataFrame(_df.loc[_df['Host'] == i],columns=["col"])
    #     list.append(_df.loc[_df['Host'] == i])

    # sol 2
    # dict에 일치하는 Host의 index번호를 저장
    dict = {}
    for ind, i in enumerate(_df['Host']):
        if(not i in dict):
            dict[i] = []
        dict[i].append(ind)

    list =[]
    for ind,i in enumerate(dict):
        print("[allHost] (" + str(ind) + "/" + str(len(dict)) + ") make dataframe :" + str(i))
        list.append( _df.iloc[dict[i]])

    # [Host별 데이터들을 가진 dataframe을 원소로 갖는 list]
    return list

def allHost_Export(_df,_path=D_ALLHOST):
    print("[allHost_Export]")
    dictN2S ={}
    dictS2N = {}

    # [Host별 데이터들을 가진 dataframe을 원소로 갖는 list]
    a = allHost(_df)
    for ind, i in enumerate(a):
        print("[allHost_Export] (" + str(ind) + "/" + str(len(a)) + ") toCSV : " +str(i['Host'].iloc[0]))
        i.sort_values(['Timestamp'], ascending=[True])
        # i['index_ori'] = i.index
        lhExport.toCsv(i,i.columns,D_ALLHOST,ind)

        dictN2S[ind] = i['Host'].iloc[0]
        dictS2N[i['Host'].iloc[0]] = str(ind)

    # with open('./../doc/info/allhostN2S.pickle', 'wb') as fw, open('../doc/info/allhostS2N.pickle', 'wb') as fw2:
    #     pickle.dump(dictN2S, fw)
    #     pickle.dump(dictS2N, fw2)
    lhExport.dict(F_DIC_ALLHOSTN2S,dictN2S)
    lhExport.dict(F_DIC_ALLHOSTS2N,dictS2N)

    #Host - csv파일 매칭 딕셔너리 반환. csv파일명은 숫자로 대체.
    return dict


