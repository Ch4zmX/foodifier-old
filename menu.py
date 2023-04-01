import requests
from bs4 import BeautifulSoup
import time
import urls
import re

def get_meal_from_time(time):
    pass

def get_site_with_cookie(url, location_url):
    location_cookie = location_url[0:2]
    cookies = {
        'WebInaCartLocation': location_cookie,
        'WebInaCartDates': '',
        'WebInaCartMeals': '',
        'WebInaCartQtys': '',
        'WebInaCartRecipes': ''
    }

    response = requests.get(url, cookies=cookies)
    return response


def get_meal(college, meal, date='today'):  # get single meal, defaults to auto based on current time. date must be formatted MM/DD/YYYY (any length, just split with slashes)
    #dtdate=04%2F2%2F2023
    
    food_items = {}
    
    
    
    date_string = ''
    #print('date: ', date)
    if date != 'today':
        date_split = date.split('/')
        #print(date_split)
        date_string = f'&dtdate={date_split[0]}%2F{date_split[1]}%2F{date_split[2]}'

    location_url = urls.LOCATION_URLS[college]

    full_url = urls.BASE_URL+location_url+urls.MEAL_URL+meal+date_string
    #print(full_url)
    # longmenucolmenucat - divider names
    # longmenucoldispname - menu items name
    response = get_site_with_cookie(full_url, location_url).text # get html of specified menu
    if 'A RedBack Exception error occured while initializing the RedBack Object' in response:
        raise Exception("Error connecting to the menu website! Probably too many requests!")

    #with open("menu.htm", "r") as f:
       # response = bytes(f.read(), 'utf-8')  #
    
    soup = BeautifulSoup(response, 'lxml')
    #print(soup.prettify())
    try:
        if (table := soup.find('div', {'class': 'longmenuinstructs'}).parent.find_all('div')[1]) is None: #tbody containing trs for each menu item/divider
            #print("we")
            return None 
    except Exception as e:
        return None

    for tr in table.find_all('tr',recursive=True): # recursive false so it doesnt get the text 3 times due to nested trs
        #print(f"{tr}\n\n")
        if (divider := tr.find('div',{'class':'longmenucolmenucat'})) is not None: # check if divider (Grill, Cereal etc) in current tr. if so, print or whatever and go to next tr
            food_items[divider.text] = None
            #print(divider.text)
            continue
        if (food := tr.find('div', {'class':'longmenucoldispname'})) is not None:
            food_items[food.text] = [] # add food to dictionary 
            #print(food.text)
            for img in tr.find_all('img'): # iterate through dietary restrictions and get img src names
                diets = img['src'].split('/')[1].split('.')[0] # parse them just in case i need them later 
                
                food_items[food.text].append(diets)

    #print(full_url)
    return food_items


if __name__ == '__main__':
    #print(get_site_with_cookie('https://nutrition.sa.ucsc.edu/longmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum=05&locationName=Cowell%2fStevenson+Dining+Hall&naFlag=1&WeeksMenus=UCSC+-+This+Week%27s+Menus&mealName=Dinner', '05').text)
    print(get_meal('cowell/stevenson', 'Dinner', '04/02/23'))
