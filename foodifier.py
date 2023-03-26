import discord
import datetime
from menu import *
from urls import *

if __name__ == '__main__':
    WHITELIST = ['bot-stuff'] # bot will only run if message is in whitelisted channel
    MESSAGE = 'cowell'

    with open('token.txt', 'r') as f: # if running this yourself, create a bot token and put it in token.txt (purpose is so i can share this program without sharing my token)
        TOKEN = f.read().strip()

    intents = discord.Intents.default()
    intents.message_content = True
    
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Client has logged in as {client.user}')

    @client.event
    async def on_message(message):
        if str(message.channel) not in WHITELIST:
            return
        if MESSAGE in str(message.content):
            if (meal_dict := await get_meal('cowell/stevenson', 'Lunch')) is None:
                await message.channel.send('Specified meal is unavailable!\n')
                return

            message_str = ''
            for food in meal_dict.keys():
                if food == '-- Cereal --':
                    break
                #print(food)
                
                if food in DIVIDERS:
                    message_str += f'**{food.replace("-","").strip()}**\n'
                    continue
                message_str += food + ' '
                for diet_restriction in meal_dict[food]:
                    #print(diet_restriction)
                    message_str += ' ' + EMOJIS[diet_restriction] + ' ' # add emojis to output string representing dietary restrictions
                message_str += '\n'
            #print(message_str)
            await message.channel.send(message_str) 
    client.run(TOKEN)