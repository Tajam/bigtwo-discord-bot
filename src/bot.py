from discord.ext import commands
from bigtwo import BigTwo
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
    
while(True):
    try:
        bot.loop.run_until_complete(bot.start(TOKEN))
        #bot.run(TOKEN)
    except BaseException:
        print('Connection error, retry in '+str(RETRY_DELAY)+' seconds.')
        time.sleep(RETRY_DELAY)
