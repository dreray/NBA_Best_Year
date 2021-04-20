#################################
##### Name: Andre Ray 
##### Uniqname: dreray
#################################

from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import json
import secrets # file that contains your API key
import time 
import json
import csv

BASE_URL ='https://www.basketball-reference.com/awards/all_league.html'


response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text,'html.parser')

years = soup.find('div', id= 'div_awards_all_league').find('tbody')

players = years.find_all('a')


for player in players:
    name = player.text.strip()
    # state_url = state.find('a')['href'].strip('/')
    # state_link = BASE_URL + state_url
    # state_dict[state_name] = state_link

    #print(name)



#IMPORTING CSV DATA AS DICTIONARY 

player_dict = {}

with open('Data/player_data.csv', mode='r') as inp:
    reader = csv.reader(inp)
    player_dict = {rows[0]:rows[1] for rows in reader}

#print(dict_from_csv)

print(player_dict)


git
