from discord.ext import commands
from bigtwo import BigTwo
from server import Server, Lobby
import random as rnd
import time

#Global functions
def get_token():
    with open('.token', 'r') as f:
        return f.read()

#Constants
TOKEN = get_token()
RETRY_DELAY = 60
MAX_NUMBER = 26

#Server object for lobbies
SERVER = Server('BigTwo')

#Instantiate bot and set command prefix
bot = commands.Bot(command_prefix='-')

#Events
@bot.event
async def on_ready():
    print('BigTwo bot is up...')

#Remove build-in command
bot.remove_command('help')

#Commands - General
@bot.command(pass_context = False)
async def ping():
    await bot.say('Pong!')

@bot.command(pass_context = False)
async def random(mode = 'card',number = 1):
    if number > MAX_NUMBER:
        await bot.say('Limit number is {}'.format(MAX_NUMBER))
        return
    s = ''
    if mode == 'card':
        s = ['`{:0>2d}` {}'.format(n+1, BigTwo.DECK.get_random().emoji()) for n in range(number)]
    if mode == 'suit':
        s = ['`{:0>2d}` {}'.format(n+1, BigTwo.SUITSET.get_random()._emoji) for n in range(number)]
    if mode == 'rank':
        s = ['`{:0>2d}` {}'.format(n+1, BigTwo.RANKSET.get_random()._emoji) for n in range(number)]
    await bot.say('\n'.join(s))

@bot.command(pass_context = False)
async def flip(number = 1):
    if number > MAX_NUMBER:
        await bot.say('Limit number is {}'.format(MAX_NUMBER))
        return
    r = ['`Head`','`Tail`']
    s = ['`{:0>2d}` `{}`'.format(n+1, r[rnd.randint(0,1)]) for n in range(number)]
    await bot.say('\n'.join(s))

#Commands - Lobby
@bot.command(pass_context = True)
async def create(ctx):
    s = ctx.message.server.id
    c = ctx.message.channel.id
    n = ctx.message.author.id
    l = '{}-{}'.format(s,c)
    if SERVER.add_lobby(s,c):
        await bot.say('<@{}> created a game in this channel!'.format(n))
        SERVER.lobby_list[l].join(ctx.message.author)
        SERVER.lobby_list[l].set_host(n)
        return
    await bot.say('This channel is occupied! <@{}>'.format(n))

@bot.command(pass_context = True)
async def join(ctx):
    s = ctx.message.server.id
    c = ctx.message.channel.id
    n = ctx.message.author.id
    l = '{}-{}'.format(s,c)
    if l in SERVER.lobby_list:
        if n in SERVER.lobby_list[l].player_pool:
            await bot.say('Already joined this game! <@{}>'.format(n))
            return
        if SERVER.lobby_list[l].join(ctx.message.author):
            await bot.say('Joined game! <@{}>'.format(n))
            return
        await bot.say('Sorry, this game is full. <@{}>'.format(n))
        return
    await bot.say('No game available to join yet! <@{}>'.format(n))

@bot.command(pass_context = True)
async def leave(ctx):
    s = ctx.message.server.id
    c = ctx.message.channel.id
    n = ctx.message.author.id
    l = '{}-{}'.format(s,c)
    if l in SERVER.lobby_list:
        if n not in SERVER.lobby_list[l].player_pool:
            await bot.say('You did not join any game! <@{}>'.format(n))
            return
        await bot.say('Game left! <@{}>'.format(n))
        if SERVER.lobby_list[l].leave(ctx.message.author):
            SERVER.remove_lobby(s,c)
            await bot.say('Everyone has left the game, game closed.'.format(n))
            return
        if SERVER.lobby_list[l].host_id == n:
            new_host = SERVER.lobby_list[l].set_random_host()
            await bot.say('Host left, <@{}> is assigned as new host!'.format(new_host))
            return
    await bot.say('You did not join any game! <@{}>'.format(n))

while(True):
    try:
        bot.loop.run_until_complete(bot.start(TOKEN))
        #bot.run(TOKEN)
    except BaseException:
        print('Connection error, retry in '+str(RETRY_DELAY)+' seconds.')
        time.sleep(RETRY_DELAY)
