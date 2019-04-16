import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

from datetime import datetime
from dateutil import tz

green1 = '#b2df8a'
green2 ='#33a02c'
blue1 = '#a6cee3'
blue2 = '#1f78b4'
red1 ='#fb9a99'
red2 = '#e31a1c'
purp1 = '#cab2d6'
purp2 = '#6a3d9a'
orange1 = '#fdbf6f'
orange2 = '#ff7f00'

def plottingIndividual(person):
    dfFB = pd.read_csv('fb.csv',index_col=False)
    dfFB = dfFB[['person', 'timestamp_ms','content','category','date']]

    dfSMS = pd.read_csv('sms.csv',index_col=False)
    dfSMS = dfSMS[['person', 'timestamp_ms','content','category','date']]

    dfMessages = dfSMS.append(dfFB, ignore_index=True, sort=False)

    dfMessages['timestamp_ms'] = dfMessages['timestamp_ms'].astype(int)
    dfMessages['date'] = dfMessages['timestamp_ms']/1000
    dfMessages['date'] = dfMessages['date'].astype(int)
    dfMessages['date'] = pd.to_datetime(dfMessages['date'], unit='s') 
    dfMessages['date'] = dfMessages['date'].dt.tz_localize('utc').dt.tz_convert('US/Pacific')
    dfMessages['hour'] = dfMessages['date'].dt.hour
    dfMessages['day'] = dfMessages['date'].dt.weekday

    dfPerson = dfMessages.loc[dfMessages['person'] == person].copy()

    totalMessagesPerson = list(dfPerson['date'])
    totalMessagesPersonHour = list(dfPerson['hour'])
    totalMessagesPersonDay = list(dfPerson['day'])

    sentPersonSMS = list(dfPerson[dfPerson['category'] == 'sent sms']['date'])
    receivedPersonSMS = list(dfPerson[dfPerson['category'] == 'received sms']['date'])
    sentPersonFB = list(dfPerson[dfPerson['category'] == 'sent facebook']['date'])
    receivedPersonFB = list(dfPerson[dfPerson['category'] == 'received facebook']['date'])

    sentPerson = list(dfPerson[dfPerson['category'].str.contains('sent')]['date'])
    receivedPerson = list(dfPerson[dfPerson['category'].str.contains('received')]['date'])

    smsPerson = list(dfPerson[dfPerson['category'].str.contains('sms')]['date'])
    fbPerson = list(dfPerson[dfPerson['category'].str.contains('facebook')]['date'])

    with plt.style.context('ggplot'):
        plt.figure()
        fig, ax = plt.subplots(figsize=(20,7))
        ax.hist([sentPerson, receivedPerson], 
                label=['Luke',person], 
                bins = 40, 
                stacked=False,
                color=([blue1, red1]))
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(16)
        fig.autofmt_xdate()
        ax.legend(prop={'size':16})
        ax.grid(False)
        ax.set_ylabel('Messages')
        ax.set_title('Messages Exchanged by Month',y=.9)
        #ax.set_xticklabels(['July 2015','Jan 2016','July 2016','Jan 2017','July 2017','Jan 2018','July 2018','Jan 2019'])

        plt.figure()
        fig, ax = plt.subplots(figsize=(15,7))
        u, inv = np.unique(totalMessagesPersonHour, return_inverse=True)
        counts = np.bincount(inv)
        plt.bar(u, counts, width=0.7, color=blue1)
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(16)
        fig.autofmt_xdate()
        #ax.legend(prop={'size':16})
        ax.grid(False)
        ax.set_xticks(np.arange(0,24,1))
        ax.set_ylabel('Messages')
        ax.set_title('Messages Exchanged by Hour in Day',y=.9)
        #ax.set_ylim(top=17000)
        ax.set_xticklabels(['12 AM','1','2','3','4','5','6','7','8','9','10','11','12','1',
                           '2','3','4','5','6','7','8','9','10','11'])

        plt.figure()
        fig, ax = plt.subplots(figsize=(5,7))
        u, inv = np.unique(totalMessagesPersonDay, return_inverse=True)
        counts = np.bincount(inv)
        plt.bar(u, counts, width=0.7, color=blue1)
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(16)
        fig.autofmt_xdate()
        #ax.legend(prop={'size':16})
        ax.grid(False)
        ax.set_xticks(np.arange(0,7,1))
        ax.set_ylabel('Messages')
        ax.set_title('Messages Exchanged by Day',y=.9)
        ax.set_xticklabels(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])

        plt.figure()
        fig, ax = plt.subplots(figsize=(20,7))
        ax.hist([smsPerson, fbPerson], 
                label=['Texting','Facebook'], 
                bins = 50, 
                stacked=False,
                color=([green1, blue1]))
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(16)
        fig.autofmt_xdate()
        ax.legend(prop={'size':16})
        ax.grid(False)
        ax.set_ylabel('Messages')
        ax.set_title('Monthly Messages by Messaging Medium', y=.9)
        #ax.set_xticklabels(['July 2015','Jan 2016','July 2016','Jan 2017','July 2017','Jan 2018','July 2018','Jan 2019'])
        plt.show()

