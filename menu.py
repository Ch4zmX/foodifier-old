import requests
from bs4 import BeautifulSoup
import time
import urls


def get_meal_from_time(time):
    pass

def get_menu(college, day="today"):  # get all meals
    if not (response := requests.get(urls.BASE_URL+urls.MENU_URLS[college])).ok:  # get html of specified menu and check if response is good
        return False
    soup = BeautifulSoup(response.content, 'lxml')
    print(soup)


def get_meal(college, meal="Auto", day="Today"):  # get single meal, defaults to auto based on current time
    if meal == "Auto":
        print("Auto feature not set! Manually choose a meal\nSetting meal to lunch...")
        meal = "Lunch"
    full_url = urls.BASE_URL+urls.MENU_URLS[college]+urls.MEAL_URL+meal
    #response = requests.get(full_url)  # get html of specified menu
    print(full_url)
    #soup = BeautifulSoup(response.content, 'lxml')
    #print(soup)


if __name__ == '__main__':
    get_meal('crown/merrill', 'Lunch')
