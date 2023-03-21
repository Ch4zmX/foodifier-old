import discord
import datetime

if __name__ == '__main__':
    BLACKLIST = ['muggestions', 'announcements', 'rules', 'menu', 'ai-art']
    WHITELIST = ['']
    with open("token.txt", "r") as f:
        TOKEN = f.read().strip()

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Client has logged in as {client.user}')

    @client.event
    async def on_message(message):
        username, user_message, channel = str(message.author), str(message.content), str(message.channel)
        print(f'{datetime.datetime.now()}: {username} said: "{user_message}" ({channel}).')

        if username == str(client.user):
            return

        if channel in BLACKLIST:
            return
        if "lean" in message.content.lower().replace(" ", ""):
            await message.delete()
            #   await message.author.timeout(datetime.timedelta(seconds=10))
            await message.channel.send("I HATE LEAN!!!")
            return 
        if "mug" in message.content.lower().replace(" ", ""):
            await message.channel.send("I LOVE MUG!!!")



    @client.event
    async def on_message_edit(before, message):
        username, user_message, channel = str(message.author), str(message.content), str(message.channel)
        if "lean" in message.content.lower().replace(" ", ""):
            await message.delete()

            if channel == "bot-stuff":
                await message.channel.send("I HATE LEAN!!!")


    client.run(TOKEN)