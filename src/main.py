import re
from lhPath import *
import lhExport
import lhImportor
import lhParser
import lhDetector
import lhPDseparator
import lhAddColumn
import pandas as pd
import numpy as np
import pickle
import datetime

import os


re.compile('path')
def testCredential():
    ori = pd.read_csv(F_LOGORI)
    # ori['Index_ori'] = ori.index
    # lhPDseparator.allHost_Export(ori)

    # for i in os.listdir(D_ALLHOST):
    #     try:
    #         host = pd.read_csv(D_ALLHOST+"/" + i)
    #         lhDetector.DetectCridential(host,file=i,_term_s=20,_low_num=5)
    #     except:
    #         print(i + "read fail")

    # ori = lhAddColumn.addlabel(ori, ["Credential"])
    # lhExport.toCsv(ori, col=ori.columns, _path=D_TEST, filename="test_credential")
    #

    # d = lhImportor.dict(F_DIC_ALLHOSTS2N)
    # print(d["188.45.31.10"])
    # lhDetector.DetectCridential(host, file="testC", _term_s=20, _low_num=5)

    # 크리덴셜 사례 "188.45.31.10"
    host = pd.read_csv(D_ALLHOST + "/3450[0].csv")
    lhDetector.DetectCridential(host, file="188.45.31.10", _term_s=20, _low_num=5)
def ImportWithIP(list_host, _getFIleNum = False):
    hostS2N = lhImportor.dict(F_DIC_ALLHOSTS2N)

    for i in list_host:
        file = hostS2N[i]
        if _getFIleNum:
            print("%s => %s"%(i,file))
        df = pd.read_csv(D_ALLHOST + "/" + file + "[0].csv")
        lhDetector.DetectCridential(df,_term_s=40,file=i)

def testCrowling():
    # file = "654"
    # list_host = ["14.135.56.110", "112.112.181.134", "188.45.31.30", "188.45.31.10", "188.45.31.20", "188.45.31.40", "14.135.56.140", "14.135.56.130", "14.135.56.120"]
    # pd1 = pd.read_csv(D_ALLHOST + "/" + file  + "[0].csv")
    # pd1 = lhDetector.DetectCrowling(pd1,_terms_s=20,_low_num=5,file=file)
    # lhExport.toCsv(pd1,filename="654_labeled")

    # list_host = ["14.135.56.110", "112.112.181.134", "188.45.31.30", "188.45.31.10", "188.45.31.20", "188.45.31.40", "14.135.56.140", "14.135.56.130", "14.135.56.120"]
    list_result = []
    list_file = []
    for i in os.listdir(D_ALLHOST):
        file = i
        print("[testCrowling : ",file)
        df = pd.read_csv(D_ALLHOST  + file )


        result = lhDetector.DetectCrowling(df,_terms_s=20,_low_num=5,file=file)
        # if len(result) == 0:
        #     result = [0]
        #
        # print(max(result))
        # list_file.append(i)
        # list_result.append(max(result))

        # pd.DataFrame(result).to_csv(D_XLSX + "testCrowling/" + file + ".csv")
        for i in result.keys():
            print("times : " , i)
            print("dates : " , result[i])

    print(pd.DataFrame({'file' : list_file, 'result' : list_result}).to_csv("zzz.csv"))
def convertWebLogFormat():
    pd1 = pd.read_csv(F_LOGORI)

    pd1[['empty1', 'empty2']] = "-"
    print(pd1.columns)
    # ['Timestamp', 'Method', 'Protocol', 'Status', 'Referer', 'Path', 'Host',
    #        'UA', 'Payload', 'Bytes', 'empty1', 'empty2'],

    pd1['Referer'] = "\"" + pd1['Referer'] + "\""
    pd1['UA'] = "\"" + pd1['UA'] + "\""
    pd1['Timestamp'] = pd.to_datetime(pd1['Timestamp'], format="%Y-%m-%d %H:%M:%S")
    pd1['Timestamp'] = pd1['Timestamp'].dt.strftime("[%d/%b/%Y:%H:%M:%S-0700]")
    # pd1['Timestamp2'] = '[' +pd1['Timestamp'].day + '/'
    pd1['Method'] = "\"" + pd1['Method'] + " " + pd1['Path'] + " " + pd1["Protocol"] + "\""
    pd1 = pd1[['Host', 'empty1', 'empty2', 'Timestamp', 'Method', 'Status', 'Bytes', 'Referer', 'UA']]
    print(pd1)
    # 출력
    # lhExport.toCsv(pd1, filename="StrangeWeblog_changed", _sep=' ', _index=False)
    pd1.to_csv("./StrangeWeblog_changed.csv", index=False, sep=' ')
