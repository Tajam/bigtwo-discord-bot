##from discord.ext import commands
##import datetime
##import random
##from PlayingCard import Card, Skill
##
##BOOTED = False
##RETRY_DELAY = 5
###Game functions
##Card.set_bossval(2)
##
##GAME_START = False
##GAME_GOING = False
##GAME_HOST = 0
##GAME_MAXPLAYER = 4
##GAME_PLAYER = []
##
##THE_CARDS = [n for n in range(52)]
##FORCE_STOPPER = []
##PLAYERS_CARD = dict()
##
##FREE_TO_THROW = True
##CARD_ON_TABLE = list()
##CARD_SKILL = 0
##CARD_OWNER = 0
##PASS_COMBO = 0
##WHOS_TURN = 0
##
##VALUE_EMOJI = dict()
##VALUE_EMOJI[1] = ':regional_indicator_a:'
##VALUE_EMOJI[2] = ':two:'
##VALUE_EMOJI[3] = ':three:'
##VALUE_EMOJI[4] = ':four:'
##VALUE_EMOJI[5] = ':five:'
##VALUE_EMOJI[6] = ':six:'
##VALUE_EMOJI[7] = ':seven:'
##VALUE_EMOJI[8] = ':eight:'
##VALUE_EMOJI[9] = ':nine:'
##VALUE_EMOJI[10] = ':keycap_ten:'
##VALUE_EMOJI[11] = ':regional_indicator_j:'
##VALUE_EMOJI[12] = ':regional_indicator_q:'
##VALUE_EMOJI[13] = ':regional_indicator_k:'
##
##SYMBOL_EMOJI = dict()
##SYMBOL_EMOJI[1] = ':spades:'
##SYMBOL_EMOJI[2] = ':hearts:'
##SYMBOL_EMOJI[3] = ':clubs:'
##SYMBOL_EMOJI[4] = ':diamonds:'
##
##def ALL_RESET():
##    global GAME_START
##    global GAME_GOING
##    global GAME_HOST
##    global GAME_PLAYER
##    global FORCE_STOPPER
##    global THE_CARDS
##    global PLAYERS_CARD
##    global FREE_TO_THROW
##    global CARD_ON_TABLE
##    global CARD_SKILL
##    global PASS_COMBO
##    global WHOS_TURN
##    global CARD_OWNER
##    
##    GAME_START = False
##    GAME_GOING = False
##    GAME_HOST = 0
##    GAME_PLAYER = []
##
##    THE_CARDS = [n for n in range(52)]
##    FORCE_STOPPER = []
##    PLAYERS_CARD = dict()
##
##    FREE_TO_THROW = True
##    CARD_ON_TABLE = list()
##    CARD_SKILL = 0
##    CARD_OWNER = str()
##    PASS_COMBO = 0
##    WHOS_TURN = 0
##
##    print('Game full reset!')
##
###Server Functions
##def next_turn():
##    global GAME_PLAYER, WHOS_TURN
##    for n in GAME_PLAYER:
##        if len(PLAYERS_CARD[n]) == 0:
##            ALL_RESET()
##            return n.display_name
##    WHOS_TURN += 1
##    if WHOS_TURN >= len(GAME_PLAYER):
##        WHOS_TURN = 0
##    return ''
##
##async def show_table(channel):
##    global GAME_PLAYER, WHOS_TURN, CARD_ON_TABLE, CARD_SKILL, CARD_OWNER, FREE_TO_THROW
##    SKILL_NAME = dict()
##    SKILL_NAME[1] = 'Straight'
##    SKILL_NAME[2] = 'Flush'
##    SKILL_NAME[3] = 'Full House'
##    SKILL_NAME[4] = 'Four of a Kind'
##    SKILL_NAME[5] = 'Straight Flush'
##
##    msg = '```Currently: '
##    if CARD_SKILL.type == 'skill':
##        msg += SKILL_NAME[CARD_SKILL.srank]
##    else:
##        msg += CARD_SKILL.type
##    msg += ' by ' + CARD_OWNER + '```'
##    for n in CARD_ON_TABLE:
##        msg += SYMBOL_EMOJI[n.symbol] + VALUE_EMOJI[n.value] + '\n'
##    msg += '``` Current turn: ' + GAME_PLAYER[WHOS_TURN].display_name
##    if FREE_TO_THROW:
##        msg += ' (Free to throw)'
##    msg += '```'
##    await bot.send_message(channel, msg)  
##
##async def show_win(channel, player_name):
##    msg = '```Player ' + player_name + ' win the game!```'
##    await bot.send_message(channel, msg)
##
###Server Bot
###TOKEN = 'NDU3OTI0MzMyNzU3NDUwNzYz.Dggbqw.DAPMYAaAyIXLkxnVNm-IBdRmxak'
##TOKEN = 'NTA5NzYyMTc5Nzk3NjE0NTk0.DsShNA.4cmFaTrp0mDZnjK8r3hAUEz_Pyw'
##
##bot = commands.Bot(command_prefix='-')
###Bot Event
##@bot.event
##async def on_ready():
##    global BOOTED
##    print('DangerousBot started!')
##    if BOOTED:
##        for server in bot.servers: 
##           for channel in server.channels: 
##               if channel.permissions_for(server.me).send_messages:
##                   await bot.send_message(channel, bot.user.display_name + ' recovered from disconnection!')
##                   break
##    else:
##        BOOTED = True
##
##bot.remove_command('help')
###Bot Command
##@bot.command(pass_context = True)
##async def create(ctx):
##    global GAME_START, GAME_HOST, GAME_PLAYER
##    await bot.delete_message(ctx.message)
##    if GAME_START == False:
##        user_host = ctx.message.author
##        GAME_HOST = user_host
##        GAME_PLAYER.append(GAME_HOST)
##        GAME_START = True
##        await bot.say('Game created, user host: ' + user_host.display_name)
##    else:
##        await bot.say('Game already created by someone: ' + GAME_HOST.display_name)
##        await bot.say('Type \"-join\" to join ' + GAME_HOST.display_name + '\'s game!')
##
##@bot.command(pass_context = True)
##async def stop(ctx):
##    global GAME_START, GAME_HOST, GAME_PLAYER
##    await bot.delete_message(ctx.message)
##    if GAME_START == True:
##        user_caller = ctx.message.author
##        if GAME_HOST == user_caller:
##            if GAME_GOING:
##                for n in GAME_PLAYER:
##                    await bot.send_message(n, '```Game force ended```')
##            ALL_RESET()
##            await bot.say('Game ended by host: ' + user_caller.display_name)
##
##@bot.command(pass_context = True)
##async def join(ctx):
##    global GAME_START, GAME_GOING, GAME_HOST, GAME_MAXPLAYER
##    await bot.delete_message(ctx.message)
##    if GAME_START == True:
##        user_caller = ctx.message.author
##        if GAME_GOING:
##            await bot.say('Game is on-going. Wait for next game, ' + user_caller.display_name + '!')
##            return
##        if not user_caller in GAME_PLAYER:
##            if len(GAME_PLAYER) < 4:
##                GAME_PLAYER.append(user_caller)
##                await bot.say(user_caller.display_name + ' joined the game hosted by ' + GAME_HOST.display_name + '!')
##                await bot.say('Game slot left: ' + str(len(GAME_PLAYER)) + '/' + str(GAME_MAXPLAYER))
##            else:
##                await bot.say('Game is full. Wait for next game, ' + user_caller.display_name + '!')
##        else:
##            await bot.say('You already joined the game, ' + user_caller.display_name + '!')
##
##@bot.command(pass_context = True)
##async def leave(ctx):
##    global GAME_START, GAME_GOING, GAME_HOST, GAME_MAXPLAYER
##    await bot.delete_message(ctx.message)
##    if GAME_START == True:
##        user_caller = ctx.message.author
##        if GAME_GOING:
##            await bot.say('Game is on-going. You can\'t leave now, ' + user_caller.display_name + '!')
##            return
##        if user_caller in GAME_PLAYER:
##            GAME_PLAYER.remove(user_caller)
##            await bot.say(user_caller.display_name + ' has left the game!')
##            await bot.say('Game slot left: ' + str(len(GAME_PLAYER)) + '/' + str(GAME_MAXPLAYER))
##
##@bot.command(pass_context = True)
##async def forcestop(ctx):
##    global GAME_START, GAME_HOST, GAME_PLAYER, FORCE_STOPPER
##    await bot.delete_message(ctx.message)
##    if GAME_START == True:
##        user_caller = ctx.message.author
##        if GAME_HOST == user_caller:
##            if GAME_GOING:
##                for n in GAME_PLAYER:
##                    await bot.send_message(n, '```Game force ended```')
##            ALL_RESET()
##            await bot.say('Game ended by host: ' + user_caller.display_name)
##        else:
##            if (user_caller in GAME_PLAYER)&(not user_caller in FORCE_STOPPER):
##                FORCE_STOPPER.append(user_caller)
##                await bot.say('Force stop vote count: ' + str(len(FORCE_STOPPER)) + '/' + str(len(GAME_PLAYER)-1))
##                if len(FORCE_STOPPER) >= len(GAME_PLAYER)-1:
##                    if GAME_GOING:
##                        for n in GAME_PLAYER:
##                            await bot.send_message(n, '```Game force ended```')
##                    ALL_RESET()
##                    await bot.say('Game force ended by players.')
##
##@bot.command(pass_context = True)
##async def start(ctx):
##    global GAME_START, GAME_GOING, GAME_HOST, GAME_PLAYER, PLAYERS_CARD
##    await bot.delete_message(ctx.message)
##    if (GAME_START == True)&(GAME_GOING == False):
##        user_caller = ctx.message.author
##        if GAME_HOST == user_caller:
##            if len(GAME_PLAYER) > 1:
##                GAME_GOING = True
##                random.shuffle(THE_CARDS)
##                card_each_player = int(52/len(GAME_PLAYER))
##                
##                for n in GAME_PLAYER:
##                    temp_card_list = []
##                    for m in range(card_each_player):
##                        temp_card_list.append(Card(THE_CARDS.pop()))
##                    Card.sort_card(temp_card_list)
##                    PLAYERS_CARD[n] = list(temp_card_list)
##                for n in GAME_PLAYER:
##                    msg = '```Your card here:``` \n'
##                    for m in range(len(PLAYERS_CARD[n])):
##                        msg += '`' + '0'*(len(str(m)) == 1) + str(m) + '`' + SYMBOL_EMOJI[PLAYERS_CARD[n][m].symbol] + VALUE_EMOJI[PLAYERS_CARD[n][m].value] + '\n'
##                    await bot.send_message(n, msg)
##                await bot.say('Game started, I have private messaged all of your cards!')
##                await bot.say('Please check out your private message box!')
##                await bot.say('Host start first!')
##
###On going state
##@bot.command(pass_context = True)
##async def throw(ctx, *cards_index):
##    global GAME_GOING, GAME_PLAYER, PLAYERS_CARD, WHOS_TURN, FREE_TO_THROW, CARD_ON_TABLE, CARD_SKILL, PASS_COMBO, CARD_OWNER
##    await bot.delete_message(ctx.message)
##    cards = list()
##    update = False
##    if GAME_GOING:
##        user_caller = ctx.message.author
##        if (user_caller in GAME_PLAYER)&(GAME_PLAYER.index(user_caller) == WHOS_TURN)&(len(cards_index) > 0):
##            for n in cards_index:
##                cards.append(PLAYERS_CARD[user_caller][int(n)])
##            THIS_SKILL = Skill(cards)
##            if THIS_SKILL.valid:
##                if not FREE_TO_THROW:
##                    if CARD_SKILL.type == THIS_SKILL.type:
##                        if THIS_SKILL.type == 'skill':
##                            if THIS_SKILL.srank > CARD_SKILL.srank:
##                                update = True
##                            if THIS_SKILL.srank == CARD_SKILL.srank:
##                                if Card.fight_against(THIS_SKILL.leader, CARD_SKILL.leader, (CARD_SKILL.srank == 2)|(CARD_SKILL.srank == 5)):
##                                    update = True
##                        else:
##                            if Card.fight_against(THIS_SKILL.leader, CARD_SKILL.leader):
##                                update = True
##                else:
##                    FREE_TO_THROW = False
##                    update = True
##    if update:
##        del_list = [int(n) for n in cards_index]
##        PLAYERS_CARD[user_caller] = [i for j, i in enumerate(PLAYERS_CARD[user_caller]) if j not in del_list]
##        CARD_ON_TABLE = list(cards)
##        CARD_SKILL = Skill(cards)
##        PASS_COMBO = 0
##        CARD_OWNER = user_caller.display_name
##        winner = next_turn()
##        await show_table(ctx.message.channel)
##        if winner != '':
##            await show_win(ctx.message.channel,winner)
##            for n in GAME_PLAYER:
##                if n.display_name == winner:
##                    await bot.send_message(n, '```You win the game, Game over!```')
##                else:
##                    await bot.send_message(n, '```You lost the game, Game over!```')
##        else:
##            msg = '```Updated:``` \n'
##            for m in range(len(PLAYERS_CARD[user_caller])):
##                msg += '`' + '0'*(len(str(m)) == 1) + str(m) + '`' + SYMBOL_EMOJI[PLAYERS_CARD[user_caller][m].symbol] + VALUE_EMOJI[PLAYERS_CARD[user_caller][m].value] + '\n'
##            await bot.send_message(user_caller, msg)
##
##@bot.command(pass_context = True)
##async def skip(ctx):
##    global GAME_GOING, GAME_PLAYER, WHOS_TURN, FREE_TO_THROW, PASS_COMBO
##    await bot.delete_message(ctx.message)
##    if GAME_GOING:
##        user_caller = ctx.message.author
##        if (user_caller in GAME_PLAYER)&(GAME_PLAYER.index(user_caller) == WHOS_TURN):
##            PASS_COMBO += 1
##            if PASS_COMBO >= len(GAME_PLAYER) - 1:
##                FREE_TO_THROW = True
##            next_turn()
##            await bot.say('```' + user_caller.display_name + ' pass the turn!```')
##            await show_table(ctx.message.channel)
##            
##@bot.command(pass_context = True)
##async def now(ctx):
##    global GAME_GOING, GAME_PLAYER, WHOS_TURN
##    await bot.delete_message(ctx.message)
##    if GAME_GOING:
##        user_caller = ctx.message.author
##        if (user_caller in GAME_PLAYER)&(GAME_PLAYER.index(user_caller) == WHOS_TURN):
##            await show_table(ctx.message.channel)
##
##while(True):
##    try:
##        bot.loop.run_until_complete(bot.start(TOKEN))
##        #bot.run(TOKEN)
##    except BaseException:
##        print('Connection error, retry in '+str(RETRY_DELAY)+' seconds.')
##        time.sleep(RETRY_DELAY)
