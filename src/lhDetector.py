import lhAnalizer
import lhExport
import lhAddColumn
import lhDraw
import lhPath
import re
import math
import pandas as pd
re1 = re.compile("/login/")
def getValue_tryLogin(_df, _STDEV, _i):
    acountEntropy_df = _df['Payload'].iloc[_STDEV[0][_i]:_STDEV[0][_i] + _STDEV[1][_i]].map(lambda x: GetIDIP(x))
    return acountEntropy_df.unique().shape[0]

def getValue_Credential(_value_tryLogin, _logLength, _value_TimeLength):
    # value_Credential = (value_tryLogin/STDEV[1][i])/((1+math.log(value_timelength)))
    if(_value_TimeLength>60):
        print("[Case] LongLog")
        return (_value_tryLogin / _logLength) / 1e9
    else:
        return (_value_tryLogin / _logLength) / (1.01 ** (_value_TimeLength))

def DetectTimediff(_df,file, _term_s = 30, _low_num = 5, _low_STRANGEVALUE = 1500, type = 1):
    # 조건에 맞는 연속로그 중에서 이상수치조건에 맞는 값들을 탐색
    # print("[DetectTimediff] col ", _df.columns)

    # 1. 로그들을 연속로그들로 나누어서 [연속로그 시작인덱스, 개수, 분산] 리스트들을 받아옴
    STDEV = lhAnalizer.GetSequentialLog(_df=_df, _time=_term_s, _n=_low_num)

    list_index = []
    list_num = []
    list_STV = []

    # 2. 이상수치 조건에 맞는 값들만 추림
    for i in range(len(STDEV[0]) - 1):
        # (STRANGEVALue)연속로그 개수 / 시간분산이 일정 일정 수치 이상이거나 시간분산이 0인경우 이상값으로 추정
        if(STDEV[2][i]!=0):
            STRANGEVALUE = STDEV[1][i] * STDEV[1][i] / STDEV[2][i]

        else:
            STRANGEVALUE = 1e9
        print(
            "[Strange] {0}, {1}, : {2} : {3}".format(STDEV[0][i], STDEV[0][i] + STDEV[1][i]-1, STDEV[2][i], STRANGEVALUE))
        # lhAddColumn.setStrange(_df,STRANGEVALUE,STDEV=[STDEV[0][i],STDEV[1][i],STDEV[2][i]])

        if (STDEV[2][i] == 0 or STRANGEVALUE > _low_STRANGEVALUE):
            # print("[DetectTimediff] {0} ~ {1} is doubtable with {2}".format(STDEV[0][i], STDEV[0][i] + STDEV[1][i]-1, STRANGEVALUE))

            # F_LOGORI 대상 라벨링
            lhAddColumn.setlabel("StrangeValue", _df, list(range(STDEV[0][i],STDEV[0][i] + STDEV[1][i] )),file)
            list_index.append(STDEV[0][i])
            list_num.append(STDEV[1][i])
            list_STV.append(STRANGEVALUE)

    # (조건부 3.) 분석용
    if type == 2:
        _df4dev = _df
        # _df4dev = lhAddColumn.addStrange(_df=_df4dev)
        # _df4dev = lhAddColumn.addlabel(_df=_df4dev)
        # _df4dev, a = lhAddColumn.__addTimedelta(_df=_df4dev,_limit=30)
        lhExport.toCsv(_df=_df4dev,_path=lhPath.D_DEV,filename=file+"_dev")
    # 4. 라벨링 파일 생성
    elif (len(STDEV[0]) != 0):
        print("Analizing file : ", file)
        # for j in range(len(STDEV[0])):
        #     print(STDEV[0][j], STDEV[1][j], STDEV[2][j])

        lhAddColumn.addlabel(_df, "Strange")
        # lhExport.addlabeledCSV(_df=_df, _filename=file)

    #5. 결과 화면 표시
    print("[DetectTimediff] file : {0}, part : {1}".format(file, len(STDEV[0])-1))
    print("")
    # return [list_index, list_num, list_STV]

def GetIDIP(x):
    r = re.compile("log=(.+)&pwd=(.+)")
    x = re.findall(r, str(x))
    if len(x) > 0:
        return x[0]
    return None
def GetIDIP2(x):
    r1 = re.compile("log=(.+)")
    r2 = re.compile("pwd=(.+)")
    id = []
    pw = []
    list = str(x).split("&")
    for i in list:
        if (id == []): id = re.findall(r1, str(i))
        if (pw == []): pw = re.findall(r2, str(i))

    if len(id) > 0 and len(pw) > 0:
        # if id in dict_IDPW:
        #     if pw in dict_IDPW[id]:
        #         dict_IDPW[id][pw].append()
        return id,pw
    else:
        return None,None