def init():
    #1 원본파일 불러와 판다스로 생성 # 파일만 F_LOGORI에서 F_LOG0로 변경해서 테스트 중
    ori = pd.read_csv(F_LOGORI, encoding='utf-8')
    ori['Index_ori'] = ori.index
    ori = ori[['Index_ori','Timestamp', 'Method', 'Protocol', 'Status', 'Referer', 'Path', 'Host', 'UA', 'Payload', 'Bytes']]
    dict_label={}

    #2 "/doc/allHost" 디렉토리에 호스트별로 나눈 로그파일 저장함. 파일명은 에러방지를 위해 숫자로 지정.
    # "/info/allh~~ 에 저장된 매칭 테이블을 이용해 호스트명-로그파일 변환 가능
    lhPDseparator.allHost_Export(ori)

    #3 파일명 -> IP변환 매핑 딕셔너리 불러옴
    hostN2S = lhImportor.dict(F_DIC_ALLHOSTN2S)



    # 4 ALLHOST에 분할된 로그파일들에게서 분석
    list_FilesSTD = {}
    for i in os.listdir(D_ALLHOST)[0:2]:
        file = i[0:-7]
        # print("Analizing file : ", file)
        df_temp =  pd.read_csv(D_ALLHOST+"\\" + i)
        lhDetector.DetectTimediff( _df=df_temp, _term_s=30, _low_num=2, file=file)




    # 5. 분석결과 보기
    # lhExport.addlabeledCSV(ori)
def dev():
    #1 원본파일 불러와 판다스로 생성 # 파일만 F_LOGORI에서 F_LOG0로 변경해서 테스트 중
    ori = pd.read_csv(F_LOGORI, encoding='utf-8')
    ori['Index_ori'] = ori.index
    ori = ori[['Index_ori','Timestamp', 'Method', 'Protocol', 'Status', 'Referer', 'Path', 'Host', 'UA', 'Payload', 'Bytes']]
    dict_label={}

    #2 "/doc/allHost" 디렉토리에 호스트별로 나눈 로그파일 저장함. 파일명은 에러방지를 위해 숫자로 지정.
    # "/info/allh~~ 에 저장된 매칭 테이블을 이용해 호스트명-로그파일 변환 가능
    # lhPDseparator.allHost_Export(ori)

    #3 파일명 -> IP변환 매핑 딕셔너리 불러옴
    hostN2S = lhImportor.dict(F_DIC_ALLHOSTN2S)

    # 4 ALLHOST에 분할된 로그파일들 분석
    list_FilesSTD = {}
    for i in os.listdir(D_ALLHOST)[0:2]:
        file = i[0:-7]
        # print("Analizing file : ", file)
        df_file =  pd.read_csv(D_ALLHOST+"/" + i)
        lhDetector.DetectTimediff( _df=df_file, _term_s=30, _low_num=2, file=file, type = 2)
        lhDetector.DetectCridential(_df=df_file, _term_s=20, _low_num=30, file=file)
        df_file = lhAddColumn.addlabel(df_file, ['StrangeValue', 'Credential'])
        lhExport.toCsv(_df=df_file, col=df_file.columns, filename=file + "_labeled")

    # lhExport.addlabeledCSV(_df=df_file,filename="StrangeWeblog_labeled")


    # 5. 분석결과 보기
    # lhExport.addlabeledCSV(ori)
