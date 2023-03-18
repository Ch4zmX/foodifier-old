import requests
from bs4 import BeautifulSoup

BASE_URL = "https://nutrition.sa.ucsc.edu/longmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum="
MENU_URLS = {
    'cowell/stevenson': "05&locationName=Cowell%2fStevenson+Dining+Hall&naFlag=1",
    'crown/merrill': "20&locationName=Crown%2fMerrill+Dining+Hall&naFlag=1",
    'nine/ten': "40&locationName=College+Nine%2fJohn+R.+Lewis+Dining+Hall&naFlag=1",
    'porter/kresge': "25&locationName=Porter%2fKresge+Dining+Hall&naFlag=1"}
MEALS = ['breakfast', 'lunch', 'dinner', 'latenight', 'auto']  # Auto meal selects meal based on current time


def get_menu(college, day="today"):  # get all meals
    if not (response := requests.get(BASE_URL+MENU_URLS[college])).ok:  # get html of specified menu and check if response is good
        return False
    soup = BeautifulSoup(response.content, 'lxml')
    print(soup)


def get_meal(college, day="today", meal="auto"):  # get single meal, defaults to auto based on current time
    response = requests.get(BASE_URL+MENU_URLS[college])  # get html of specified menu
    soup = BeautifulSoup(response.content, 'lxml')
    print(soup)


if __name__ == '__main__':
    get_meal('cowell/stevenson')
