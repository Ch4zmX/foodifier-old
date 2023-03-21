import requests
from bs4 import BeautifulSoup
import time
import urls


def get_meal_from_time(time):
    pass

def get_site_with_cookie(url, location_cookie):
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


def get_meal(college, meal="Auto", day="Today"):  # get single meal, defaults to auto based on current time
    food_items = {}
    div = ''
    if meal == "Auto":
        print("Auto feature not set! Manually choose a meal\nSetting meal to lunch...")
        meal = "Lunch"
    location = urls.MENU_URLS[college]

    full_url = urls.BASE_URL+location+urls.MEAL_URL+meal
    location_cookie = location[0:2]


    response = get_site_with_cookie(full_url, location_cookie) # get html of specified menu
    soup = BeautifulSoup(response.content, 'lxml')
    table = soup.find('div', {'class': 'longmenuinstructs'}).parent.find_all('div')[1].find('table')
    print(table.prettify())
    for tag in table.find_all('div', {'class': 'longmenucoldispname'}):
        tag = tag.parent.parent # Go up 2 tags to get name and also
        for td in tag.find_all('td'):
            if div := td.find('div', {'class': 'longmenucoldispname'}):
                food_items[div.text] = []
                print(div.text, end=': ')
            else:
                dietary_restriction = td.find('img')['src'][13:].replace('.gif', '')
                print(dietary_restriction)


    print(food_items)

    #for tag in table.find_all('div', {'class': 'longmenucoldispname'}):
        #print(tag, "\n")
        #print(tag, '\n')


if __name__ == '__main__':
    get_meal('cowell/stevenson', 'Lunch')
