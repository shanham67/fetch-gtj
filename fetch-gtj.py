#!python

#****************** NOTE ********************
#This is my first virtualenv project
#To run it:
# %>source env/bin/activate
# %>python ./fetch-gtj.py

from bs4 import BeautifulSoup
import requests
import re
import datetime

bbn_url = 'https://bbn1.bbnradio.org/english/home/all-programs/gateway-to-joy-elisabeth-elliot'
url = 'https://bbn1.bbnradio.org/english/home/all-programs/gateway-to-joy-elisabeth-elliot/gateway-to-joy-'

page = requests.get(bbn_url)
soup = BeautifulSoup(page.content, 'html.parser')

#
# get all of the titles from the 'calendar' at the bottom of the page
# This creates an array of filenames indexed by day_of_month (i.e. 1 to 31)
# day0, saturdays and sundays will have the value 'No-Show'
#
filenames = []
filenames.append("No-Show") #days are indexed from '1', arrays from '0'
for day in range(1, 31):
    cal_day_link = soup.find('td',class_='simcal-day-'+str(day))
    title_link = cal_day_link.find('span',class_='simcal-event-title')
    if title_link:
        fn =  re.sub('[^\w_.)(-]', '-', title_link.text)+'.m4a'
        print( str(day), fn)
    else:
        fn = "No-Show"

    filenames.append(fn)

today = datetime.date.today()
monday_date = today - datetime.timedelta(days=today.weekday())

i = 0
for day in ('monday','tuesday','wednesday','thursday','friday'):
    day_date = monday_date + datetime.timedelta(days=i)
    if day_date.month == today.month:
        dom = day_date.day
        day_player_page = requests.get(url+day)
        day_player_soup = BeautifulSoup(day_player_page.content,'html.parser')
        su_audio_div = day_player_soup.find('div',class_='su-audio')
        day_str = day_date.year+day_date.month+day_date.day
        if su_audio_div:
            m4a_url = su_audio_div['data-audio']
            fn = day_date.strftime("%Y%m%d")+"-"+filenames[dom]
            print( "wget","-nc -O",fn,m4a_url)
            r = requests.get(m4a_url, allow_redirects=True)
            open(fn,'wb').write(r.content)
        else:
            print ('No m4a found for "' + day + '"')

    else:
        print("Skipping",day,".  It occurs in a different month.")
    i = i + 1

