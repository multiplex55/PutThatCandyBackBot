#https://github.com/Giphy/giphy-python-client

# bot.py
import os
import random
import json
import aiohttp
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
giphy_token = os.getenv('GIPHY_TOKEN')

bot = commands.Bot(command_prefix='!')
api_instance = giphy_client.DefaultApi()

@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    print('------')
  
@bot.command(name='cool', help='Tells you you are cool')
async def cmd_cool(ctx):
    userWhoSent = ctx.message.author
    response = "Hey " + "@" + str(userWhoSent) + "...you are cool"
    await ctx.send(response)

@bot.command(name='best', help='Tells you you are the best')
async def cmd_best(ctx):
    userToMention = ctx.message.author.mention
    response = "Hey " + str(userToMention) + "...you are the best"
    await ctx.send(response)

@bot.command(name='mult', help='Multiplies two numbers')
async def cmd_mult(ctx, a: int, b: int):
    await ctx.send("The result is " + str(a*b))
    
@bot.command(name='cat', help='cat gif')
async def cmd_cat(ctx):
    with ctx.channel.typing():
        with aiohttp.ClientSession() as session:
            async with session.get("http://random.cat/meow") as r:
                r = await r.read()
                url = json.JSONDecoder().decode(r.decode("utf-8"))["file"]
                await ctx.send(embed=discord.Embed(title="Random Cat").set_image(url=url).set_footer(text="Powered by random.cat")) 
     
@bot.command(name='gay', help='gay stuff')
async def cmd_gay(ctx):
    userToMention = ctx.message.author.mention
    response = "Are you really gay " + str(userToMention) + "?"
    await ctx.send(response)

@bot.command(name='gifs', help='gif stuff')
async def cmd_gifs(ctx,*,search):
    log_this("gifs: " + str(search))
    
    gif = await search_gifs(search)    
    await ctx.send('Gif URL : ' + gif)
    
async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(giphy_token, query, limit=5, rating='R')
        lst = list(response.data)        
        
        if(len(lst) == 0):
            log_this("Search gif -> Random Gif")
            return await random_gifs()
        else:
            gif = random.choices(lst)
            return gif[0].url
        
    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

@bot.command(name='gifr', help='gif stuff')
async def cmd_gifr(ctx):
    log_this("gifr")
    
    gif = await random_gifs()    
    await ctx.send('Gif URL : ' + gif)   
    
async def random_gifs():
   try:
       response = api_instance.gifs_random_get(giphy_token, tag='',rating='R',fmt='json')
       gif = response.data
       return gif.url
   except ApiException as e:
       return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e 
   
bot.remove_command('help')
@bot.command(name='help', help='It is the help')
async def cmd_help(ctx):
    embed = discord.Embed(title="MultiBot Commands", description="List of commands are:", color=0xeee657)
    embed.add_field(name="$cool X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="$mult X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="$cool", value="Says you are cool", inline=False)
    embed.add_field(name="$best", value="Says you are the best", inline=False)
    embed.add_field(name="$gay", value="Questions you", inline=False)
    embed.add_field(name="$gifs SEARCH", value="Searches GIPHY for something", inline=False)
    embed.add_field(name="$gifr", value="Random GIF", inline=False)
    
    embed.add_field(name="$help", value="Gives this message", inline=False)
    
    await ctx.send(embed=embed)
    
def log_this(what_to_log):
    print("Command executed: " + what_to_log)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
bot.run(discord_token)
