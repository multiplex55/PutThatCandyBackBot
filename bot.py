#https://github.com/Giphy/giphy-python-client
# CTRL K CTRL 0 to fold all
# CTRL K CTRL J to unfold all

# bot.py
import os
import random
import json
import aiohttp
import asyncio
import giphy_client
from giphy_client.rest import ApiException
import requests
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import datetime
from urllib import parse, request
import re
import hashlib
import sqlite3
from PIL import Image
import bisect
import asyncio

# notes and todo
# gay duration
# achievements

#GLOBALS
#=============================
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
giphy_token = os.getenv('GIPHY_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix='$', intents=intents)

api_instance = giphy_client.DefaultApi()
client = discord.Client()

votes = []
channel_bot_commands = 538158421875097600
channel_general = 111237149793222656

#check if database is made and load it
db = sqlite3.connect('ptcb.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS quotes(hash TEXT primary key, user TEXT, message TEXT, date_added TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS gamba (user TEXT primary key, userName TEXT, points INTEGER)')
print("Loaded database")
db.commit()
#====================================================================================================================
@bot.command(name='cool', help='Tells you you are cool')
async def cmd_cool(ctx):
    userWhoSent = ctx.message.author
    response = "Hey " + "@" + str(userWhoSent) + "...you are cool"
    await ctx.send(response)

@bot.command(name='mult', help='Multiplies two numbers usage: multi num1 num2')
async def cmd_mult(ctx, a: int, b: int):
    await ctx.send("The result is " + str(a*b))

@bot.command(name='cat', help='cat gif usage: cat')
async def cmd_cat(ctx):
    with ctx.channel.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get("http://aws.random.cat/meow") as r:
                r = await r.read()
                url = json.JSONDecoder().decode(r.decode("utf-8"))["file"]
                await ctx.send(embed=discord.Embed(title="Random Cat").set_image(url=url).set_footer(text="Powered by random.cat"))

@bot.command(name='gay', help='gay stuff')
async def cmd_gay(ctx):
    userToMention = ctx.message.author.mention
    response = "Are you really gay " + str(userToMention) + "?"
    await ctx.send(response)

@bot.command(name='5050', help='plays 5050 on reddit')
async def play_5050(ctx):
    dat = requests.get('https://reddit.com/r/fiftyfifty/.json', headers={'User-Agent':'Discord-Acid-Bot /u/saucecode'}).json()
    urls = [(i['data']['title'], i['data']['url']) for i in dat['data']['children'] if 'imgur.com' in i['data']['url'] or 'i.redd.it' in i['data']['url'] or '5050.degstu' in i['data']['url']]
    titles,url = random.choice(urls)
    await ctx.send('`%s` or...' % titles.split('|')[0].replace('[50/50] ','') )
    await ctx.send('`%s`' % titles.split('|')[1] )
    await asyncio.sleep(5)
    await ctx.send(url)

@bot.command(name='reddit', help='random reddit image usage: reddit some_reddit_name')
async def get_random_reddit_image(ctx):
    subreddit = ctx.message.content.split(' ')[1]
    dat = requests.get('https://reddit.com/r/' + subreddit + '/.json', headers={'User-Agent':'Discord-Multibot-Bot'}).json()

    urls = [i['data']['url'] for i in dat['data']['children']] # pull urls from reddit post list
    imgurs = [url for url in urls if any( domain in url for domain in ['imgur.com', 'i.redd.it'] )] # filter links for only these domains

    await ctx.send(random.choice(imgurs))

@bot.command(name='vote', help='random reddit image usage: vote')
async def do_call_vote(ctx):
 	# spawn a message with the vote, and one upvote and one downvote button
 	# wait n seconds
 	# delete vote message
 	# post new message with vote results
    vote_string = ctx.message.content[6:]
    VOTE_LENGTH = 10

    vote = await ctx.send('**Hear, hear! A vote has been called!**\n`%s`' % (vote_string))
    await ctx.message.add_reaction('\U0001F44D')
    await ctx.message.add_reaction('\U0001F44E')

    votes.append({
        'vote_string': vote_string,
        'message': vote,
        'expires': time.time() + VOTE_LENGTH,
        'ctx': ctx
        })

@bot.command(name='gifs', help='gif stuff usage: gifs something_to_serach_for')
async def cmd_gifs(ctx,*,search):
    # log_this("gifs: " + str(search))

    gif = await search_gifs(search)
    await ctx.send('Gif URL : ' + gif)
    return

async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(giphy_token, query, limit=5, rating='R')
        lst = list(response.data)

        if(len(lst) == 0):
            # log_this("Search gif -> Random Gif")
            return await random_gifs()
        else:
            gif = random.choices(lst)
            return gif[0].url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

@bot.command(name='gifr', help='gif stuff usageL gifr')
async def cmd_gifr(ctx):
    # log_this("gifr")

    gif = await random_gifs()
    await ctx.send('Gif URL : ' + gif)

async def random_gifs():
    try:
        response = api_instance.gifs_random_get(giphy_token, tag='',rating='R',fmt='json')
        gif = response.data
        return gif.url
    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

@bot.command(name='crabrave', help='crab rave video usage: crabrave')
async def cmd_crabrave(ctx):
    await ctx.send('https://www.youtube.com/watch?v=cE0wfjsybIQ')
    return

@bot.command(name='brothermanbill', help='brothermanbill song usage: brothermanbill')
async def cmd_brothermanbill(ctx):
    await ctx.send('https://www.youtube.com/watch?v=qkUVToIfrKg')
    return

@bot.command(name='oceanman', help='oceanman usage: oceanman')
async def cmd_oceanman(ctx):
    await ctx.send('https://www.youtube.com/watch?v=tkzY_VwNIek')
    return

@bot.command(name='mustardman', help='oceanman usage: mustardman')
async def cmd_mustardman(ctx):
    await ctx.send('https://www.youtube.com/watch?v=V1HdWTsdSSo')
    return

def CreateCommandHelpFile():
    listDecorators = []
    with open(__file__) as f:
        lines = f.readlines()

    for line in lines:
        if "@bot.command" in line and line[0] == '@':
            split_line = line.split(',')
            command_string = line.split(',')[0].split('(')[1].split('=')[1].replace('\'','')
            doc_string = split_line[1].strip().replace(")","").split('=')[1].replace('\'','')
            listDecorators.append((command_string, doc_string))
    return listDecorators

listHelp = CreateCommandHelpFile()
bot.remove_command('help')
@bot.command(name='help', help='Prints this message usage: help')
async def cmd_help(ctx):
    embed = discord.Embed(title="MultiBot Commands", description="List of commands are:", color=0xeee657)
    for ele in listHelp:
        embed.add_field(name=ele[0], value=ele[1], inline=False)

    await ctx.send(embed=embed)

@bot.command(name='quoterandom', help='random quote')
async def quote_random(ctx):
    cursor.execute("SELECT user,message,date_added FROM quotes ORDER BY RANDOM() LIMIT 1")
    query = cursor.fetchone()

    #log
    print(query[0]+": \""+query[1]+"\" printed to the screen "+str(query[2]))

    #embeds the output
    style = discord.Embed(name="responding quote", description="- "+str(query[0])+" "+str(query[2]))
    style.set_author(name=str(query[1]))
    # await ctx.send(embed=style)
    await ctx.send(query[1] + "by " + query[0] + " on " + query[2])

@bot.command(name='quote', help='quote somebody')
async def quote(ctx):
    #identify if there is a user quoted in the string
    split_string = str(ctx.message.content).split()

    if(len(split_string) == 1):
        await quote_random(ctx)
        return
    found_user = False
    user = ""
    text = ""
    for part in split_string:
        print(part)
        if "<@" in part:
            found_user = True
            user = part
        elif "quote" in part:
            pass
        else:
            text += part + " "

    print(text)
    
    if not found_user:
        await ctx.send("There must be a user in the string")
        return

    uniqueID = hash(user+text)

    #date and time of the message
    time = datetime.datetime.now()
    formatted_time = str(time.strftime("%d-%m-%Y %H:%M"))

    #find if message is in the db already
    cursor.execute("SELECT count(*) FROM quotes WHERE hash = ?",(uniqueID,))
    find = cursor.fetchone()[0]

    if find>0:
        return

    #insert into database
    cursor.execute("INSERT INTO quotes VALUES(?,?,?,?)",(uniqueID,user,text,formatted_time))
    await ctx.send("Quote successfully added")

    db.commit()

    #number of words in the database
    rows = cursor.execute("SELECT * from quotes")

    #log to terminal
    print(str(len(rows.fetchall()))+". added - "+str(user)+": \""+str(text)+"\" to database at "+formatted_time)

@bot.command(name='getquote', help='getquote or getquote {name / id of person @Dilly or Dilly}')
async def get_quote(ctx):

    split_string = str(ctx.message.content).split()

    if(len(split_string) == 1):
        await get_quote_self(ctx)
    else:
        await get_quote_other(ctx)

async def get_quote_self(ctx):
    #sanitise name
    user = f"<@!{ctx.author.id}>"
    print(user)

    try:
        #query random quote from user
        query = f"SELECT user,message,date_added FROM quotes WHERE user='{user}' ORDER BY RANDOM() LIMIT 1"
        cursor.execute(query)
        query = cursor.fetchone()

        #log
        print(query[0]+": \""+query[1]+"\" printed to the screen "+str(query[2]))

        style = discord.Embed(name="responding quote", description="- "+str(query[0])+" "+str(query[2]))
        style.set_author(name=str(query[1]))
        # await ctx.send(embed=style)
        await ctx.send(query[1] + "by " + query[0] + " on " + query[2])

    except Exception as e:
        print(e)
        await ctx.send("No quotes of that user found")
    return

async def get_quote_other(ctx):
    #command_params[0] = getquote
    #command_params[1] = either name or "@" of user

    command_params = str(ctx.message.content).split()

    to_return = ""
    id_valid = False


    user = " ".join(command_params[1:])
    if '@' in command_params[1]:
        print(user)
    else:
        print(f"DEBUG: This should be a user ID: {user}")

        user = user.lower()

        if user == "multi":
            print(user)
            user = "<@!142060232867184642>"
        elif user == "dilly":
            print(user)
            user = "<@!117746864035463170>"
        elif user == "kryll":
            print(user)
            user = "<@!96736688251891712>"
        elif user == "chris":
            print(user)
            user = "<@!105759786406010880>"
        elif user == "chrisJ" or user == "chris malevolent" or user == "chris m":
            print(user)
            user = "<@!171463372863176704>"
        elif user == "guge" or user == "gage" or user == "gayge" or user == "shidfard":
            print(user)
            user = "<@!96794466920194048>"
        else:
            print(f"I have no idea who: {user} is")
            await ctx.send(f"I have no idea who {user} is, try again")
            return

    #Name should be the id here <@!numbers>

    try:
        #query random quote from user
        query = f"SELECT user,message,date_added FROM quotes WHERE user='{user}' ORDER BY RANDOM() LIMIT 1"
        cursor.execute(query)
        query = cursor.fetchone()

        #log
        print(query[0]+": \""+query[1]+"\" printed to the screen "+str(query[2]))

        style = discord.Embed(name="responding quote", description="- "+str(query[0])+" "+str(query[2]))
        style.set_author(name=str(query[1]))
        # await ctx.send(embed=style)
        await ctx.send(query[1] + "by " + query[0] + " on " + query[2])

    except Exception as e:
        print(e)
        await ctx.send("No quotes of that user found")
    return

@tasks.loop(seconds=5)
async def bot_background_task():
    # vote background task
    global votes
    if len(votes) > 0:
        t = time.time()
        for v in votes:
            print(v['message'].reactions)
            if v['expires'] < t:
                if len(v['ctx'].message.reactions) > 0:

                    dictReactions = {}
                    for reaction in v['ctx'].message.reactions:
                        dictReactions[str(reaction.emoji)] = []
                        async for user in reaction.users():
                            dictReactions[str(reaction.emoji)].append(user.name)

                    print(dictReactions)

                    users_voted_for = list(set(dictReactions['\U0001F44D']) - set(dictReactions['\U0001F44E']))
                    users_voted_against = list(set(dictReactions['\U0001F44E']) - set(dictReactions['\U0001F44D']))

                    print(users_voted_for)
                    print(users_voted_against)

                    double_voters = len([x for x in users_voted_for if x in users_voted_against]) - 1

                    votes_for = len(dictReactions['\U0001F44D']) - 1 - double_voters
                    votes_against = len(dictReactions['\U0001F44E']) - 1 - double_voters

                    await v['message'].delete()
                    if double_voters == 0:
                        await v['message'].channel.send('The results are in: `%s`\n**%i for**, **%i against**!' % (v['vote_string'], votes_for, votes_against))
                    else:
                        await v['message'].channel.send('The results are in: `%s`\n**%i for**, **%i against**! %i %s voted for both, and their votes were not counted.' % (v['vote_string'], votes_for, votes_against, double_voters, 'person' if double_voters == 1 else 'people'))
                    del v

                    votes[:] = [v for v in votes if v['expires'] > t]
#====================================================================================================================
#===========GAMBA====================================================================================================

@bot.command(name='gambapoints', aliases=['points'],help='Gets your gamba points')
async def gamba_get_points(ctx):
    #get the calling user's id
    userID = f"{ctx.author.id}"
    userName = ctx.author.name
    in_bot_channel = ctx.channel.id == channel_bot_commands
    
    #attempt to get their points
    cursor.execute(f"SELECT points FROM gamba WHERE user = '{userID}'")
    query = cursor.fetchone()    
    #do they have anything?
    if query:                
        message = await ctx.send(f"Hi {userName}! You have {query[0]} points!\n{await int_to_english(query[0])}")        
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
    else:
        message = await ctx.send(f"Hi {userName} I did not find you in our database, adding you with 0 points")    
        await gamba_initalize_user(userID, userName)                
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
    return

async def gamba_get_points(userID):
    #attempt to get their points
    cursor.execute(f"SELECT points FROM gamba WHERE user = '{userID}'")
    query = cursor.fetchone()    
    #do they have anything?
    if query:        
        return query[0]        
    return

async def update_gamba_points(userID, num):
    #attempt to get their points
    cursor.execute(f"SELECT points FROM gamba WHERE user = '{userID}'")
    query = cursor.fetchone()    
    #do they have anything?
    if query:  
        points = query[0]
        points += num
        # await ctx.send(f"Hi {userName}! You have {query[0]} points!")
        cursor.execute(f"UPDATE gamba set points = {points} WHERE user = '{userID}'")
        print(f"Updated user {userID} with points {num}")
        db.commit()
    
async def gamba_initalize_user(userID, userName):
    cursor.execute("INSERT INTO gamba VALUES(?,?,?)",(userID,userName,1000))
    print(f"Added user {userName} to the gamba table with id of {userID}")
    db.commit()

@bot.command(name='gambagivepoints',help='Give points to another player Usage: givepoints # UserName', aliases=['givepoints'])
async def gamba_give_points(ctx):
    userID = ctx.author.id
    userName = ctx.author.name
    in_bot_channel = ctx.channel.id == channel_bot_commands
    
    return

async def int_to_english(num):
    names = { 6  : "Thousand",
              9  : "Million",
              12 : "Billion",
              15 : "Trillion",
              18 : "Quadrillion",
              21 : "Quintillion",
              24 : "Sextillion",
              27 : "Septillion",
              30 : "Octillion",
              33 : "Nonillion",
              36 : "Decillion",
              39 : "Undecillion",
              42 : "Duodecillion",
              45 : "Tredecillion",
              48 : "Quattuordecillion",
              51 : "Quindecillion",
              54 : "Sexdecillion",
              57 : "Septendecillion",
              60 : "Octodecillion",
              63 : "Novemdecillion",
              66 : "Vigintillion",
              69 : "Centillion",
              }
    str_num = str(num)
    num_char = len(str_num)
    while num_char not in names.keys():
        num_char += 1
    ms_num = str_num
    while len(ms_num) > 3:
        ms_num = ms_num[:-3]
    return f"{ms_num} {names[num_char]}"

@bot.command(name='gambaboard',help='slot machine Usage: gambaslots {num}', aliases=['board'])
async def gamba_board(ctx):
    userID = ctx.author.id
    userName = ctx.author.name
    in_bot_channel = ctx.channel.id == channel_bot_commands
    
    cursor.execute(f"SELECT * FROM gamba ORDER by points DESC LIMIT 10")
    query = cursor.fetchall()
    
    leaderboard_output = ""
    places = []
    users = []
    points = []
    for i,ele in enumerate(query):        
        print(f"{i} {ele[1]} {ele[2]}")  
        places.append(str(i))
        users.append(str(ele[1]))
        points.append(ele[2])                
    
    embed = discord.Embed(
        title=("Put That Candy Back Gamba Points Top 10"),     
    )
    place_str = "\n".join(places)
    users_str = "\n".join(users)
    points_str = ""
    for p in points:
        points_str += str(format(int(p), ',d')) + "\n"                             
                           
    embed.add_field(name="Place", value=place_str, inline=True)
    embed.add_field(name="User", value=users_str, inline=True)
    embed.add_field(name="Points", value=points_str, inline=True)
    
    message = await ctx.send(embed=embed)
    if(not in_bot_channel):
        await bot_cleanup(ctx, message)
                
@tasks.loop(seconds=300)
async def gamba_update_all_user_points():
    points_online = 2500
    points_in_vc = 5000
    print(f"\nUpdating user points")
    for guild in bot.guilds:            
        for vc in guild.voice_channels:
            for mem in vc.members:
                userID = mem.id
                #find if message is in the db already
                cursor.execute(f"SELECT * FROM gamba WHERE user='{userID}'")                    
                query = cursor.fetchone()

                if not query:
                    print(f"no user found for member {mem.id} {mem.name}")
                    await gamba_initalize_user(mem.id, mem.name)                                                
                else:
                    print(f"user found for member {mem.id} {mem.name}")   
                    await update_gamba_points(mem.id, points_in_vc)
        # async for mem in guild.fetch_members(limit=150):
        # members = [member for member in bot.get_all_members() if not member.bot]
        for mem in guild.members:            
            if not mem.bot:
                if mem.raw_status == "online":
                    userID = mem.id
                    #find if message is in the db already
                    cursor.execute(f"SELECT * FROM gamba WHERE user='{userID}'")                    
                    query = cursor.fetchone()

                    if not query:
                        print(f"no user found for member {mem.id} {mem.name}")
                        await gamba_initalize_user(mem.id, mem.name)                                                
                    else:
                        print(f"user found for member {mem.id} {mem.name}")   
                        await update_gamba_points(mem.id, points_online)                                      
    return

########################### Gamba games ###########################
@bot.command(name='gambaflip',help='Coin flip gamba. Usage: gambaflip {points}', aliases=['flip'])
async def gamba_flip(ctx):
    userID = ctx.author.id
    userName = ctx.author.name
    in_bot_channel = ctx.channel.id == channel_bot_commands
    
    points_to_bet = str(ctx.message.content).split()
    if len(points_to_bet) != 2:
        message = await ctx.send(f"For some reason you typed too many parameters")           
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
        return
    if not points_to_bet[1].isnumeric():
        message = await ctx.send(f"Second parameter is not a number, what you doin")           
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
        return
        
    points_to_bet = int(points_to_bet[1])    
    points_available = await gamba_get_points(userID)
    
    if points_to_bet > points_available:
        message = await ctx.send(f"Hey {userName}. You only have {points_available}, can't bet {points_to_bet} how about you change that amount")
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
        return
    
    # play game
    flip = random.randint(0, 1)
    if (flip == 0):
        print("Heads")
        await update_gamba_points(userID, points_to_bet)
        points_available = await gamba_get_points(userID) 
        message = await ctx.send(f"HEADS!! {userName} You win {points_to_bet}! You now have {points_available} points")        
    else:
        print("Tails")        
        await update_gamba_points(userID, points_to_bet * -1)
        points_available = await gamba_get_points(userID) 
        message = await ctx.send(f"TAILS!! {userName} You loser! You now have {points_available} points") 
        
    if(not in_bot_channel):
        await bot_cleanup(ctx, message)

@bot.command(name='gambaroll',help='Guess dice result. Win 2x bet. Usage: gambaroll {points} {1-6}',aliases=['roll'])
async def gamba_roll(ctx):
    userID = ctx.author.id
    userName = ctx.author.name
    in_bot_channel = ctx.channel.id == channel_bot_commands
    
    user_input = str(ctx.message.content).split()
    if len(user_input) != 3:
        message = await ctx.send(f"For some reason you typed too many parameters")           
        return
    if not user_input[1].isnumeric():
        message = await ctx.send(f"Second parameter is not a number, what you doin")           
        return
    if not user_input[2].isnumeric():
        message = await ctx.send(f"Third parameter is not a number, what you doin")           
        return
        
    points_to_bet = int(user_input[1])    
    points_available = await gamba_get_points(userID)
    guess_num = int(user_input[2])
    
    if points_to_bet > points_available:
        message = await ctx.send(f"Hey {userName}. You only have {points_available}, can't bet {points_to_bet} how about you change that amount")
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
        return
    if guess_num <= 0 or guess_num > 6:
        message = await ctx.send(f"Hey {userName}. Why guess a number that doesn't appear on a dice")
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
        return
    
    # play game
    choices = range(1,7)
    choice_res = random.choice(choices)
    message = ""
    if choice_res == guess_num:
        points_won = points_to_bet*6
        await update_gamba_points(userID, points_won)
        points_available = await gamba_get_points(userID) 
        message = await ctx.send(f"You win with guess {guess_num} {userName}! You win {points_won}! You now have {points_available} points")        
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
    else:        
        await update_gamba_points(userID, points_to_bet * -1)
        points_available = await gamba_get_points(userID) 
        message = await ctx.send(f"Sorry, rolled a {choice_res} you guessed {guess_num} {userName} You loser! You now have {points_available} points")         
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
    
@bot.command(name='gambaslots', aliases=['slots'], help='slot machine Usage: gambaslots {num}')
async def gamba_slots(ctx):
    userID = ctx.author.id
    userName = ctx.author.name
    in_bot_channel = ctx.channel.id == channel_bot_commands
    
    points_to_bet = str(ctx.message.content).split()
    if len(points_to_bet) != 2:
        message = await ctx.send(f"For some reason you typed too many parameters")           
        #clean up
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
        return

    if "%" not in points_to_bet[1]:
        if not points_to_bet[1].isnumeric():
            message = await ctx.send(f"Second parameter is not a number, what you doin")     
            #clean up
            if(not in_bot_channel):
                await bot_cleanup(ctx, message)      
            return
        points_to_bet = int(points_to_bet[1])    
    else:
        if points_to_bet[1][:-1].isnumeric():
            maybe_points = int(points_to_bet[1][:-1])            
            if maybe_points > 0 and maybe_points <= 100:
                points_available = await gamba_get_points(userID)  
                points_to_bet = int((points_available * maybe_points) / 100)
            else:
                message = await ctx.send(f"Too big or too small, stahp")     
                #clean up
                if(not in_bot_channel):
                    await bot_cleanup(ctx, message)      
                return
            
    points_available = await gamba_get_points(userID)
    
    if points_to_bet > points_available:
        message = await ctx.send(f"Hey {userName}. You only have {points_available}, can't bet {points_to_bet} how about you change that amount")
        #clean up
        if(not in_bot_channel):
            await bot_cleanup(ctx, message)
        return
    
    #play game    
    path = os.path.join(os.path.abspath(os.getcwd()), 'modules/')
    facade = Image.open(f'{path}slot-face.png').convert('RGBA')
    reel = Image.open(f'{path}slot-reel.png').convert('RGBA')

    rw, rh = reel.size
    item = 180
    items = rh//item

    s1 = random.randint(1, items-1)
    s2 = random.randint(1, items-1)
    s3 = random.randint(1, items-1)

    win_rate = 40/100

    if random.random() < win_rate:
        symbols_weights = [3.5, 7, 15, 25, 55] # 
        x = round(random.random()*100, 1)
        pos = bisect.bisect(symbols_weights, x)
        s1 = pos + (random.randint(1, (items/6)-1) * 6)
        s2 = pos + (random.randint(1, (items/6)-1) * 6)
        s3 = pos + (random.randint(1, (items/6)-1) * 6)
        # ensure no reel hits the last symbol
        s1 = s1 - 6 if s1 == items else s1
        s2 = s2 - 6 if s2 == items else s2
        s3 = s3 - 6 if s3 == items else s3

    images = []
    speed = 6
    for i in range(1, (item//speed)+1):
        bg = Image.new('RGBA', facade.size, color=(255,255,255))
        bg.paste(reel, (25 + rw*0, 100-(speed * i * s1)))
        bg.paste(reel, (25 + rw*1, 100-(speed * i * s2))) # dont ask me why this works, but it took me hours
        bg.paste(reel, (25 + rw*2, 100-(speed * i * s3)))
        bg.alpha_composite(facade)
        images.append(bg)

    fp = str(id(ctx.author.id))+'.gif'
    images[0].save(
        fp,
        save_all=True,
        append_images=images[1:], # append all images after first to first
        duration=50  # duration of each slide (ms)
    )

    #win logic             
    # (1+s1)%6 gets the symbol 0-5 inclusive
    if (1+s1)%6 == (1+s2)%6 == (1+s3)%6:
        symbol = (1+s1)%6
        reward = [4, 80, 40, 25, 10, 5][symbol] * points_to_bet
        result = ('won', reward)        
        await update_gamba_points(userID, reward)
        points_available = await gamba_get_points(userID) 
        # await ctx.send(f"WIN") 
    else:
        result = ('lost', points_to_bet * -1)       
        await update_gamba_points(userID, points_to_bet * -1)
        points_available = await gamba_get_points(userID) 
        # await ctx.send(f"LOSE") 
            
    embed = discord.Embed(
        title=(
            f"{userName} {result[0]} {str(format(int(result[1]), ',d'))} credits"+
            ('.' if result[0] == 'lost' else '!') # happy or sad based on outcome
        ),
        description=( f"You have {str(format(int(points_available), ',d'))} points"),
        color=(
            discord.Color.red() if result[0] == "lost"
            else discord.Color.green()
        )
    )

    file = discord.File(fp, filename=fp)
    embed.set_image(url=f"attachment://{fp}") # none of this makes sense to me :)    
    message = await ctx.send(file=file, embed=embed)
    os.remove(fp)
    if(not in_bot_channel):
        await bot_cleanup(ctx, message)            

#====================================================================================================================
########################################################################
@bot.command(name='test', help='my test function')
async def test(ctx):
    for guild in bot.guilds:            
        for vc in guild.voice_channels:
            print(f"name {vc.name}")
            print(f"members {vc.members}")
            print(len(vc.members))
            for mem in vc.members:
                if mem.raw_status == "online":
                    userID = mem.id
                        #find if message is in the db already
                    cursor.execute(f"SELECT * FROM gamba WHERE user='{userID}'")                    
                    query = cursor.fetchone()

                    if not query:
                        print(f"no user found for member {mem.id} {mem.name}")
                        await gamba_initalize_user(ctx, mem.id, mem.name)                                                
                    else:
                        print(f"user found for member {mem.id} {mem.name}")                    
                    # print(f"member name {mem.name}")  
                    # print(f"status {mem.status}")
                    # print(f"id {mem.id}")                    
                    # print(f"raw_status {mem.raw_status}")
                    # print(f"desktop_status {mem.desktop_status}")
                    # print(f"web_status {mem.web_status}")
                    # print(f"mobile_status {mem.mobile_status}")
                    # print("\n")
        member_count = guild.member_count
        print(f"Total member count: {member_count}")
        # async for mem in guild.fetch_members(limit=150):
        # members = [member for member in bot.get_all_members() if not member.bot]
        for mem in guild.members:            
            if not mem.bot and mem.raw_status == "online":
                userID = mem.id
                    #find if message is in the db already
                cursor.execute(f"SELECT * FROM gamba WHERE user='{userID}'")                    
                query = cursor.fetchone()

                if not query:
                    print(f"no user found for member {mem.id} {mem.name}")
                    await gamba_initalize_user(ctx, mem.id, mem.name)                                                
                else:
                    print(f"user found for member {mem.id} {mem.name}")   
                    
                # print(f"member name {mem.name}")  
                # print(f"status {mem.status}")
                # print(f"id {mem.id}")            
                # print(f"raw_status {mem.raw_status}")
                # print(f"desktop_status {mem.desktop_status}")
                # print(f"web_status {mem.web_status}")
                # print(f"mobile_status {mem.mobile_status}")
                # print("\n")
                                      
    return

    
@bot.event
async def on_reaction_add(reaction, user):
    """
    This is called when a message has a reaction added to it.
    The message is stored in ``reaction.message``.
    For older messages, it's possible that this event
    might not get triggered.
    Args:
        reaction:
            A Reaction object of the current state of the reaction.
        user:
            An User or Member object of the user who added the reaction.
    """
    global votes
    print(user, "added", reaction, "to", reaction.message)
    print(reaction.message.reactions)
    
@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    #bot_background_task_debug.start()
    gamba_update_all_user_points.start()
    
async def bot_cleanup(ctx, message):
    #clean up
    # DELETE BOT MESSAGE
    ## wait for 10 seconds
    await asyncio.sleep(10)
    ## delete the bot message
    await message.delete()
    
    # DELETE USER MESSAGE
    message = ctx.message
    ## delete the message
    await message.delete()
    
@tasks.loop(seconds=5)
async def bot_background_task_debug():
    channel = bot.get_channel(channel_bot_commands)
    embed=discord.Embed(title=f"ANNOUNCEMENT GUYS !",description="description",color=0x9208ea)
    embed.set_footer(text="test test")

    await channel.send(embed=embed)

bot_background_task.start()
bot.run(discord_token)




