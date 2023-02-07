import random as rnd
import time
from math import ceil

import discord
from discord.ext import commands

from bigtwo import BigTwo
from server import Server, Lobby
from stats import Stats


# Global functions
def get_token():
    with open(".token", "r") as f:
        return f.read()


bot = discord.Bot()

def context_unpack(ctx):
    s = ctx.guild_id
    c = ctx.channel_id
    n = ctx.author.id
    l = f"{s}-{c}"
    return [s, c, n, l]


async def message_board_state(player_pool: dict, messages: str):
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
    player_pool: dict,
    group_message: str,
    specific_player: str = None,
    specific_player_message: str = None,
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
async def direct_message_card(player_pool: dict):
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


async def direct_message_winner(ctx, lobby: Lobby):
    place = {0: "🥇", 1: "🥈", 2: "🥉"}
    message = ""
    for index, winner in enumerate(lobby.winners):
        message += f"{place[index]}: <@{winner}>\n"

    message += "Game Over!"
    for p in lobby.player_pool:
        player = lobby.player_pool[p]
        await player.player_object.send(message)


async def show_board(ctx, lobby: Lobby):
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


async def show_turn(ctx, lobby: Lobby):
    player = lobby.whos_turn()
    owner = lobby.current_owner
    combo = lobby.current_combo
    msg = "It's your turn. <@{}>".format(player)
    if combo == None:
        msg += "\nYou are free to play anything."
    await ctx.respond(msg)


# Constants
TOKEN = get_token()
RETRY_DELAY = 60
MAX_NUMBER = 26

# Server object for lobbies
SERVER = Server("BigTwo")
STATS = Stats()
stats = STATS.read_stats_file()

# Events
@bot.event
async def on_ready():
    activity = discord.Game(name="-help", type=4)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("BigTwo bot is up...")


# Commands - General
@bot.slash_command()
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


@bot.slash_command()
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
            await ctx.respond(
                f"<@{player_id}> has {len(SERVER.lobby_list[l].player_pool[player_id].cards)} card left."
            )


# Commands - Lobby
@bot.slash_command()
async def create(ctx):
    s, c, n, l = context_unpack(ctx)
    delete_dead_lobby = False
    for lobby in SERVER.lobby_list:
        if n in SERVER.lobby_list[lobby].player_pool:
            if discord.utils.find(
                lambda m: m.id == int(lobby.split("-")[1]), ctx.guild.text_channels
            ):
                await ctx.respond(
                    f"You already joined a game in other channel. <@{n}>"
                )
                return
            else:
                delete_dead_lobby = True
    if delete_dead_lobby:
        del SERVER.lobby_list[lobby]
    if SERVER.add_lobby(s, c):
        await ctx.respond(f"<@{n}> created a game in this channel.")
        SERVER.lobby_list[l].join(ctx.author)
        SERVER.lobby_list[l].set_host(n)
        return
    await ctx.respond(f"This channel is occupied. <@{n}>")


@bot.slash_command()
async def join(ctx):
    s, c, n, l = context_unpack(ctx)
    if l in SERVER.lobby_list:
        if SERVER.lobby_list[l].started:
            return
        if n in SERVER.lobby_list[l].player_pool:
            await ctx.respond(f"Already joined this game. <@{n}>")
            return
        if len(SERVER.lobby_list[l].player_pool) == 4:
            await ctx.respond(f"This game is full. <@{n}>")
            return
        for lobby in SERVER.lobby_list:
            if n in SERVER.lobby_list[lobby].player_pool:
                await ctx.respond(
                    f"You already joined a game in other channel. <@{n}>"
                )
                return
        if SERVER.lobby_list[l].join(ctx.author):
            await ctx.respond(f"Joined game! <@{n}>")
            return
        await ctx.respond(f"Sorry, this game is full. <@{n}>")


@bot.slash_command()
async def leave(ctx):
    s, c, n, l = context_unpack(ctx)
    if l in SERVER.lobby_list:
        if n not in SERVER.lobby_list[l].player_pool:
            await ctx.respond(f"You did not join any game. <@{n}>")
            return
        if not SERVER.lobby_list[l].started:
            if SERVER.lobby_list[l].leave(ctx.author):
                SERVER.remove_lobby(s, c)
                await ctx.respond("Everyone has left the game, game closed.")
                return
            await ctx.respond(f"Game left! <@{n}>")
            if SERVER.lobby_list[l].host_id == n:
                new_host = SERVER.lobby_list[l].set_random_host()
                await ctx.respond(
                    f"Host left, <@{n}> is assigned as new host.".format(new_host)
                )
                return


