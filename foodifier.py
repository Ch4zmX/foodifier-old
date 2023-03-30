import discord
from discord.ext import commands
import datetime
from menu import *
from urls import *


if __name__ == '__main__':
    WHITELIST = ['bot-stuff'] # bot will only run if message is in whitelisted channel
    INTENTS = discord.Intents.all()
    INTENTS.message_content = True
    with open('token.txt', 'r') as f: # if running this yourself, create a bot token and put it in token.txt (purpose is so i can share this program without sharing my token)
        TOKEN = f.read().strip()
    
    bot = commands.Bot(command_prefix='$', intents=INTENTS)
    
    @bot.event
    async def on_ready():
        
        print(f'Client has logged in as {bot.user}')
    @bot.command(name='menu', description='Get the menu of a specific meal at the specified dining hall, with an optional day offset.', guild='1028797629037023242')
    async def menu(interaction: discord.Interaction, question: str):
        menu_embed = discord.Embed(title='Menu for specified DH:', description='MENU GOES HERE', color='#50C878')
        await interaction.response.send_message(embed=menu_embed)

    @bot.event
    async def on_message(message):
        username, user_message, channel = str(message.author), str(message.content), str(message.channel)
        if (channel not in WHITELIST) or message.author == bot.user:
            return
        print(f'{datetime.datetime.now()}: {username} said {user_message}')

        content = user_message.strip()
       
        command_split = content.split(' ') # command format: "/menu cowell/stevenson Lunch 04/02/23"
        if command_split[0] != '/menu':
            return
        print (command_split)
        if (meal_dict := get_meal(command_split[1], command_split[2], command_split[3])) is None or meal_dict == False:
            if meal_dict == False:
                await message.channel.send('Error connecting to the menuwebsite! Probably too many requests\n')
                return
            await message.channel.send('Specified meal is unavailable!\n')
            print("Bot response: meal unavailable")
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