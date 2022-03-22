import random as rnd
import time
from math import ceil

import discord
from discord.ext import commands

from bigtwo import BigTwo
from server import Server
from stats import Stats


# Global functions
def get_token():
    with open(".token", "r") as f:
        return f.read()


def context_unpack(ctx):
    s = ctx.message.guild.id if ctx.message.guild else None
    c = ctx.message.channel.id
    n = ctx.message.author.id
    l = "{}-{}".format(s, c)
    return [s, c, n, l]


async def message_board_state(player_pool, messages):
    for p in player_pool:
        player = player_pool[p]
        if len(player.player_board_messages) == 0:
            await player.player_object.send(
                "- - - - - - - - - - - - - - - - Current 𝄜 - - - - - - - - - - - - - - - -"
            )
            if len(messages) == 0:
                player.player_board_messages.append(
                    await player.player_object.send("-" + " " * 99 + "-")
                )
                player.player_board_messages.append(
                    await player.player_object.send("-" + " " * 99 + "-")
                )
            else:
                for mi, message in enumerate(messages):
                    player.player_board_messages.append(
                        await player.player_object.send(message)
                    )
        else:
            for mi, message in enumerate(messages):
                if mi < len(player.player_board_messages):
                    await player.player_board_messages[mi].edit(content=message)


async def message_status(
    player_pool, group_message, specific_player=None, specific_player_message=None,
):
    for p in player_pool:
        player = player_pool[p]
        if player.player_status_message == None:
            await player.player_object.send(
                "- - - - - - - - - - - - - - - - Current ⚐ - - - - - - - - - - - - - - - -"
            )
            if p == specific_player:
                player.player_status_message = await player.player_object.send(
                    specific_player_message
                )
            else:
                player.player_status_message = await player.player_object.send(
                    group_message
                )
        else:
            if p == specific_player:
                await player.player_status_message.edit(content=specific_player_message)
            else:
                await player.player_status_message.edit(content=group_message)


# Game functions
async def direct_message_card(player_pool):
    for p in player_pool:
        player = player_pool[p]
        emoji_list = [
            f"{next(filter(lambda emoji: emoji_name == emoji.name , bot.emojis))}"
            for emoji_name in player.get_card_discord_format()
        ]

        index_dict = {
            0: "| 0 | | 1 | | 2 | | 3 | | 4  | | 5 | | 6 | | 7 | ",
            1: "| 8 | | 9 | | 10 || 11 || 12 || 13 || 14 || 15 | ",
            2: "| 16 || 17 || 18 || 19 || 20 || 21 || 22 || 23 | ",
            3: "| 24 || 25 || 26 || 27 || 28 || 29 || 30 || 31 | ",
            4: "| 32 || 33 || 34 || 35 || 36 || 37 || 38 || 39 | ",
            5: "| 40 || 41 || 42 || 43 || 44 || 45 || 46 || 47 | ",
            6: "| 48 || 49 || 50 || 51 | ",
        }

        messages = []

        for i in range(ceil(len(emoji_list) / 8.0)):
            single_line_emoji_list = emoji_list[i * 8 : (i + 1) * 8]
            messages.append("".join(single_line_emoji_list))
            messages.append(
                f"```{'|'.join(index_dict[i].split('|')[: len(single_line_emoji_list) * 2])}|```"
            )

        if len(player.player_hand_messages) == 0:
            await player.player_object.send(
                "- - - - - - - - - - - - - - - - Current ✋ - - - - - - - - - - - - - - - -"
            )

            for message in messages:
                player.player_hand_messages.append(
                    await player.player_object.send(message)
                )
        else:
            for mi, message in enumerate(messages):
                if mi >= len(player.player_hand_messages):
                    player.player_hand_messages.append(
                        await player.player_object.send(message)
                    )
                else:
                    await player.player_hand_messages[mi].edit(content=message)


async def direct_message_winner(ctx, lobby):
    place = {0: "🥇", 1: "🥈", 2: "🥉"}
    message = ""
    for index, winner in enumerate(lobby.winners):
        message += f"{place[index]}: <@{winner}>\n"

    message += "Game Over!"
    for p in lobby.player_pool:
        player = lobby.player_pool[p]
        await player.player_object.send(message)


async def show_board(ctx, lobby):
    owner = lobby.current_owner
    combo = lobby.current_combo
    if combo is None:
        return
    card_list_msg = [f"{str(card)}" for card in combo.card_list]
    emoji_list = [
        f"{next(filter(lambda emoji: emoji_name == emoji.name , bot.emojis))}"
        for emoji_name in card_list_msg
    ]
    card_left = len(lobby.player_pool[owner].cards)
    description = f"`{combo._type.capitalize()} by` <@{owner}> `{card_left} card{'s' * int(card_left > 1)} left`"
    messages = [f"{''.join(emoji_list)}", f"{description}"]
    [await ctx.send(msg) for msg in messages]
    await message_board_state(lobby.player_pool, messages)