@bot.slash_command()
async def start(ctx):
    s, c, n, l = context_unpack(ctx)
    if l not in SERVER.lobby_list:
        await ctx.respond("You have to create a lobby first and have players \"/join\" the lobby.")
        return
    if SERVER.lobby_list[l].started:
        await ctx.respond(f"Game already started. <@{n}>")
        return
    if len(SERVER.lobby_list[l].player_pool) < 2:
        await ctx.respond(f"This game need at least 2 players. <@{n}>")
        return
    SERVER.lobby_list[l].start()
    await ctx.respond("Game started! Your cards will be direct messaged to you.")
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


@bot.slash_command()
async def stop(ctx):
    s, c, n, l = context_unpack(ctx)
    if l in SERVER.lobby_list:
        if n != SERVER.lobby_list[l].host_id:
            await ctx.respond(f"You are not the host. <@{n}>")
            return
        del SERVER.lobby_list[l]
        await ctx.respond("Game stopped by host.")


# Sort cards
@bot.slash_command()
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
    await ctx.respond(
        f"Cards have been sorted by {'number' if sort_value == 'n' else 'suit'}"
    )


@bot.slash_command()
async def play(ctx, *, cards):
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
        indexes = [int(n) for n in cards.split(" ")]
    except Exception:
        await ctx.respond(f"Invalid input. <@{n}>")
        return
    player = SERVER.lobby_list[l].player_pool[n]
    player_cards = player.cards
    if max(indexes) >= len(player_cards):
        await ctx.respond(f"Index exceed card number. <@{n}>")
        return
    cards = player.peek_cards(indexes)
    res = SERVER.lobby_list[l].attack(n, cards)
    res_msg = [
        f"Not your turn. <@{n}>",
        f"Invalid card combination. <@{n}>",
        f"Opponent card/combo is better. <@{n}>",
    ]
    if res != 0 and res != 4:
        await ctx.respond(res_msg[res - 1])
        return
    player.play_cards(indexes)

    player.player_hand_messages = []
    player.player_status_message = None
    player.player_board_messages = []

    channel = bot.get_channel(int(l.split("-")[1]))

    await show_board(channel, SERVER.lobby_list[l])

    # Check victory
    if len(player.cards) == 0:
        SERVER.lobby_list[l].add_winner(n)
        place = {1: "first place", 2: "second place", 3: "third place"}

        await ctx.respond(
            f"<@{n}> wins the {place[len(SERVER.lobby_list[l].winners)]}!"
        )
        if len(SERVER.lobby_list[l].player_turn) == 1:
            await direct_message_winner(ctx, SERVER.lobby_list[l])
            STATS.update_stats(
                SERVER.lobby_list[l].winners, SERVER.lobby_list[l].player_pool.keys()
            )
            del SERVER.lobby_list[l]
            return

    await show_turn(ctx, SERVER.lobby_list[l])
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


@bot.slash_command()
async def skip(ctx):
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
        await ctx.respond(f"You cannot skip a free play round. <@{n}>")
        return

    SERVER.lobby_list[l].next_turn()
    await ctx.respond(
        f"<@{n}> skipped. It's <@{SERVER.lobby_list[l].player_turn[0]}> turn."
    )

    channel = bot.get_channel(int(l.split("-")[1]))

    await show_board(channel, SERVER.lobby_list[l])
    await message_status(
        SERVER.lobby_list[l].player_pool,
        f"<@{n}> skipped. It's <@{SERVER.lobby_list[l].player_turn[0]}> turn.",
    )    


@bot.slash_command()
async def help(ctx):
    help_message = """```BigTwoBot Command List:
Set-up Commands:
/[create] Creates a game lobby
/[join] Joins current game lobby
/[start] Starts a game, once started no other players may join, needs at least 2 players before you start the game
/[leave] Leaves a lobby or game
/[stop] Stops a game or game lobby
/[stat] Shows points, wins, and losses
Gameplay Commands:
/[play] # (# # # #) Plays cards by index from current hand
/[skip] Skips your turn
/[sort] (n/s) Sorts your hand numerically or by suit
/[refresh] Refresh the view of the current board, status, and hand (used when there is an error with message)
/[hands] Shows hand size of all other players```"""
    await ctx.respond(help_message)


@bot.slash_command()
async def stats(ctx):
    await ctx.respond(STATS.get_stats(ctx))


while True:
    try:
        bot.run(TOKEN)
    except BaseException:
        print("Connection error, retry in " + str(RETRY_DELAY) + " seconds.")
        time.sleep(RETRY_DELAY)
