from enum import Enum

BASE_URL = "https://nutrition.sa.ucsc.edu/longmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum="
LOCATION_URLS = {
    'cowell/stevenson': "05&locationName=Cowell%2fStevenson+Dining+Hall&naFlag=1",
    'crown/merrill': "20&locationName=Crown%2fMerrill+Dining+Hall&naFlag=1",
    'nine/ten': "40&locationName=College+Nine%2fJohn+R.+Lewis+Dining+Hall&naFlag=1",
    'porter/kresge': "25&locationName=Porter%2fKresge+Dining+Hall&naFlag=1"}
MEAL_URL = "&WeeksMenus=UCSC+-+This+Week%27s+Menus&mealName="

MEALS = ['Breakfast', 'Lunch', 'Dinner', 'Late Night', 'Auto']  # Auto meal selects meal based on current time
DIVIDERS = ['-- Grill --', '-- Clean Plate --', '-- DH Baked --', '-- Bakery --', '-- Open Bars --', '-- Cereal --', '-- All Day --', '-- Condiments --', 
            '-- Salad Bar --', '-- Deli Bar --', '-- Bread and Bagels --', '-- Beverages --'] # strings corresponding to the dividers, will be used to determine menu validity 
                                                                                      # (eg if cereal is first divider found, then the dh is not open for that meal)
EMOJIS = {'veggie':'🥦', 'vegan':'🌱', 'halal':'🍖', 'eggs':'🥚', 'beef':'🐮', 'milk':'🥛', 'fish':'🐟', 'alcohol':'🍷', 'gluten':'🍞', 'soy':'🇸'}