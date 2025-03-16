from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from comment_checker import check_kyedae_comment
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, LiveEndEvent

import asyncio
import discord
import os


load_dotenv()
token = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)

connected = False
client = None
username = ""

channel = None
output_channel = None

current_date = datetime.today().date()
count = 0


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def connect(ctx, usernameInput):
    global channel, client, username

    channel = ctx.channel
    username = f"@{usernameInput}"

    client = TikTokLiveClient(unique_id=username)
    client.on(CommentEvent)(on_comment)
    client.on(LiveEndEvent)(on_live_end)

    await ctx.send(f"Connecting to **{username}**'s live")

    try:
        await client.connect() 
    except Exception as e:
        global connected
        connected = False
            
        await ctx.send(f"**Failed:** Unable to connect on **{username}**'s live  **):**")


@bot.command()
async def disconnect(ctx):
    global client, connected, username
    
    client = None
    connected = False

    if username != "":
        await ctx.send(f"**Success: ** Disconnected to **{username}**'s live")
        username =""
    else:
        await ctx.send("**Error:** Currently not connected to any live")



@bot.command()
async def setoutchan(ctx, channel_id: str = None):
    global output_channel

    if channel_id is None:
        output_channel = ctx.channel
        await ctx.send(f"**Success:** Output channel was set to channel **`{output_channel.name}`**")
        return

    try:
        output_channel = bot.get_channel(int(channel_id))
    except Exception as e:
        await ctx.send("**Error:** Invalid input for channel ID.")
        return

    print(output_channel)

    if output_channel is not None:
        await ctx.send(f"**Success:** Output channel was set to channel **`{output_channel.name}`**")
    else:
        await ctx.send(f"**Failed:** Channel for channel ID **`{channel_id}`** not found")
        

@bot.command()
async def bye(ctx):
    global count, current_date, output_channel

    if output_channel is None:
        await ctx.send("**Failed:** Output channel not found\nSet output channel:  `>setoutchan` or `>setoutchan [channelID]`")
        return
    
    await output_channel.send(f"## Today's log:\n```Date:  {current_date}\nCount: {count}```")

    await bot.close()
    os._exit(0)


@bot.command()
async def goodnight(ctx):
    await ctx.send("Good night  **(:**")

    await bot.close()
    os._exit(0) 


@bot.command()
async def inc(ctx, num: str = None):
    global channel, count
    
    if num is None: 
        num = 1
    else:
        try:
            num = int(num)  
        except Exception as e:
            await ctx.send("**Error:** Invalid input for a number")
            return
        
    if num <= 0:
        await ctx.send("**Error:** Invalid increment value")
        return

    count += num

    await ctx.send(f"Counter Manually Updated:  **+{num}**")
    await ctx.send(f"```Kyedae:  {count}```")


@bot.command()
async def dec(ctx, num: str = None):
    global channel, count
    
    if num is None: 
        num = 1
    else:
        try:
            num = int(num)
        except Exception as e:
            await ctx.send("**Error:** Invalid input for a number")
            return

    if num <= 0:
        await ctx.send("**Error:** Invalid decrement value")
        return

    if count - num >= 0:
        count -= num
    else:
        await ctx.send("**Error:**  Counter cannot be less than 0")
        return

    await ctx.send(f"Counter Manually Updated:  **-{num}**")
    await ctx.send(f"```Kyedae:  {count}```")


async def on_comment(event: CommentEvent):
    global channel, client, connected, username, count

    if client is None:
        return

    if not connected:
        connected = True
        await channel.send(f"**Success:** Connected to  **{username}**'s live  **(:**")

    if (check_kyedae_comment(event.comment)):
        count += 1
        await channel.send(f"{event.user.nickname}:  ` {event.comment} `")
        await channel.send(f"```Kyedae:  {count}```")
    #else:
        #await channel.send(f"{event.user.nickname}:  `{event.comment}`")
    
    # await channel.send(f"{event.user.nickname}:  `{event.comment}`")

    await asyncio.sleep(0.5)


async def on_live_end(event: LiveEndEvent):
    global channel, output_channel, username
    message = f"## Today's log:\n```Date:  {current_date}\nCount: {count}```"

    await channel.send(f"**{username}**'s live has ended")

    if output_channel is not None:
        await output_channel.send(message)
    elif channel is not None:
        await channel.send(message)
    

bot.run(token)
