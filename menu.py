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

#def get_menu(college, day="today"):  # get all meals
    #response = requests.get(urls.BASE_URL+urls.MENU_URLS[college.lower()])  # get html of specified menu and check if response is good
   # soup = BeautifulSoup(response.content, 'lxml')
    #print(soup)


async def get_meal(college, meal="Auto", date='today'):  # get single meal, defaults to auto based on current time. date must be formatted MM/DD/YYYY (any length, just split with slashes)
    #dtdate=04%2F2%2F2023
    
    food_items = {}
    
    if meal == "Auto":
        print("Auto feature not set! Manually choose a meal!\nSetting meal to lunch...")
        meal = "Lunch"
    
    date_string = ''
    if date != 'today':
        date_split = date.split('/')
        date_string = f'&dtdate={date_split[0]}%2F{date_split[1]}%2F{date_split[2]}'

    location_url = urls.LOCATION_URLS[college]

    full_url = urls.BASE_URL+location_url+urls.MEAL_URL+meal+date_string
    print(full_url)
    # longmenucolmenucat - divider names
    # longmenucoldispname - menu items name
    with open("menu.htm", "r") as f:
        response = bytes(f.read(), 'utf-8')  #
    #response = get_site_with_cookie(full_url, location_url).text # get html of specified menu
    soup = BeautifulSoup(response, 'lxml')
    print(response)
    try:
        if (table := soup.find('div', {'class': 'longmenuinstructs'}).parent.find_all('div')[1].find('tbody')) is None: #tbody containing trs for each menu item/divider
            return None 
    except:
        return None

    for tr in table.find_all('tr',recursive=False): # recursive false so it doesnt get the text 3 times due to nested trs
        if (divider := tr.find('div',{'class':'longmenucolmenucat'})) is not None: # check if divider (Grill, Cereal etc) in current tr. if so, print or whatever and go to next tr
            food_items[divider.text] = None
            continue
        if (food := tr.find('div', {'class':'longmenucoldispname'})) is not None:
            food_items[food.text] = [] # add food to dictionary 
            for img in tr.find_all('img'): # iterate through dietary restrictions and get img src names
                diets = img['src'].split('/')[1].split('.')[0] # parse them just in case i need them later 
                
                food_items[food.text].append(diets)
    print(full_url)
    return food_items
    


'''
for tag in table.find_all('div', {'class': 'longmenucoldispname'}):
        tag = tag.parent.parent # Go up 2 tags to get name and also
        for td in tag.find_all('td'):
            if div := td.find('div', {'class': 'longmenucoldispname'}):
                food_items[div.text] = []
                #print(div.text, end=': ')
            else:
                dietary_restriction = td.find('img')['src'][13:].replace('.gif', '')
                #print(dietary_restriction)
'''

    #print(food_items)

    #for tag in table.find_all('div', {'class': 'longmenucoldispname'}):
        #print(tag, "\n")
        #print(tag, '\n')


if __name__ == '__main__':
    print(get_meal('cowell/stevenson', 'Dinner', '04/02/23'))
