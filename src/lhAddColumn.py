import pandas as pd
import datetime
import lhExport

dict_StrangeValue = {}
dict_Credential = {}
dict_Crowling = {}
dict_label = {"StrangeValue": dict_StrangeValue, "Credential": dict_Credential, "Crowling" : dict_Crowling}


def __timedelta2int(td):
    if type(td) == pd._libs.tslibs.timedeltas.Timedelta or type(td) == type(datetime.timedelta(seconds=1)):
        res = + (td.seconds + td.days * 24 * 3600)
        return res
    else:
        if(td == 0):
            return 0
        return -1


def __addTimedelta(_df, _limit):
    list = []
    list_con = []
    list_timelength = []
    list_avg=[]

    con_cnt = 0
    list_time=[]

    time_prev = datetime.datetime(year=1, month=1, day=1, hour=1, minute=1, second=1)
    time_start = datetime.datetime(year=1, month=1, day=1, hour=1, minute=1, second=1)

    for idx, i in enumerate(_df['Timestamp']):
        try:
            time_now = datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
        except:
            time_now = datetime.datetime.strptime(i, "%Y-%m-%d %H:%M")

        # list_con = 연속의 시작되는 부분
        if time_now - time_prev > datetime.timedelta(seconds=_limit):
            # print("p : ", time_prev, " n : ", time_now, "n-p : ", (time_now - time_prev), " endidx : ", idx-1)
            list.append(None)
            list_timelength.append(0)
            list_con.append(idx)
            time_start = time_now
            # if(len(list_time) != 0):
            #     list_avg.append(sum(list_time)/len(list_time))
            # else:
            #     list_avg.append(0)
        else:
            list.append(time_now - time_prev)
            list_timelength.append(time_now - time_start)

            # list_time.append(__timedelta2int(time_now - time_prev))


            # print(type(time_now - time_start))
        # print("p : ", time_prev, " n : ", time_now, "n-p : ", (time_now - time_prev))
        time_prev = time_now

    # print("시바 : ", list_con[len(list_con)-1])
    list_con.append(idx + 1)
    temp = pd.Series(list, name= "Timediff").map(lambda x: __timedelta2int(x))
    temp2 = pd.Series(list_timelength,name = "Timelength").map(lambda x: __timedelta2int(x))

    _df = pd.concat([_df, temp, temp2], axis=1)
    # print("lc : ", list_con)
    return _df, list_con, list_avg


def setlabel(_list_label_name, _df, _range, mark):
    # range는 들어온 _df기준
    # print("setlabel : ", _df.columns)
    if(not _list_label_name in dict_label):
        print("[error:setlabel] : 존재하지않는 라벨 명입니다")
        return

    list_oriidx = []
    list_changed = []
    if (type(_range) == type([])):
        for i in _range:
            if (_df['Index_ori'].iloc[i] in dict_label[_list_label_name]):
                list_changed.append(_df['Index_ori'].iloc[i])


            dict_label[_list_label_name][_df['Index_ori'].iloc[i]] = mark
            # print("[setLabel] {0} -> {1} : {2}".format(_df['Index_ori'].iloc[i],i,mark))
            list_oriidx.append(_df['Index_ori'].iloc[i])
    else:
        print("[error]label range is not list!!", type(_range))
    if (len(list_changed) != 0):
        print("[    Mark changed to {0} : {1}".format(mark, list_changed))


def addlabel(_df, list_label_name):
    list_label = []
    list_except = []
    for i in range(len(list_label_name)):
        list_label.append([])
        list_except.append([])
        if (not list_label_name[i] in dict_label):
            print("라벨 이름을 잘못 입력했습니다")
            return

    for i in range(_df.shape[0]):
        for jidx, j in enumerate(list_label_name):
            if (_df['Index_ori'].iloc[i] in dict_label[j]):
                list_label[jidx].append(dict_label[j][_df['Index_ori'].iloc[i]])
            else:
                list_except[jidx].append(i)
                list_label[jidx].append(None)

    for jidx, j in enumerate(list_label_name):
        np_label = pd.DataFrame(list_label[jidx], columns=[j])
        _df = pd.concat([_df, np_label], axis=1)
        print("[Addlabel] {0} : ".format(j), _df.shape[0] - len(list_except))
    return _df


def setStrange(_df, _STRANGEVALUE, STDEV):
    for j in range(STDEV[0], STDEV[0] + STDEV[1]):
        if (j == STDEV[0] or j == STDEV[0] + STDEV[1] - 1):
            dict_StrangeValue[_df['Index_ori'].iloc[j]] = None
        else:
            dict_StrangeValue[_df['Index_ori'].iloc[j]] = _STRANGEVALUE


def setBasedSTDEV(_df, _STDEV):
    for i in range(_STDEV[0], _STDEV[0] + _STDEV[1]):
        if (i == _STDEV[0] or i == _STDEV[0] + _STDEV[1] - 1):
            dict_Credential[_df['Index_ori'].iloc[i]] = None
        else:
            dict_Credential[_df['Index_ori'].iloc[i]] = "Cred"


def addcredential(_df):
    list_credential = []
    list_except = []
    for i in range(_df.shape[0]):
        if (_df['Index_ori'].iloc[i] in dict_Credential):
            list_credential.append(dict_Credential[_df['Index_ori'].iloc[i]])
        else:
            list_except.append(i)
            list_credential.append(None)
    np_label = pd.DataFrame(list_credential, columns=['credential'])
    # print("[AddStrange] : ", _df.shape[0] - len(list_except))
    return pd.concat([_df, np_label], axis=1)


def addStrange(_df):
    list_strange = []
    list_except = []
    for i in range(_df.shape[0]):
        if (_df['Index_ori'].iloc[i] in dict_StrangeValue):
            list_strange.append(dict_StrangeValue[_df['Index_ori'].iloc[i]])
        else:
            list_except.append(i)
            list_strange.append(None)
    np_label = pd.DataFrame(list_strange, columns=['StrangeValue'])
    # print("[AddStrange] : ", _df.shape[0] - len(list_except))
    return pd.concat([_df, np_label], axis=1)
