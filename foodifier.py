from datetime import datetime, timedelta
from typing import *
import config
import discord

from discord.ext import commands

from menu import *
from urls import *

CONFIG_FILE = 'config.ini'
INTENTS = discord.Intents.all()
INTENTS.message_content = True

bot = commands.Bot(command_prefix='!', intents=INTENTS)




if __name__ == '__main__':

    config.reset_config(CONFIG_FILE)
    config.BLACKLIST = ['general']
    config.WHITELIST = ['bot-stuff', 'bot-commands']
    config.write_config(CONFIG_FILE)
    config.read_config(CONFIG_FILE)
    print(config.WHITELIST, config.BLACKLIST)

    @bot.event
    async def on_ready():
        

        print(f'Client has logged in as {bot.user}') 

    @bot.tree.command(name='whitelist', description='Set the whitelist to enabled to false, and/or add channels to the whitelist using hashtag links') # first optional arg 'enabled': set whitelist to true or false, second optional arg 'add': enter multiple channels with the hashtag to add to whitelist 
    async def whitelist(interaction: discord.Interaction,
                        enabled: Literal['True', 'False'] = None,
                        add: str = ''
                        ):
        if not interaction.user.guild_permissions.administrator:
            print(f'Non admin user {interaction.user} used whitelist command! Ignoring...')
            await interaction.response.send_message('You must be server administrator to run this command!')
            return
        
        print(f'User {interaction.user} used whitelist command!')

        if enabled is not None: # None is the default option if not specified, which doesnt change the value of the whitelisted var
            config.whitelisted = bool(enabled)
        msg = '\n'
        if add != '':
            msg += f'Successfully added channels '
            bot.fetch_channel()
            discord.utils.get
            channels = str(add).split(' ')
            for i, channel in enumerate(channels):
                try:
                    id = int(channel.strip('<#').strip('>'))
                    print(id)
                    channel = await bot.fetch_channel(channel_id=id)
                    msg += f'"{channel.name}"'
                    if i < len(channels) - 1:
                        msg += ', '
                except:
                    print('Not a valid channel!')
            msg += 'to whitelist!'
        
        config.write_config(CONFIG_FILE)
        print(msg)
        whitelist_embed = discord.Embed(title='Whitelist', description=msg, color=0x50c878) # error message if meal not available
        await interaction.response.send_message(embed=whitelist_embed)
        return  

    @bot.tree.command(name='menu', description='Get the menu of a specific meal at the specified dining hall, with an optional day offset.')
    async def menu(interaction: discord.Interaction, 
                   location: Literal[tuple((LOCATION_URLS.keys()))],  # Autocomplete choices for location parameter
                   meal: Literal[tuple(MEALS)],  # Autocomplete choices for meal parameter
                   day_offset: Literal[tuple([i for i in range(0,19)])] = 0): # max offset is tested to be 18 
        user, channel, command = str(interaction.user), str(interaction.channel), str(interaction.command)
        if (config.whitelisted and channel not in config.WHITELIST) or (config.blacklisted and channel in config.BLACKLIST): # only accept commands in whitelisted channels
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
            #print(meal_dict)
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
            if '-- ' in food and food not in DIVIDERS: # cereal divider means end of actual menu
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

        if channel != 'mod':
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

        

bot.run(config.TOKEN)