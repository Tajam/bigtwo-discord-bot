from discord.ext import commands
from discord.utils import get
import datetime
import asyncio
from datetime import date
import time
import os

BOOTED = False
RETRY_TOGGLE = True
RETRY_DELAY_INIT = 15
RETRY_DELAY = 15
RETRY_COUNT_INIT = 10
RETRY_COUNT = 10
BOT_TIME = datetime.datetime.now()
BOT_PATH = os.getcwd().replace('\\','/')
ASSET_PATH = BOT_PATH +'/Assets/'
ADMIN_ID = ['245580232587870208','456772953862832129']

def write_command(caller ,command):
    return caller + ' sends a ' + command + ' command to the bot.'

def write_picture(caller, picture):
    return caller + ' request a picture upload of ' + picture + ' from the bot.'

BOT_MSG = dict()
BOT_MSG['Dead'] = 'AnotherBot fall into a deep sleep.'
BOT_MSG['Start'] = 'AnotherBot started service.'
BOT_MSG['Reboot'] = 'AnotherBot recovered from disconnection.'
BOT_MSG['Uptime'] = 'Admin checks bot uptime.'
BOT_MSG['DoRetry'] = 'Admin flips the do retry toggle.'
BOT_MSG['Notice'] = 'Admin sends a bot notice.'
BOT_MSG['Ping'] = 'Admin sends a ping to the bot.'
BOT_MSG['Reconnect'] = 'AnotherBot tried hard to reconnect.'
BOT_MSG['Command'] = write_command
BOT_MSG['Picture'] = write_picture
#Tajam, Twiska

#Server Bot
#TOKEN = 'NDU3NTQ3MzEyMDMwNDE2OTAz.DgasAg.pRN3qnSk_wuXU3CRiuRayOJWoe8'
TOKEN = 'NTA5NzYyMTc5Nzk3NjE0NTk0.DsShNA.4cmFaTrp0mDZnjK8r3hAUEz_Pyw'
#AnotherBotLogs
def write_log_inter(logmsg):
    file = open(BOT_PATH + '/AnotherBotLogs/' + str(date.today())+'.log','a+')
    timenow = str(datetime.datetime.now())[:-7]
    file.write('['+timenow+'] '+logmsg+'\n')
    file.close()

async def write_log(logmsg):
    write_log_inter(logmsg)

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    global BOOTED, BOT_MSG
    print('AnotherBot started!')
    await write_log(BOT_MSG['Start']);
    if BOOTED:
        for server in bot.servers: 
           for channel in server.channels: 
               if channel.permissions_for(server.me).send_messages:
                   await bot.send_message(channel, BOT_MSG['Reboot'])
                   await write_log(BOT_MSG['Reboot'])
                   break
    else:
        BOOTED = True

#Admin Command
@bot.command(pass_context=True)
async def uptime(ctx):
    callmsg = ctx.message
    #Delete message
    await bot.delete_message(callmsg)
    #Admin filter
    if callmsg.author.id in ADMIN_ID:
        timenow = datetime.datetime.now()
        msg = '```Bot uptime: '
        msg += str(timenow - BOT_TIME)[:-7]
        msg += '```'
        await bot.send_message(callmsg.author, msg)
        await write_log(BOT_MSG['Uptime'])
        #await bot.say(msg)

@bot.command(pass_context=True)
async def doretry(ctx):
    global RETRY_TOGGLE
    callmsg = ctx.message
    #Delete message
    await bot.delete_message(callmsg)
    #Admin filter
    if callmsg.author.id in ADMIN_ID:
        RETRY_TOGGLE = not RETRY_TOGGLE
        msg = '```Retry toogle status: ' + str(RETRY_TOGGLE) + '```'
        await bot.send_message(callmsg.author, msg)
        await write_log(BOT_MSG['DoRetry'])

@bot.command(pass_context=True)
async def notice(ctx, *text):
    callmsg = ctx.message
    #Delete message
    await bot.delete_message(callmsg)
    #Admin filter
    if callmsg.author.id in ADMIN_ID:
        msg = '```Bot notice``````'
        msg += ' '.join(text)
        msg += '```'
        await bot.say(msg)
        await write_log(BOT_MSG['Notice'])

@bot.command(pass_context=True)
async def ping(ctx):
    callmsg = ctx.message
    #Delete message
    await bot.delete_message(callmsg)
    #Admin filter
    if callmsg.author.id in ADMIN_ID:
        await bot.send_message(callmsg.author, 'Bot is still up!')
        await write_log(BOT_MSG['Ping'])

