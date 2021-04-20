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

BASE_URL ='https://www.nps.gov/'
site_url = BASE_URL+'/isro'
state_url = 'https://www.nps.gov/state/mi/index.htm'

CACHE_FILE_NAME = 'cacheSI_Scrape.json'
CACHE_DICT = {}

key = secrets.API_KEY

headers = {'User-Agent': 'UMSI 507 Course Project - Python Web Scraping','From': 'ray@umich.edu','Course-Info': 'https://www.si.umich.edu/programs/courses/507'}

def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]


def make_url_request_using_cache2(url, cache):
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url, params=parameters, headers=headers)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

CACHE_DICT = load_cache()

#STATES(HOMEPAGE)
#response = make_url_request_using_cache(BASE_URL, CACHE_DICT)
response = requests.get(BASE_URL)
#soup = BeautifulSoup(response, 'html.parser')
soup = BeautifulSoup(response.text, 'html.parser')
states = soup.find('ul', class_= 'dropdown-menu SearchBar-keywordSearch').find_all('li')



#PARKS (PARK PAGES)
#response2 = make_url_request_using_cache(site_url, CACHE_DICT)
response2 = requests.get(site_url)
soup2 = BeautifulSoup(response2.text, 'html.parser')
#soup2 = BeautifulSoup(response2, 'html.parser')



#STATE GRAB 
#Takes a state page URL(e.g.“https://www.nps.gov/state/tx/index.htm”) and returns a list of NationalSiteobjects in the state page.



#response3 = make_url_request_using_cache(state_url, CACHE_DICT)
response3 = requests.get(state_url)
#soup3 = BeautifulSoup(response3, 'html.parser')
soup3 = BeautifulSoup(response3.text, 'html.parser')
state_parks = soup3.find_all('h3')



class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, category="", name="", address="", zipcode="", phone=""):

        self.category = category
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.phone = phone

    def info(self):
        return f"{self.name} ({self.category}): {self.address} {self.zipcode}"

def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''
    state_dict = {}

    for state in states:
        state_name = state.text.lower().strip()
        state_url = state.find('a')['href'].strip('/')
        state_link = BASE_URL + state_url
        state_dict[state_name] = state_link

    #print(state_dict.keys())
    return state_dict


def get_site_instance(site_url):
    '''Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''

    response2 = requests.get(site_url)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    
    parks = soup2.find('div', class_ = "Hero-titleContainer clearfix").find('a')
    park_name = parks.text.strip()
    #print(park_name)


    if soup2.find('p', class_ = "adr").find('span', class_='region') is not None:
        category = soup2.find('div', class_ = "Hero-designationContainer").find('span')
        park_category = category.text.strip()

    else: park_category = 'N/A'

    #print(park_category)


    #street = soup2.find('p', class_ = "adr").find('span', class_='street-address').text.strip()
    city = soup2.find('p', class_ = "adr").find('span', itemprop='addressLocality').text.strip()

    if soup2.find('p', class_ = "adr").find('span', class_='region') is not None:
        state = soup2.find('p', class_ = "adr").find('span', class_='region').text.strip()
    else: state = 'N/A'

    if soup2.find('p', class_ = "adr").find('span', class_='postal-code') is not None:
        zcode = soup2.find('p', class_ = "adr").find('span', class_='postal-code').text.strip()

    else: zcode = 'N/A'

    phone = soup2.find('div', class_ = "vcard").find('span',class_='tel').text.strip()


    
    address = f'{city}, {state}'
    #print(phone)

    #print(park_category,park_name,address,zcode,phone)
    
    return park_category,park_name,address,zcode,phone



def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site instances
    '''
    
    response3 = requests.get(state_url)
    soup3 = BeautifulSoup(response3.text, 'html.parser')
    state_parks = soup3.find_all('h3')

    instance_list = []

    nat_site_list = []

    for parks in state_parks:
        park_tag = parks.find('a')
      
        if park_tag is not None:
            park_path = park_tag['href'].strip('/')

            park_url = BASE_URL+park_path
            site_details = ((get_site_instance(park_url)))
            
            #instance_list.append(site_details)

            Nat_Site_Init = NationalSite(category=site_details[0],name=site_details[1],address=site_details[2],zipcode=site_details[3],phone=site_details[4])

            nat_site_list.append(Nat_Site_Init)





        #body = NationalSite(category=site_detail[0],name=d)            

    return nat_site_list 

#get_sites_for_state(state_url)


def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''

    mapquest_url = 'http://www.mapquestapi.com/search/v2/radius'
    parameters = {}
    parameters['key'] = key
    parameters['origin'] =  site_object.zipcode
    parameters['radius'] = 10
    parameters['maxMatches'] =  10
    parameters['ambiguities'] = 'ignore'
    parameters['outFormat'] =  'json'
    

    #quest_response = make_url_request_using_cache2(mapquest_url, CACHE_DICT)
    quest_response = requests.get(mapquest_url,params= parameters)
    results = (json.loads(quest_response.text))
    results_dict = results['searchResults']


    #ordered_list =  []

    for places in results_dict:
        if places['name'] != "":
            name = places['name']

        if places['fields']['group_sic_code_name'] != "":
            category = places['fields']['group_sic_code_name']
        else: category = 'no category'

        if places['fields']['address'] != "":
            address = places['fields']['address']
        else: address = 'no address'

        if places['fields']['city'] != "":
            city = places['fields']['city']
        else: city = "no city"

        #print(places['fields']['group_sic_code_name'])

        print(f'- {name} ({category}): {address}, {city}')

        # print(f'-{name}:{address},{city}')


    #print(results_dict[2])




# parks = get_sites_for_state(state_url)
# get_nearby_places(parks[4])

if __name__ == "__main__":
    
    breakall = False
    while breakall == False:
        try:
            state = input('Enter a State name (i.e Florida or florida) or "exit" : ')
            if state.lower() == 'exit':
                
                print('Goodbye and May Peace Be With You')
                break;
                    

            
            
        
            if state.lower() in build_state_url_dict().keys():

                state = state.lower()

                state_dicts = (build_state_url_dict())

                state_url = state_dicts[state]
                parks = get_sites_for_state(state_url)

                print('')
                print('')
                print("-"*20)
                print(f'List of National Sites in {state.title()}')
                print("-"*20)
                print('')

                counter = 1
                #park_list = []
                for park in parks:
                    print (f' {[counter]} {park.info()}')
                    

                    counter += 1
                print('')
                print('')

                while (True):
                
                    state2 = (input('Enter a Number for a detailed Search or "exit" or "back": '))
                    
                    if state2.lower() == 'back':
                        break

                    if state2.lower() == 'exit':
        
                        print('Goodbye and May Peace Be With You')
                        breakall = True
                        break


                    if state2.isnumeric():
                        state_num = int(state2)-1

                        if state_num <= len(parks):
                            
                            print('')
                            print('')
                            print("-"*40)
                            print(f'Places near {parks[state_num].name}')
                            print("-"*40)
                            print('')
                            
                            get_nearby_places(parks[state_num])
                            print('')
                            print('')

                        else:
                            print("[Error] Invalid Number" )
                            print("-"*40)
                            print('')
                            print('')



                    else:
                        print("[Error] Invalid Input (not a number)" )
                        print("-"*40)
                        print('')
                        print('')
                            
            else:
                print("[Error] Enter a proper state name" )

            
            

        except:
            continue