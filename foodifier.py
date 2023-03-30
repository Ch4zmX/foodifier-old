import discord
from discord.ext import commands
from discord import app_commands
from typing import List
from datetime import datetime
from datetime import timedelta  
from menu import *
from urls import *


if __name__ == '__main__':
    WHITELIST = ['bot-stuff', 'foodifier'] # bot will only run if message is in whitelisted channel
    INTENTS = discord.Intents.all()
    INTENTS.message_content = True
    with open('token.txt', 'r') as f: # if running this yourself, create a bot token and put it in token.txt (purpose is so i can share this program without sharing my token)
        TOKEN = f.read().strip()
    
    bot = commands.Bot(command_prefix='!', intents=INTENTS)


    @bot.event
    async def on_ready():
        print('Syncing bot slash commands with server...')
        try:
            await bot.tree.sync()
            print("Commands synced successfully!")
        except Exception as e:
            print(f'Error syncing commands: {str(e)}')

        print(f'Client has logged in as {bot.user}') 

    @bot.tree.command(name='menu', description='Get the menu of a specific meal at the specified dining hall, with an optional day offset.')
    async def menu(interaction: discord.Interaction, location: str, meal: str, day_offset: int = 0):
        user, channel, command = str(interaction.user), str(interaction.channel), str(interaction.command)
        if channel not in WHITELIST:
            print(f'Ignoring command in {channel} channel')
            return
        if location not in LOCATION_URLS.keys():
            print(f'Invalid dining location specified: "{location}"')
            menu_embed = discord.Embed(title=f'Invalid dining location specified: "{location}"\n', color=0xFF0000)
            await interaction.response.send_message(embed=menu_embed)
            return
        if meal not in MEALS:
            print(f'Invalid meal specified location specified: "{location}". Setting meal to lunch...')
            #menu_embed = discord.Embed(title=f'Invalid meal specified: "{location}"\n', color=0xFF0000)
            #await interaction.response.send_message(embed=menu_embed)
            meal = "Lunch"
        
        print(f'{datetime.now()}: {user} used command') # print who used what command for logging purposes

        date = (datetime.now() + timedelta(days=day_offset)).strftime('%m/%d/%y') # get date of , default offset of 0
        
        try:
            meal_dict = get_meal(location, meal, date) # try except in case command 
        except Exception as e:
            print(f'Failed fetching menu: {str(e)}')
            menu_embed = discord.Embed(title=f'Failed fetching specified menu: "{location}"\n', color=0xFF0000)
            await interaction.response.send_message(embed=menu_embed)
            return
        if meal_dict is None: # if menu was not found the value will be None
            print("Bot response: meal unavailable")
            menu_embed = discord.Embed(title=f'Specified meal is unavailable!\n', color=0xFF0000)
            await interaction.response.send_message(embed=menu_embed)
            return
        
        message_str = ''
        for food in meal_dict.keys():
            food = food.strip()
            if food == '-- Cereal --':
                break
            
            if food in DIVIDERS:
                message_str += f'**{food.replace("-","").strip()}**\n'
                continue

            message_str += food + ' '
            if meal_dict[food] is not None:
                    for diet_restriction in meal_dict[food]:
                        try:
                            message_str += ' ' + EMOJIS[diet_restriction] + ' ' # add emojis to output string representing dietary restrictions
                        except Exception as e:
                            print(f'Error handling allergen keyword: {str(e)}')
            message_str += '\n'

        menu_embed = discord.Embed(title=f'Menu for {meal} at {location} on {date}', description=message_str, color=0x50c878)

        await interaction.response.send_message(embed=menu_embed)

    @bot.event
    async def on_message(message):
        username, user_message, channel = str(message.author), str(message.content), str(message.channel)
        if (channel not in WHITELIST) or message.author == bot.user:
            return
        print(f'{datetime.now()}: {username} said {user_message}')

        content = user_message.strip()
       
        command_split = content.split(' ') # command format: "/menu cowell/stevenson Lunch 04/02/23"
        if command_split[0] != '/menu':
            return

        
        message_str = ''
        for food in meal_dict.keys():
            food = food.strip()
            if food == '-- Cereal --':
                break
            
            if food in DIVIDERS:
                message_str += f'**{food.replace("-","").strip()}**\n'
                continue

            message_str += '     ' + food + ' '
            if meal_dict[food] is not None:
                for diet_restriction in meal_dict[food]:
                    #print(diet_restriction)
                    message_str += ' ' + EMOJIS[diet_restriction] + ' ' # add emojis to output string representing dietary restrictions
            message_str += '\n'
        #print(message_str)
        await message.channel.send(message_str)
        print("Bot response: Successfully got specified meal")
    bot.run(TOKEN)