from enum import Enum

BASE_URL = "https://nutrition.sa.ucsc.edu/longmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum="
LOCATION_URLS = {
    'cowell/stevenson': "05&locationName=Cowell%2fStevenson+Dining+Hall&naFlag=1",
    'crown/merrill': "20&locationName=Crown%2fMerrill+Dining+Hall&naFlag=1",
    'nine/ten': "40&locationName=College+Nine%2fJohn+R.+Lewis+Dining+Hall&naFlag=1",
    'porter/kresge': "25&locationName=Porter%2fKresge+Dining+Hall&naFlag=1"}
MEAL_URL = "&WeeksMenus=UCSC+-+This+Week%27s+Menus&mealName="

MEALS = ['Breakfast', 'Lunch', 'Dinner', 'Late Night', 'Auto']  # Auto meal selects meal based on current time