async def show_turn(ctx, lobby):
    player = lobby.whos_turn()
    owner = lobby.current_owner
    combo = lobby.current_combo
    msg = "It's your turn. <@{}>".format(player)
    if combo == None:
        msg += "\nIt's free to throw."
    await ctx.send(msg)


# Constants
TOKEN = get_token()
RETRY_DELAY = 60
MAX_NUMBER = 26

# Server object for lobbies
SERVER = Server("BigTwo")
STATS = Stats()
stats = STATS.read_stats_file()
# Instantiate bot and set command prefix
bot = commands.Bot(command_prefix="-")

# Events
@bot.event
async def on_ready():
    activity = discord.Game(name="-help", type=4)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("BigTwo bot is up...")


# Remove build-in command
bot.remove_command("help")

# Commands - General
@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command(pass_context=True)
async def random(ctx, mode="card", number=1):
    if number > MAX_NUMBER:
        await ctx.send("Limit number is {}".format(MAX_NUMBER))
        return
    s = ""
    if mode == "card":
        s = [
            "`{:0>2d}` {}".format(n + 1, BigTwo.DECK.get_random().emoji())
            for n in range(number)
        ]
    if mode == "suit":
        s = [
            "`{:0>2d}` {}".format(n + 1, BigTwo.SUITSET.get_random()._emoji)
            for n in range(number)
        ]
    if mode == "rank":
        s = [
            "`{:0>2d}` {}".format(n + 1, BigTwo.RANKSET.get_random()._emoji)
            for n in range(number)
        ]
    await ctx.send("\n".join(s))


@bot.command(pass_context=True, aliases=["f"])
async def flip(ctx, number=1):
    if number > MAX_NUMBER:
        await ctx.send("Limit number is {}".format(MAX_NUMBER))
        return
    r = ["`Head`", "`Tail`"]
    s = ["`{:0>2d}` `{}`".format(n + 1, r[rnd.randint(0, 1)]) for n in range(number)]
    await ctx.send("\n".join(s))


@bot.command(pass_context=True, aliases=["r"])
async def refresh(ctx):
    s, c, n, l = context_unpack(ctx)
    if l not in SERVER.lobby_list:

        def find_lobby_id(item):
            l_id, lob = item
            if n in lob.player_pool:
                return True
            return False

        l, _ = next(filter(find_lobby_id, SERVER.lobby_list.items(),))

    if n not in SERVER.lobby_list[l].player_pool:
        return
    if not SERVER.lobby_list[l].started:
        return
    player = SERVER.lobby_list[l].player_pool[n]
    board_messages = player.player_board_messages
    status_message = player.player_status_message
    player.player_hand_messages = []
    player.player_status_message = None
    player.player_board_messages = []
    single_player = {n: player}
    await message_board_state(
        single_player, [message_object.content for message_object in board_messages]
    )
    await message_status(single_player, status_message.content)
    await direct_message_card(single_player)


@bot.command(pass_context=True, aliases=["h"])
async def hands(ctx):
    s, c, n, l = context_unpack(ctx)
    if l not in SERVER.lobby_list:

        def find_lobby_id(item):
            l_id, lob = item
            if n in lob.player_pool:
                return True
            return False

        l, _ = next(filter(find_lobby_id, SERVER.lobby_list.items(),))

    for player_id in SERVER.lobby_list[l].player_pool:
        if n != player_id:
            await ctx.send(
                f"<@{player_id}> has {len(SERVER.lobby_list[l].player_pool[player_id].cards)} card left."
            )


# Commands - Lobby
@bot.command(pass_context=True, aliases=["c"])
async def create(ctx):
    s, c, n, l = context_unpack(ctx)
    delete_dead_lobby = False
    for lobby in SERVER.lobby_list:
        if n in SERVER.lobby_list[lobby].player_pool:
            if discord.utils.find(
                lambda m: m.id == int(lobby.split("-")[1]), ctx.guild.text_channels
            ):
                await ctx.send(
                    "You already joined a game in other channel. <@{}>".format(n)
                )
                return
            else:
                delete_dead_lobby = True
    if delete_dead_lobby:
        del SERVER.lobby_list[lobby]
    if SERVER.add_lobby(s, c):
        await ctx.send("<@{}> created a game in this channel.".format(n))
        SERVER.lobby_list[l].join(ctx.message.author)
        SERVER.lobby_list[l].set_host(n)
        return
    await ctx.send("This channel is occupied. <@{}>".format(n))


