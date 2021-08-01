import pickle
from lhPath import *
import os
import re
import pandas as pd
def dict(_path):
    with open(_path, 'rb') as fr:
        return pickle.load(fr)

def Host(_ip):
    _dict = dict(F_DIC_ALLHOSTS2N)
    host = _dict[_ip]
    # Host별로 저장된 allHost파일의 이름을 위한 정규표현식
    # r = re.compile('[\d]+\[[\d]+\]\.csv')

    # 특정 ip의 host파일명을 걸러내기위한 정규표현식
    # 파일의 열이 너무 많아 엑셀에서 읽어들일 수 없을 경우 분할해두었음, 이를위함
    regStr = str(host)
    sentence = " ".join(os.listdir(D_ALLHOST))
    r = re.compile(fr'\b{regStr}\[[\d]+\].csv\b')
    files = re.findall(r, sentence)
    sum = pd.DataFrame()
    for i in files:
        temp = pd.read_csv(D_ALLHOST + i)
        sum = pd.concat([sum, temp], axis=1)
    return sum