#Bot Command
@bot.command(pass_context=True)
async def me(ctx, *act):
    callmsg = ctx.message
    #Delete message
    await bot.delete_message(callmsg)
    #Action process
    author = callmsg.author.display_name
    action = ' '.join(act)
    #Output
    print('MeAction function printed by ' + author)
    await bot.say('**' + author + ' **' + action)
    await write_log(BOT_MSG['Command'](author, 'ME'))

@bot.command(pass_context=True)
async def quote(ctx ,name, *qot):
    callmsg = ctx.message
    #Delete message
    await bot.delete_message(callmsg)
    #Action process
    text = ' '.join(qot)
    words = '*' + text + '*'
    dtime = str(datetime.date.today())
    #Me means the caller itself
    if name == 'me':
        name = callmsg.author.display_name
    sign = '-**' + name + '** (' + dtime + ')'
    msg = words + '\n\n' + sign
    #Output
    author = callmsg.author.display_name
    print('Quote function printed by ' + author)
    await bot.say(msg)
    await write_log(BOT_MSG['Command'](author, 'QUOTE'))

@bot.command(pass_context=True)
async def cum(ctx, emoji_name = '%^&*No-Emoji*&^%'):
    callmsg = ctx.message
    #Delete message
    await bot.delete_message(callmsg)        
    #Get all emoji
    emoji = bot.get_all_emojis()
    head_emoji = str(get(emoji, name='AwOo'))
    tail_emoji = str()
    if emoji_name != '%^&*No-Emoji*&^%':
        print('Cum function receiving emoji: ' + emoji_name)
        if not ((emoji_name[0] == '<')&(emoji_name[-1] == '>')):
            tail_emoji = str(get(emoji, name=emoji_name))
            if tail_emoji == 'None':
                await bot.say('Emoji not found, please try another one.')
                return
        else:
            tail_emoji = emoji_name
        print('Cum function returned emoji: ' + tail_emoji)
    #Generate message
    msg = ''
    msg += head_emoji + '\n'
    msg += ' '*6 + ':eggplant:\n'
    msg += ' '*16 + ':sweat_drops:'
    if emoji_name != '%^&*No-Emoji*&^%':
        msg += '\n' + ' '*28 + tail_emoji
    #Output
    author = callmsg.author.display_name
    print('Cum function printed!')
    await bot.say(msg)
    await bot.say('Posted by ' + author)
    await write_log(BOT_MSG['Command'](author, 'CUM'))

@bot.command(pass_context=True)
async def hokage(ctx, *faces):
    callmsg = ctx.message
    #Delete message
    await bot.delete_message(callmsg)
    #Detect number of face
    if len(faces) > 6:
        await bot.say('Emoji number overflow, please try again.')
        return
    #Get all emoji
    emoji = bot.get_all_emojis()
    dmoji = ['None' for n in range(6)]
    for n, i in enumerate(faces):
        if not ((i[0] == '<')&(i[-1] == '>')&('><' not in i)):
            dmoji[n] = str(get(emoji, name=i))
        else:
            dmoji[n] = i
    #Original HOKAGE
    omoji = list()
    omoji.append(str(get(emoji, name='qh_handsome')))
    omoji.append(str(get(emoji, name='jw_handsome')))
    omoji.append(str(get(emoji, name='kw_handsome')))
    omoji.append(str(get(emoji, name='jh_handsome')))
    omoji.append(str(get(emoji, name='cj_handsome')))
    #Have no idea why this did not work
    omoji.append('<:jc_handsome:458680379247689750>')
    #Elements
    element_text = ':fire::ocean::leaves::cookie::zap::eye_in_speech_bubble:'
    hokage_words = 'hokage'
    region_words = ':regional_indicator_'
    #Generate message
    msg = ''
    for n, i in enumerate(dmoji):
        if i == 'None':
            msg += omoji[n]
        else:
            msg += i
    msg += '\n'
    for i in hokage_words:
        msg += region_words + i + ':'
    msg += '\n'
    msg += element_text
    #Output
    author = callmsg.author.display_name
    print('Hokage function printed!')
    await bot.say(msg)
    await bot.say('Posted by ' + author)
    await write_log(BOT_MSG['Command'](author, 'HOKAGE'))