@bot.command(pass_context=True, aliases=["j"])
async def join(ctx):
    s, c, n, l = context_unpack(ctx)
    if l in SERVER.lobby_list:
        if SERVER.lobby_list[l].started:
            return
        if n in SERVER.lobby_list[l].player_pool:
            await ctx.send("Already joined this game. <@{}>".format(n))
            return
        if len(SERVER.lobby_list[l].player_pool) == 4:
            await ctx.send("This game is full. <@{}>".format(n))
            return
        for lobby in SERVER.lobby_list:
            if n in SERVER.lobby_list[lobby].player_pool:
                await ctx.send(
                    "You already joined a game in other channel. <@{}>".format(n)
                )
                return
        if SERVER.lobby_list[l].join(ctx.message.author):
            await ctx.send("Joined game! <@{}>".format(n))
            return
        await ctx.send("Sorry, this game is full. <@{}>".format(n))


@bot.command(pass_context=True, aliases=["l"])
async def leave(ctx):
    s, c, n, l = context_unpack(ctx)
    if l in SERVER.lobby_list:
        if n not in SERVER.lobby_list[l].player_pool:
            await ctx.send("You did not join any game. <@{}>".format(n))
            return
        if not SERVER.lobby_list[l].started:
            if SERVER.lobby_list[l].leave(ctx.message.author):
                SERVER.remove_lobby(s, c)
                await ctx.send("Everyone has left the game, game closed.")
                return
            await ctx.send("Game left! <@{}>".format(n))
            if SERVER.lobby_list[l].host_id == n:
                new_host = SERVER.lobby_list[l].set_random_host()
                await ctx.send(
                    "Host left, <@{}> is assigned as new host.".format(new_host)
                )
                return


@bot.command(pass_context=True, aliases=["go", "g"])
async def start(ctx):
    s, c, n, l = context_unpack(ctx)
    if l in SERVER.lobby_list:
        if SERVER.lobby_list[l].started:
            await ctx.send("Game already started. <@{}>".format(n))
            return
        if len(SERVER.lobby_list[l].player_pool) < 2:
            await ctx.send("This game need at least 2 players. <@{}>".format(n))
            return
        SERVER.lobby_list[l].start()
        await ctx.send("Game started! Your cards will be direct messaged to you.")
        # Set up DM board state for all players
        await message_board_state(SERVER.lobby_list[l].player_pool, {})
        await show_turn(ctx, SERVER.lobby_list[l])
        await message_status(
            SERVER.lobby_list[l].player_pool,
            f"It's <@{SERVER.lobby_list[l].whos_turn()}>'s turn.",
            SERVER.lobby_list[l].whos_turn(),
            "It's your turn.",
        )
        await direct_message_card(SERVER.lobby_list[l].player_pool)


@bot.command(pass_context=True, aliases=["kill", "k"])
async def stop(ctx):
    s, c, n, l = context_unpack(ctx)
    if l in SERVER.lobby_list:
        if n != SERVER.lobby_list[l].host_id:
            await ctx.send("You are not the host. <@{}>".format(n))
            return
        del SERVER.lobby_list[l]
        await ctx.send("Game stopped by host.")


# Sort cards
@bot.command(pass_context=True)
async def sort(ctx, sort_value="n"):
    _, _, n, l = context_unpack(ctx)

    if l not in SERVER.lobby_list:

        def find_lobby_id(item):
            l_id, lob = item
            if n in lob.player_pool:
                return True
            return False

        l, _ = next(filter(find_lobby_id, SERVER.lobby_list.items(),))

    if n not in SERVER.lobby_list[l].player_pool:
        return
    if not SERVER.lobby_list[l].started:
        return

    player = SERVER.lobby_list[l].player_pool[n]

    player.sort_cards(sort_value)
    await direct_message_card({n: player})


