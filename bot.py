#https://github.com/Giphy/giphy-python-client

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

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
giphy_token = os.getenv('GIPHY_TOKEN')

bot = commands.Bot(command_prefix='$')
api_instance = giphy_client.DefaultApi()
client = discord.Client()

votes = []


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
    #debug print
    #await ctx.send(votes)

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
async def cmd_crabrave(ctx):
    await ctx.send('https://www.youtube.com/watch?v=qkUVToIfrKg')
    return

@bot.command(name='oceanman', help='oceanman usage: oceanman')
async def cmd_oceanman(ctx):
    await ctx.send('https://www.youtube.com/watch?v=tkzY_VwNIek')
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

#setup helpfile
listHelp = CreateCommandHelpFile()

bot.remove_command('help')
@bot.command(name='help', help='Prints this message usage: help')
async def cmd_help(ctx):
    embed = discord.Embed(title="MultiBot Commands", description="List of commands are:", color=0xeee657)
    for ele in listHelp:
        embed.add_field(name=ele[0], value=ele[1], inline=False)

    await ctx.send(embed=embed)

# @client.event
# async def on_message(message):
#     print(message)

@tasks.loop(seconds=5)
async def bot_background_task():
    global votes
    if len(votes) > 0:
        t = time.time()
        for v in votes:
            print(v['message'].reactions)
            if v['expires'] < t:
                # print(v['message'])
                # print(v['message'].channel.name)
                # print(client.get_all_channels())
                # for guild in client.guilds:
                #     for channel in guild.channels:
                #         print(channel)
                # channel_vote_came_from = get_channel(client.get_all_channels(), v['message'].channel.name)
                # await v['message'].channel.send('asdf')
                # print(channel_vote_came_from)
                # v['message'] = await client.get_guild(v['message'].guild.id).get_channel(v['message'].id)

                #await v['ctx'].send('test')



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

@bot.command(name='test', help='my test function')
async def test(ctx):
    global votes
    for v in votes:
        print(v['ctx'].message.reactions)
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
async def on_reaction_remove(reaction, user):
    print(user, "added", reaction, "to", reaction.message)

bot_background_task.start()
bot.run(discord_token)