@bot.command(pass_context=True)
async def big(ctx, *text):
    callmsg = ctx.message
    #Delete message
    await bot.delete_message(callmsg)
    #Supported symbol
    support_symbol = dict()
    support_symbol[ord('0')] = ':zero:'
    support_symbol[ord('1')] = ':one:'
    support_symbol[ord('2')] = ':two:'
    support_symbol[ord('3')] = ':three:'
    support_symbol[ord('4')] = ':four:'
    support_symbol[ord('5')] = ':five:'
    support_symbol[ord('6')] = ':six:'
    support_symbol[ord('7')] = ':seven:'
    support_symbol[ord('8')] = ':eight:'
    support_symbol[ord('9')] = ':nine:'
    support_symbol[ord('*')] = ':asterisk:'
    support_symbol[ord('#')] = ':hash:'
    support_symbol[ord('!')] = ':exclamation:'
    support_symbol[ord('?')] = ':question:'
    support_symbol[ord('$')] = ':heavy_dollar_sign:'
    support_symbol[ord('+')] = ':heavy_plus_sign:'
    support_symbol[ord('-')] = ':heavy_minus_sign:'
    #Check limit and generate message
    author = callmsg.author.display_name
    msg = '```' + author + '```\n'
    if len(text) > 5:
        await bot.say('Maximum input word is 5, please cut down your word number.')
        return
    region_words = ':regional_indicator_'
    for n in text:
        if len(n) > 20:
            await bot.say('Maximum input letter per word is 20, please cut down your letter number.')
            return
        else:
            for m in n:
                if ord(m) in support_symbol:
                    msg += support_symbol[ord(m)]
                    continue
                if ord(m) < ord('a'):
                    m = chr(ord(m)+32)
                if (ord(m) < ord('a'))|(ord(m) > ord('z')):
                    continue
                msg += region_words + m + ':'
            msg += '\n'
    #Output
    print('Big function printed!')
    await bot.say(msg)
    await write_log(BOT_MSG['Command'](author, 'BIG'))

#=====IMAGE COMMAND BELOW=====

@bot.command(pass_context=True)
async def adminface(ctx):
    callmsg = ctx.message
    destination = callmsg.channel
    #Delete message
    await bot.delete_message(callmsg)
    author = callmsg.author.display_name
    image_name = 'Admin.jpg'
    await bot.send_file(destination, ASSET_PATH + image_name)
    await bot.say('Posted by ' + author)
    await write_log(BOT_MSG['Picture'](author, image_name))

@bot.command(pass_context=True)
async def iamgay(ctx):
    callmsg = ctx.message
    destination = callmsg.channel
    #Delete message
    author = callmsg.author.display_name
    image_name = 'IamGay.jpg'
    await bot.delete_message(callmsg) 
    await bot.send_file(destination, ASSET_PATH + image_name)
    await bot.say('Posted by ' + author)
    await write_log(BOT_MSG['Picture'](author, image_name))

@bot.command(pass_context=True)
async def duckman(ctx):
    callmsg = ctx.message
    destination = callmsg.channel
    #Delete message
    author = callmsg.author.display_name
    image_name = 'Duckman.jpg'
    await bot.delete_message(callmsg) 
    await bot.send_file(destination, ASSET_PATH + image_name)
    await bot.say('Posted by ' + author)
    await write_log(BOT_MSG['Picture'](author, image_name))

@bot.command(pass_context=True)
async def noobhai(ctx):
    callmsg = ctx.message
    destination = callmsg.channel
    #Delete message
    author = callmsg.author.display_name
    image_name = 'NoobHai.jpg'
    await bot.delete_message(callmsg) 
    await bot.send_file(destination, ASSET_PATH + image_name)
    await bot.say('Posted by ' + author)
    await write_log(BOT_MSG['Picture'](author, image_name))

@bot.command(pass_context=True)
async def huehuehue(ctx):
    callmsg = ctx.message
    destination = callmsg.channel
    #Delete message
    author = callmsg.author.display_name
    image_name = 'HueHueHue.jpg'
    await bot.delete_message(callmsg) 
    await bot.send_file(destination, ASSET_PATH + image_name)
    await bot.say('Posted by ' + author)
    await write_log(BOT_MSG['Picture'](author, image_name))

@bot.command(pass_context=True)
async def hokagerock(ctx):
    callmsg = ctx.message
    destination = callmsg.channel
    #Delete message
    author = callmsg.author.display_name
    image_name = 'HokageRock.jpg'
    await bot.delete_message(callmsg) 
    await bot.send_file(destination, ASSET_PATH + image_name)
    await bot.say('Posted by ' + author)
    await write_log(BOT_MSG['Picture'](author, image_name))

while(RETRY_TOGGLE):
    try:
        bot.loop.run_until_complete(bot.start(TOKEN))
        RETRY_DELAY = RETRY_DELAY_INIT
        RETRY_COUNT = RETRY_COUNT_INIT
        #bot.run(TOKEN)
    except BaseException:
        print('Connection error, retry in '+str(RETRY_DELAY)+' seconds.')
        RETRY_COUNT -= 1
        if RETRY_COUNT <= 0:
            RETRY_COUNT = RETRY_COUNT_INIT
            RETRY_DELAY *= 2
            write_log_inter(BOT_MSG['Reconnect'])
        if RETRY_DELAY >= 1920:
            break
        time.sleep(RETRY_DELAY)

write_log_inter(BOT_MSG['Dead'])
