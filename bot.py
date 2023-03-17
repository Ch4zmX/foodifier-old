import discord

gif_random = "https://g.tenor.com/v1/random?"
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
    if username == str(client.user):
        return

    if channel != "bot-stuff":
        if message.content == "lean":
            await message.delete()
            return


    print(f'{username} said: "{user_message}" ({channel}).')

    if message.content.lower() == "mug":
        await message.channel.send("MUG Moment")
    if "lean" in message.content.lower():
        await message.delete()
        await message.channel.send("LEAN BAD")



client.run(TOKEN)