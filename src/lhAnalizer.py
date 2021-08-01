import datetime
import lhExport
import lhAddColumn
import pandas as pd
def stDeviation(_df, col):
    return _df[col].std()[0]

def stDeviation2(_df, col, row_start, row_end):
    return _df[col].iloc[row_start:row_end].std()[0]

def __timedelta2int(td):
    if type(td) == pd._libs.tslibs.timedeltas.Timedelta:
        res = + (td.seconds + td.days * 24 * 3600)
        return res
    else:

        return -1

def GetSequentialLog(_df, _time=3000, _n=3):
    STDEV_selected = [[],[]]
    _df_addTimediff = _df
    value_st=[]
    time = []
    list_index = []
    list_loglength = []
    list_stdev = []
    list_timelength=[]
    list_TimeStart = []
    list_Time_Average= []
    # timediff가 추가된 데이터프레임과 연속적인 로그 index를 반환받음.
    _df_addTimediff, index_st, avg_st = lhAddColumn.__addTimedelta(_df_addTimediff,_time)
    # print("[GetTimeSTD] {0} continous connection (more than {1}),  ".format(len(index_st)-1, _n))
    for idx in range(len(index_st)-1):
        if index_st[idx+1] - index_st[idx] >= _n:
            # 로그 개수가 _n개 이하면 버림
            k = index_st[idx]
            v = stDeviation2(_df_addTimediff, ['Timediff'], index_st[idx] + 1, index_st[idx + 1])
            # print("[GetTimedeltaST] {0}~{1} : STDEV : ".format(index_st[idx],index_st[idx+1]-1), v)
            value_st.append(v)

            list_index.append(k)
            list_TimeStart.append(_df_addTimediff.loc[index_st[idx],'Timestamp'])
            list_loglength.append(index_st[idx+1] - index_st[idx])
            list_stdev.append(v)
            list_timelength.append(_df_addTimediff['Timelength'].iloc[index_st[idx+1]-1])
            # list_Time_Average.append(avg_st[idx])
        else:
            # print("[GetTimedeltaST] {0}~{1} : ".format(index_st[idx], index_st[idx + 1] - 1), "Fail")
            value_st.append(-1)

    list_index.append(idx)
    # 연속로그들의 시간분산 출력`

    # for i in range(len(index_st)-1):
    #     print(str( index_st[i] )+ " ~ ", str(index_st[i+1]-1), " : " + str(value_st[i]))

    # STDEV파일에 인덱스와 벨류 정리
    STDEV_all = [index_st,value_st]
    STDEV_selected = [list_index, list_loglength, list_stdev,list_timelength, list_TimeStart]
    return STDEV_selected