def mapping(list_host = 'Host'):

    # F_DIC_ALLHOSTS2N가 제대로 되어있지않는 경우 아래 코드 실행
    # ori = pd.read_csv(F_LOGORI, encoding='utf-8')
    # ori['Index_ori'] = ori.index
    # ori = ori[
    #     ['Index_ori', 'Timestamp', 'Method', 'Protocol', 'Status', 'Referer', 'Path', 'Host', 'UA', 'Payload', 'Bytes']]
    # lhPDseparator.allHost_Export(ori)

    hostN2S = lhImportor.dict(F_DIC_ALLHOSTS2N)
    # print(hostN2S.keys())
    for i in list_host:
        print("{0} = {1}".format(i, hostN2S[i]))
def CheckHost(Host):
    answer = re.findall("[\d]+.[\d].[\d].[\d]",str(Host))
    if(len(answer) != 0):
        return answer[0]
    else:
        return ""
def main():
    global ori
    # init() #기본 동작
    # dev() #개발용
    # testCredential()
    # convertWebLogFormat()
    # testCrowling()

    # ori = pd.read_csv(F_LOGORI,encoding='utf-8')
    # lhDetector.DecectCridential(ori)
    # 9000번이 포함된 log
    # mask = [False for i in range(ori.shape[0])]
    # for i in ori.columns:
    #
    #     if(ori[i].dtype == "object" and i != 'UA'):
    #         print(i)
    #         mask_temp = ori[i].str.contains("9000")
    #         mask = mask_temp | mask
    # mask2 = ori['Payload'].str.contains('log')
    # for i in range(len(mask2)):
    #     mask[i] = mask[i] & (not mask2[i])
    #
    # lhExport.toCsv(ori[mask], filename="zz")

    # 101.224.32.28을 refer로 구별
    # df_101 = ori[ori['Host'] == "101.224.32.28"]
    # df_101_ref1 =df_101[df_101['Referer'] == "\"-\""]
    # lhExport.toCsv(df_101_ref1, filename="df_101_Strangeref")

    # mask = [False for i in range(ori.shape[0])]
    # for i in ori.columns:
    #
    #     if(ori[i].dtype == "object"):
    #
    #         mask_temp = ori[i].str.contains("Hello")
    #         mask = mask_temp | mask
    #
    # lhExport.toCsv(ori[mask], filename="Hello")

    # Host별 Path에 접속한 날짜 가지수수
    # list_file = []
    # list_max = []
    # for i in os.listdir(D_ALLHOST):
    #
    #     host = pd.read_csv(D_ALLHOST + str(i))
    #     df_date = pd.to_datetime(host['Timestamp'], format="%Y-%m-%d %H:%M:%S")
    #     host['Date'] = df_date.dt.date
    #     host['Time'] = df_date.dt.time
    #     df_date = host[['Path', 'Date', 'Time']]
    #     df_date.drop_duplicates(inplace=True)
    ##     lhExport.toCsv(_df=df_date, _path= D_XLSX + "testCrowling/", filename=i[0:-7])
    ##     df_date.to_csv(D_XLSX + "/testCrowling/" + i[0:-7] + ".csv" )
        #
        #
        # df_sorted = df_date.groupby(['Path']).count().sort_values(by='Date', ascending=False).head(5)
        # if(df_sorted['Date'].max() != 1):
        #     list_file.append(i)
        #     list_max.append(df_sorted['Date'].max())
        #     print(i , df_sorted['Date'].max() )
    # df_result = pd.DataFrame({"file" : list_file, "Max" : list_max}).sort_values('Max')
    # df_result.to_csv("./Host_PathTry.csv")
    print(ImportWithIP(['100.200.156.222','101.224.32.28','112.112.181.134','14.135.56.110','14.135.56.120','14.135.56.130','14.135.56.140','188.45.31.10','188.45.31.20','188.45.31.30','188.45.31.40',],_getFIleNum=True))











main()