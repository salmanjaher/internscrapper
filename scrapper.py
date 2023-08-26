import discord
from discord.ext import commands
import requests
import json
import os
from environs import Env
env = Env()
env.read_env()

# Set up the bot with a command prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",intents=intents)

print(os.getenv)

API_KEY = os.getenv('API_KEY')
CX_ID = os.getenv('CX_ID')
BOT_ID = os.getenv('BOT_ID')

def find_latest_links(query, num_links=5):
    search_url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX_ID,
        "q": query,
        "num": num_links
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    
    links = []
    for item in data.get("items", []):
        links.append(item.get("link", ""))
    return links

@bot.command()
async def hi(ctx):
    await ctx.send("Hi!")
     
@bot.command()
async def pull(ctx, *, query):
    await ctx.send(f"Searching for top 5 latest links related to: {query}")
    
    links = find_latest_links(query, num_links=5)
    
    if links:
        response = "\n".join(links)
        await ctx.send(f"```Here are the top 5 latest links:\n{response}```")
    else:
        await ctx.send("No links found.")

bot.run(BOT_ID)