@bot.command(pass_context=True, aliases=["t", "play", "p"])
async def throw(ctx, *args):
    _, _, n, l = context_unpack(ctx)

    if l not in SERVER.lobby_list:

        def find_lobby_id(item):
            l_id, lob = item
            if n in lob.player_pool:
                return True
            return False

        l, _ = next(filter(find_lobby_id, SERVER.lobby_list.items(),))

    if n not in SERVER.lobby_list[l].player_pool:
        return
    if not SERVER.lobby_list[l].started:
        return
    indexes = []
    try:
        indexes = [int(n) for n in args]
    except Exception:
        await ctx.send("Invalid input. <@{}>".format(n))
        return
    player = SERVER.lobby_list[l].player_pool[n]
    player_cards = player.cards
    if max(indexes) >= len(player_cards):
        await ctx.send("Index exceed card number. <@{}>".format(n))
        return
    cards = player.peek_cards(indexes)
    res = SERVER.lobby_list[l].attack(n, cards)
    res_msg = [
        "Not your turn. <@{}>".format(n),
        "Invalid card combination. <@{}>".format(n),
        "Opponent card is better. <@{}>".format(n),
    ]
    if res != 0 and res != 4:
        await ctx.send(res_msg[res - 1])
        return
    player.throw_cards(indexes)

    player.player_hand_messages = []
    player.player_status_message = None
    player.player_board_messages = []

    channel = ctx.message.channel
    if type(channel) is discord.DMChannel:
        channel = bot.get_channel(int(l.split("-")[1]))
    await show_board(channel, SERVER.lobby_list[l])

    # Check victory
    if len(player.cards) == 0:
        SERVER.lobby_list[l].add_winner(n)
        place = {1: "first place", 2: "second place", 3: "third place"}

        await channel.send(
            f"<@{n}> wins the {place[len(SERVER.lobby_list[l].winners)]}!"
        )
        if len(SERVER.lobby_list[l].player_turn) == 1:
            await direct_message_winner(ctx, SERVER.lobby_list[l])
            STATS.update_stats(
                SERVER.lobby_list[l].winners, SERVER.lobby_list[l].player_pool.keys()
            )
            del SERVER.lobby_list[l]
            return

    await show_turn(channel, SERVER.lobby_list[l])
    if len(player.cards) == 0:
        await message_status(
            SERVER.lobby_list[l].player_pool,
            f"<@{n}> has won. <@{SERVER.lobby_list[l].whos_turn()}> can play anything.",
            SERVER.lobby_list[l].whos_turn(),
            f"<@{n}> has won so you can play anything.",
        )
    elif res == 4:
        await message_status(
            SERVER.lobby_list[l].player_pool,
            f"Your turn has been skipped. <@{SERVER.lobby_list[l].whos_turn()}> played an unbeatable combo.",
            SERVER.lobby_list[l].whos_turn(),
            "It's your turn.",
        )
    else:
        await message_status(
            SERVER.lobby_list[l].player_pool,
            f"It's <@{SERVER.lobby_list[l].whos_turn()}>'s turn.",
            SERVER.lobby_list[l].whos_turn(),
            "It's your turn.",
        )
    await direct_message_card({n: SERVER.lobby_list[l].player_pool[n]})


@bot.command(pass_context=True, aliases=["pass", "s"])
async def skip(ctx, *args):
    _, _, n, l = context_unpack(ctx)

    if l not in SERVER.lobby_list:

        def find_lobby_id(item):
            l_id, lob = item
            if n in lob.player_pool:
                return True
            return False

        l, _ = next(filter(find_lobby_id, SERVER.lobby_list.items(),))

    if n not in SERVER.lobby_list[l].player_pool:
        return
    if not SERVER.lobby_list[l].whos_turn() == n:
        return
    if SERVER.lobby_list[l].current_combo == None:
        await ctx.send("You cannot skip a free throw round. <@{}>".format(n))
        return
    SERVER.lobby_list[l].next_turn()
    channel = ctx.message.channel
    if type(channel) is discord.DMChannel:
        channel = bot.get_channel(int(l.split("-")[1]))
    await show_board(channel, SERVER.lobby_list[l])
    await channel.send(
        f"<@{n}> skipped. It's <@{SERVER.lobby_list[l].player_turn[0]}> turn."
    )
    await message_status(
        SERVER.lobby_list[l].player_pool,
        f"<@{n}> skipped. It's <@{SERVER.lobby_list[l].player_turn[0]}> turn.",
    )


@bot.command(pass_context=True)
async def help(ctx):
    help_message = """```BigTwoBot Command List:
Set-up Commands:
-[create/c] Creates a game lobby
-[join/j] Joins current game lobby
-[start/go/g] Starts a game, once started no other players may join, needs at least 2 players before you start the game
-[leave/l] Leaves a lobby or game
-[stop] Stops a game or game lobby
-[stat] Shows points, wins, and losses
Gameplay Commands:
-[throw/play/p] # (# # # #) Plays cards by index from current hand
-[skip/s] Skips your turn
-[sort] (n/s) Sorts your hand numerically or by suit
-[refresh/r] Refresh the view of the current board, status, and hand (used when there is an error with message)
-[hands/h] Shows hand size of all other players```"""
    await ctx.send(help_message)


@bot.command(pass_context=True, aliases=["stat"])
async def stats(ctx):
    await ctx.send(STATS.get_stats(bot, ctx.message.author.id))


while True:
    try:
        bot.loop.run_until_complete(bot.start(TOKEN))
    except BaseException:
        print("Connection error, retry in " + str(RETRY_DELAY) + " seconds.")
        time.sleep(RETRY_DELAY)
