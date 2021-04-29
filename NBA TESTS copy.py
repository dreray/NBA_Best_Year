#################################
##### Name: Andre Ray 
##### Uniqname: dreray
#################################

from bs4 import *
import requests
import json
import secrets # file that contains your API key
import time 
import json
import csv
import urllib 
from csv import DictReader
from operator import itemgetter

from flask import Flask,  render_template
import secrets
import json
import requests
import time 





with open('holyg.csv', 'r') as read_obj:
    dict_reader = DictReader(read_obj)
    nba_dict = list(dict_reader)
    #print(nba_dict)


for k in nba_dict:
    k['holy_grail'] = float(k['holy_grail'])
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
    while i < 7:

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

    print(top_10)
    top_sort = sorted(top_10, key = itemgetter('holy_grail'), reverse=True)

    

    return(top_sort)

def Goats(year_list):

    TOP_8 = {}

    MVP = {}

    #Total Season Score Leaders in {year}:

    for goats in year_list:
        # print (f"{goats['Player']} generated a Total Season Score of {goats['holy_grail']}")
        TOP_8[goats['Player']]= goats['holy_grail']

    # for goats in year_list:

    #     if goats['mvp_bonus'] > 1: 
    #         TOP_8['MVP']= goats['Player']
    #         MVP['MVP']= goats['Player']
    #         break

    # for goats in year_list:

    #     if goats['fmvp_bonus'] > 1: 
    #         TOP_8['Finals MVP']= goats['Player']
    #         MVP['Finals MVP']= goats['Player']
    #         break
    # print('')
    # for goats in year_list:
        
    #     if goats['all_team']  == '1st': 
    #         print (f"{goats['Player']} made ALL NBA 1st Team ")


    print(TOP_8)
    return(TOP_8)
   

            #nba_2.remove(max)
            #top_25.append(result)
                #top_holy = holy_grail


        #if year == nba_dict
        #print(result)
        # holy_grail >= top_holy:


        # year = (result['title'])
        # if count <6:
        #     headline_count = f'{headline}'
        #     headline_list.append(headline_count)
        # count +=1

    #return(headline_list)


#fetch_year(2020)



app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Welcome NBA FAN! </h1> <h3>Add a Year between 1980 and 2020 into the URL (i.e /1995) to see which players had the best Season that year<h3>'



@app.route('/<year>')

def Year(year):

    lines = Goats(fetch_year(year))

    return render_template('nba.html', year=year,
    headlines = lines) 


if __name__ == '__main__':  
    print('starting Flask app', app.name)  
    app.run(debug=True)


