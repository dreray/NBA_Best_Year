#################################
##### Name: Andre Ray 
##### Uniqname: dreray
#################################

from bs4 import *
import requests
import json

import time 
import json
import csv
import urllib 
from csv import DictReader
from operator import itemgetter

from flask import Flask,  render_template, request, redirect, url_for
import secrets
import json
import requests
import time 





with open('holyg.csv', 'r') as read_obj:
    dict_reader = DictReader(read_obj)
    nba_dict = list(dict_reader)
    #print(nba_dict)


for k in nba_dict:
    k['holy_grail'] = round(float(k['holy_grail']),2)
    k['mvp_bonus'] = float(k['mvp_bonus'])
    k['fmvp_bonus'] = float(k['fmvp_bonus'])

    #print(type(k['holy_grail']))

# nba_2 = sorted(nba_dict, key = itemgetter('holy_grail'), reverse=True)

nba_2 = sorted(nba_dict, key = itemgetter('holy_grail'), reverse=False)



def fetch_year(year):

    year = str(year)
    
    
    top_10 = []
    
    max_grail = 0.0
    grail = None
    n = 0

    nba3 = nba_2

    i = 0 
    while i < 15:

        for count,result in enumerate(nba3):

            if year == result["Year"]:

                holy_grail = float(result['holy_grail'])

                if holy_grail > max_grail:
                    max_grail = holy_grail
                    grail = result
                    n = count


        top_10.append(grail)
        nba_2.pop(n)
        i+=1 
        max_grail = 0

    
    for removed_list in top_10:
        nba3.append(removed_list)

    #print(top_10)
    top_sort = sorted(top_10, key = itemgetter('holy_grail'), reverse=True)

    

    return(top_sort)

def Goats(year_list):

    TOP_8 = {}

    for goats in year_list:
        
        TOP_8[goats['Player']]= goats['holy_grail']

    


  
    return(TOP_8)

def MVP(year_list):

    MVP = {}
    for goats in year_list:

        if goats['mvp_bonus'] > 1: 
            MVP['MVP']= goats['Player']
            break

    for goats in year_list:

            if goats['fmvp_bonus'] > 1:
                MVP['Finals MVP']= goats['Player']

    return(MVP)

def ATeam(year_list):

    all_t = {}
    for goats in year_list:
        
        
        if goats['all_team']  == '1st':
            all_t[goats['Player']]= '1st Team'

        if goats['all_team']  == '2nd':
            all_t[goats['Player']]= '2nd Team'

    #print(all_t)
    return(all_t)

#ATeam(fetch_year(2020))


app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    
    if request.method == "POST":
        nba_season = request.form['Years']
        return redirect(url_for('Year',year=nba_season))

    else: 
        return render_template('input.html')

@app.route('/<year>', methods=['POST','GET'])

def Year(year):

    top_player_dict = Goats(fetch_year(year))
    mvp_dict = MVP(fetch_year(year))
    all_nba = ATeam(fetch_year(year))

    if request.method == "POST":
        nba_season = request.form['Years']
        return redirect(url_for('Year',year=nba_season))

    else:
        return render_template('nba.html', season=year,
        goats = top_player_dict,mvp = mvp_dict,all_nba = all_nba) 



if __name__ == '__main__':  
    print('starting Flask app', app.name)  
    app.run(debug=True)


