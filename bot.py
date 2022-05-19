import os

import discord
from dotenv import load_dotenv
from behavior import InServer, Chats

load_dotenv()
TOKEN = os.getenv("STONKS_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
chats = Chats()
behavior = InServer(chats)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message:discord.Message):
    if (message.author == client.user or message.content[0] != '!'):
        return
    message.content = message.content.removeprefix('!')
    if (message.author in chats.instances):
        await chats.instances[message.author].on_message(message)
    else:
        global behavior
        await behavior.on_message(message)

client.run(TOKEN)
