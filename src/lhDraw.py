import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams["font.family"] = 'Malgun Gothic'
plt.rcParams["font.size"] = 16
plt.rcParams["figure.figsize"] = (20, 10)

def lhCrawling(_df):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    print(_df)
    print(_df[['Length_Log', 'Length_Time']])

    ax = plt.scatter(_df['Length_Log'], _df['Length_Time'], s = _df['STDEV']*1000, )
    plt.show()



