from datetime import datetime, timedelta
from typing import *

import discord
from discord.ext import commands

from menu import *
from urls import *

if __name__ == '__main__':
    WHITELIST = ['bot-stuff', 'foodifier', 'menu'] # bot will only run if message is in whitelisted channel (these are specific to my test server)
    INTENTS = discord.Intents.all()
    INTENTS.message_content = True
    with open('token.txt', 'r') as f: # if running this yourself, create a bot token and put it in token.txt (purpose is so i can share this program without sharing my token)
        TOKEN = f.read().strip()
    
    bot = commands.Bot(command_prefix='!', intents=INTENTS)



    @bot.event
    async def on_ready():
        

        print(f'Client has logged in as {bot.user}') 

    @bot.tree.command(name='menu', description='Get the menu of a specific meal at the specified dining hall, with an optional day offset.')
    async def menu(interaction: discord.Interaction, 
                   location: Literal[tuple((LOCATION_URLS.keys()))],  # Autocomplete choices for location parameter
                   meal: Literal[tuple(MEALS)],  # Autocomplete choices for meal parameter
                   day_offset: Literal[tuple([i for i in range(0,19)])] = 0): # max offset is tested to be 18 
        user, channel, command = str(interaction.user), str(interaction.channel), str(interaction.command)
        if channel not in WHITELIST: # only accept commands in whitelisted channels
            print(f'Ignoring command in {channel} channel')
            return
        
        if location not in LOCATION_URLS.keys(): # error if incorrect location entered
            print(f'Invalid dining location specified: "{location}"')
            menu_embed = discord.Embed(title=f'Invalid dining location specified: "{location}"\n', color=0xFF0000)
            await interaction.response.send_message(embed=menu_embed)
            return
        if meal not in MEALS: # if invalid meal entered, auto set to lunch. I will later add auto meal selection based on current time and schedule of specified dh
            print(f'Invalid meal specified location specified: "{location}". Setting meal to lunch...')
            #menu_embed = discord.Embed(title=f'Invalid meal specified: "{location}"\n', color=0xFF0000)
            #await interaction.response.send_message(embed=menu_embed)
            meal = "Lunch"
        if meal == "Auto":
            print("Auto feature not set! Manually choose a meal!\nSetting meal to lunch...")
            meal = "Lunch"
        
        print(f'{datetime.now()}: {user} used command') # print who used what command for logging purposes

        date = (datetime.now() + timedelta(days=day_offset)).strftime('%m/%d/%y') # get menu parsing date from current date and offset with a default offset of 0 for today
        
        try:
            meal_dict = get_meal(location, meal, date) # try except in case command 
        except Exception as e:
            print(f'Failed fetching menu: {str(e)}')
            menu_embed = discord.Embed(title=f'Failed fetching specified menu: "{location}"\n', color=0xFF0000) # error message if exception occured
            await interaction.response.send_message(embed=menu_embed)
            return
        if meal_dict is None: # if menu was not found the value will be None
            print("Bot response: meal unavailable")
            menu_embed = discord.Embed(title=f'{meal} at {location} on {date} is unavailable!\n', color=0xFF0000) # error message if meal not available
            await interaction.response.send_message(embed=menu_embed)
            return
        
        message_str = '' # empty message to add to
        for food in meal_dict.keys(): 
            food = food.strip()
            if food == '-- Cereal --': # cereal divider means end of actual menu
                break
            
            if food in DIVIDERS: # ignore dividers and show as bold
                message_str += f'**{food.replace("-","").strip()}**\n'
                continue

            message_str += food + ' ' 
            if meal_dict[food] is not None: # iterate through allergens/dietary restrictions and add them to each menu item
                    for diet_restriction in meal_dict[food]:
                        try:
                            message_str += ' ' + EMOJIS[diet_restriction] + ' ' # add emojis to output string representing dietary restrictions
                        except Exception as e:
                            print(f'Error handling allergen keyword: {str(e)}') # if unknown allergen encountered show error so i can add it
            message_str += '\n'

        menu_embed = discord.Embed(title=f'Menu for {meal} at {location} on {date}', description=message_str, color=0x50c878) #send embed with green color to signify success

        await interaction.response.send_message(embed=menu_embed) 

    @bot.tree.command(name='notify', description='Get pinged when a certain meal or food item is in the menu')
    async def notify(interaction: discord.Interaction, food_item: str): # doesnt do anything yet

        pass



    @bot.event
    async def on_message(message):
        username, user_message, channel = str(message.author), str(message.content), str(message.channel)
        if username != 'Sh4d0w#8259' or channel != 'mod':
            return
        
        print(f'{datetime.now()}: {username} said {user_message}')
        if user_message == '/sync':
            print('Syncing bot slash commands with server...')
            try:
                await bot.tree.sync()
                print("Commands synced successfully!")
                await message.channel.send('Commands synced successfully!')
            except Exception as e:
                print(f'Error syncing commands: {str(e)}')
                await message.channel.send(f'Error syncing commands: {str(e)}')

        

bot.run(TOKEN)