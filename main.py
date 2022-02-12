import discord
import json
import os

intents = discord.Intents.all()
from decouple import config
from discord.ext import commands

activity = discord.Activity(type=discord.ActivityType.playing, name="LITERALLY ANY OTHER GAME")
client = commands.Bot(command_prefix = '$', activity=activity, status=discord.Status.online, intents=intents)



@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  print("Branch version " + discord.__version__)

async def createChannel(guild):
  for i in guild.channels:
    if(i.name == 'channel-of-shame'):
      channel = i
      return channel
  else:
    channel = await guild.create_text_channel('channel-of-shame')
    await channel.set_permissions(guild.default_role, send_messages=False)
    return channel
  

@client.command()
async def games(ctx, style = " ", game = " "):
  if not ctx.message.author.guild_permissions.administrator:
    await ctx.send("no")
    return
  if style.lower() == 'add' and game != " ":
    with open(f'{os.getcwd()}/guilds/{ctx.guild.id}.json', 'r') as f:
      data = json.load(f)
      if game.lower() not in data['games']:
        data['games'].append(game.lower())
        await ctx.send(game + " added to list :thumbsup:")
      else:
        await ctx.send(game + " is already on the list!")
        return
    with open(f'{os.getcwd()}/guilds/{ctx.guild.id}.json', 'w') as f:
      json.dump(data, f, indent=4)
  elif style.lower() == 'remove' and game != " ":
    with open(f'{os.getcwd()}/guilds/{ctx.guild.id}.json', 'r') as f:
      data = json.load(f)
    if game.lower() in data['games']:
      data['games'].remove(game.lower())
      await ctx.send(game + " removed from the list")
    else:
      await ctx.send(game + " is not in the list!")
      return
    with open(f'{os.getcwd()}/guilds/{ctx.guild.id}.json', 'w') as f:
      json.dump(data, f, indent=4)
  elif style.lower() == 'view':
    f = open(f'{os.getcwd()}/guilds/{ctx.guild.id}.json')
    data = json.load(f)
    await ctx.send(data.get('games'))
  else:
    await ctx.send("Command used incorrectly. Please specify whether you want to 'add', 'remove', or 'view' game list.")


@client.command()
async def resetSettingsToDefault(ctx):
  if not ctx.message.author.guild_permissions.administrator:
    await ctx.send("no")
    return
  try:
    os.remove(f'{os.getcwd()}/guilds/{ctx.guild.id}.json')
  except OSError:
    pass
  await createConfig(ctx.guild)
  await ctx.send("Config file succesfully reset")


@client.command()
async def zeroTolerance(ctx, boo=" "):
  if not ctx.message.author.guild_permissions.administrator:
    await ctx.send("no")
    return
  f = open(f'{os.getcwd()}/guilds/{ctx.guild.id}.json')
  data = json.load(f)
  tolerance = data.get('tolerance')
  if boo.lower() == 'enable' and tolerance == True:
    await ctx.send("Zero Tolerance initiated. Anyone who plays league in this server will be **permanently** banned!")
    tolerance = False
    
  elif boo.lower() == 'enable':
    await ctx.send("You already have Zero Tolerance enabled!")
    return
    
  elif boo.lower() == 'disable' and tolerance == False:
    await ctx.send("Zero Tolerance disabled!")
    tolerance = True
    
  elif boo.lower() == 'disable':
    await ctx.send("Zero Tolerance was not enabled so it was not disabled.")
    return
    
  elif boo.lower() == " ":
    await ctx.send("Zero Tolerance is " + str(tolerance).lower() + ". If you wish to change that, please specify whether you want to 'enable' or 'disable' zero tolerance")
    return
    
  else:
    await ctx.send("Not a valid input. Please say 'enable' for zero tolerance, or 'disable' if you want to be merciful")
    return
  
  with open(f'{os.getcwd()}/guilds/{ctx.guild.id}.json', 'r') as f:
    data = json.load(f)
    data['tolerance'] = tolerance 
  with open(f'{os.getcwd()}/guilds/{ctx.guild.id}.json', 'w') as f:
    json.dump(data, f, indent=4)


@client.event
async def on_member_update(before, after):
  try:
    f = open(f'{os.getcwd()}/guilds/{after.guild.id}.json')
  except FileNotFoundError:
    await createConfig(after.guild)
    f = open(f'{os.getcwd()}/guilds/{after.guild.id}.json')
  data = json.load(f)
  games = data.get('games')
  if after.activity and after.activity.name.lower() in games:
    
    if before.activity is None:
      await punish(after, data)
    elif not before.activity.name.lower() in games:
      await punish(after, data)


async def punish(after, data):
  tolerance = data.get('tolerance')
  channel = client.get_channel(data.get('channelID'))
  messages = data.get('messages')
  if tolerance:
    await channel.send(f"{after.mention} is playing {after.activity.name.lower()} :sick:")
  else:
    await channel.send(f"{after.mention} plays league!!!! BANNED :sick::sick::sick:")
    await after.ban(reason = "ZERO TOLERANCE FOR LEAGUE PLAYERS")


@client.event
async def on_guild_remove(guild):
  try:
    os.remove(f'{os.getcwd()}/guilds/{guild.id}.json')
  except OSError:
    pass


@client.event
async def on_guild_join(guild):
  await createConfig(guild)


async def createConfig(guild):
  channel = await createChannel(guild)
  default = {
    "games" : ["league of legends"],
    "tolerance" : True,
    "messages" : ["{after.mention} is playing {after.activity.name.lower()} :sick:"],
    "channelID" : channel.id
  }

  json_object = json.dumps(default, indent = 4)
  with open(f"{os.getcwd()}/guilds/{guild.id}.json", "w") as outfile:
    outfile.write(json_object)

client.run(config('TOKEN'))
