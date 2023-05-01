from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests as r
import time
import random
import pandas as pd

name_list = []
chords_list = []
keys_list = []

url = 'https://www.e-chords.com/chords/bill-evans/order-hits'
page = r.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
song_names = soup.find_all("div", {"class": "track"})
link_to_songs = [song.find("a", href=True) for song in song_names]

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
for i in range(0,len(link_to_songs)):
    driver.get(link_to_songs[i]['href'])         
    html = driver.page_source
    soup = BeautifulSoup(html)
    key = soup.find('span', {'class': "actualkey"})
    #chords = soup.find_all('div', {"class": "chordtitle"})
    chords = soup.find('pre', {"id": "core"}).find_all('a')
    chords_text = [chord.text for chord in chords]
    if link_to_songs[i].text and key.text and chords_text:
        name_list.append(link_to_songs[i].text)
        keys_list.append(key.text)
        chords_list.append(';'.join(chords_text)) 
    time.sleep(random.randint(0, 2))

chords_df = pd.DataFrame(data={'name': name_list, 'key': keys_list, 'chords': chords_list})
#chords_df.to_csv('bill_evans_chords.csv', index=False)
chords_df.to_csv('bill_evans_sequence.csv', index=False)