def DetectCridential(_df, file = "nofilename", _term_s = 1000, _low_num = 5, _VALUE = 0.7, _STDEV = 5,_threshold = 2):
    VALUE = 0
    # 1. 로그들을 연속로그들로 나누어서 [연속로그 시작인덱스, 개수, 분산] 리스트들을 받아옴
    print("%s의 연속로그 결과 \n\t(최소연속시간 : %d초 최소개수 : %d개)" % (file,_term_s, _low_num))

    STDEV = lhAnalizer.GetSequentialLog(_df=_df, _time=_term_s, _n=_low_num)
    for i in range(len(STDEV[0]) - 1):
        # 무시
        # continuous_df = _df['Path'].iloc[STDEV[0][i]:STDEV[0][i] + STDEV[1][i]].str.lower()
        # continuous_df = continuous_df.str.contains('/wp-login.php').value_counts()

        # 크레덴셜 판별
        value_tryLogin = getValue_tryLogin(_df,STDEV,i)
        value_timelength = STDEV[3][i]

        value_Credential = getValue_Credential(value_tryLogin, STDEV[1][i] , value_timelength)

        # 결과 출력
        print("[Credential] %d ~ %d [%d] , Value(로그인시도비율: %f, 로그인시도시간: %d) STDEV: %d 결과값 : %f)" %
              (STDEV[0][i], STDEV[0][i] + STDEV[1][i] - 1,STDEV[1][i], value_tryLogin/STDEV[1][i], value_timelength,STDEV[2][i], value_Credential))

        # 라벨링
        # if(value_tryLogin > 10 and STDEV[2][i] < 3):
        # if(Value_Credential > 100):
        #     lhAddColumn.setBasedSTDEV(_df, [STDEV[0][i], STDEV[1][i], STDEV[2][i]])

def DetectCrowling(_df,_terms_s, _low_num, file="noname"):
    STDEV = lhAnalizer.GetSequentialLog(_df=_df, _time=_terms_s, _n=_low_num)
    value_refererUnknown = 0

    # 분석결과 DF
    df_result = pd.DataFrame({'Index' : STDEV[0][0:-1], 'Length_Log' : STDEV[1], 'STDEV' : STDEV[2], 'Length_Time' : STDEV[3], 'TimeStart' : STDEV[4]})
    df_result['File'] =  file
    # Ver1
    # list_value_refererUnknown = []
    # list_value_refererEntropy = []
    # list_value_stdev = []
    #
    # for i in range(len(STDEV[0])-1):
    #     print("[Crowling] start : {0}, loglength : {1}, timdeSTDEV : {2}, timelength :  {3}".format(STDEV[0][i],STDEV[1][i],STDEV[2][i],STDEV[3][i]))
    #     df_sliced = _df.iloc[STDEV[0][i]:STDEV[0][i] + STDEV[1][i]]
    #     list_value_stdev.append(STDEV[2][i])
    #
    #     # Get value_refererUnknown
    #     list_domainCount = df_sliced['Referer'].value_counts()
    #     if not "\"-\"" in list_domainCount.index:
    #         list_value_refererUnknown.append(0)
    #     else:
    #         list_value_refererUnknown.append(list_domainCount.loc["\"-\""] / list_domainCount.sum())
    #
    #     # Get value_refererEntropy
    #     list_value_refererEntropy.append(len(df_sliced['Path'].unique())/df_sliced['Path'].shape[0])
    #     print("Unknown : " , list_value_refererUnknown, "Entropy : ", list_value_refererEntropy[i], "STDEV : " , list_value_stdev[i])
    #
    #     if list_value_stdev[i]>0.7 and list_value_refererEntropy[i] > 0.7 and list_value_stdev[i] >0.3 and list_value_stdev[i] < 0.7:
    #         lhAddColumn.setlabel("Crowling",_df, list(range(STDEV[0][i],STDEV[0][i] + STDEV[1][i])),"Crowling")
    #
    # _df = lhAddColumn.addlabel(_df,["Crowling"])
    # # df_result.append(pd.Series(list_value_refererEntropy, name="RefererEntropy"), ignore_index=True)
    # # df_result.append(pd.Series(list_value_refererUnknown, name="RefererUnknown"), ignore_index=True)
    # lhDraw.lhCrawling(df_result)
    # print(df_result)
    # Ver2

    # 같은 시간차이를 가지는 로그들 찾기
    # df = pd.to_datetime(df_result['TimeStart'], format= "%Y-%m-%d %H:%M")
    # dict_timeRegular = {}
    # df_times = pd.DataFrame()
    # df_times['Date'] = df.dt.date
    # df_times['Time'] = df.dt.time

    # for i in range(df_times.shape[0]):
    #     date = df_times.loc[i, 'Date']
    #     time = df_times.loc[i, 'Time']

        # if time in dict_timeRegular:
        #     dict_timeRegular[time].add(date)

        # else:
        #     dict_timeRegular[time] = set()
        #     dict_timeRegular[time].add(date)

    # list_count = []

    # for i in dict_timeRegular.keys():
    #     list_count.append(len(dict_timeRegular[i]))

    # return dict_timeRegular

def DecectCridential2(_df):
    dict_IDPW = {}
    _df2 = _df.copy()
    mask = _df2['Payload'].str.contains('log=|pwd=', na=False)
    _df2['Payload'] = _df2['Payload'].map(lambda x:GetIDIP2(x))
    print(_df2.loc[mask,'Payload'].map(lambda x : x[1]))
    _df3 =pd.DataFrame()
    _df3['Host'] = _df2.loc[mask,'Host']
    _df3['Timestamp'] = _df2.loc[mask,'Timestamp']
    _df3['Id'] = _df2.loc[mask,'Payload'].map(lambda x : x[0][0])
    _df3['Pw'] = _df2.loc[mask,'Payload'].map(lambda x : x[1][0])
    _df3['Bytes'] = _df2.loc[mask,'Bytes']
    _df3.drop_duplicates(inplace=True)
    # _df3 = _df3.set_index(['Id','Pw'])
    _df3.sort_index(inplace=True)

    # _df3.to_csv("./Login_try.csv")
    print(_df3.columns)


    # _df['Payload'].value_counts().to_csv("zz2.csv")





