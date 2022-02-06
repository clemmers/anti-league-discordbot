import discord
intents = discord.Intents.all()
from decouple import config
from discord.ext import commands

activity = discord.Activity(type=discord.ActivityType.playing, name="LITERALLY ANY OTHER GAME")
client = commands.Bot(command_prefix = '$', activity=activity, status=discord.Status.online, intents=intents)
global channel
global guild
tolerance = True

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  print("Branch version " + discord.__version__)
  global guild
  guild = client.get_guild(int(config('GUILD_ID')))
  await createChannel(guild)

async def createChannel(guild):
  global channel
  for i in guild.channels:
    if(i.name == 'channel-of-shame'):
      channel = i
      print("Channel of Shame is already created, but got its channel ID!")
      break
  else:
    channel = await guild.create_text_channel('channel-of-shame')
    await channel.set_permissions(guild.default_role, send_messages=False)
  
@client.command()
async def zeroTolerance(ctx, boo=" "):
  global tolerance
  if not ctx.message.author.guild_permissions.administrator:
    await ctx.send("no")
    return
  if boo.lower() == 'enable' and tolerance == True:
    await ctx.send("Zero Tolerance initiated. Anyone who plays league in this server will be **permanently** banned!")
    tolerance = False
    
  elif boo.lower() == 'enable':
    await ctx.send("You already have Zero Tolerance enabled!")
    
  elif boo.lower() == 'disable' and tolerance == False:
    await ctx.send("Zero Tolerance disabled!")
    tolerance = True
    
  elif boo.lower() == 'disable':
    await ctx.send("Zero Tolerance was not enabled so it was not disabled.")
    
  elif boo.lower() == " ":
    await ctx.send("Zero Tolerance is " + str(tolerance).lower() + ". If you wish to change that, please specify whether you want to 'enable' or 'disable' zero tolerance")
    
  else:
    await ctx.send("Not a valid input. Please say 'enable' for zero tolerance, or 'disable' if you want to be merciful")

@client.event
async def on_member_update(before, after):
    global guild
    games = ["league of legends"]
    if after.activity and after.activity.name.lower() in games and after in guild.members:
      if before.activity is None:
        await punish(after)
      elif not before.activity.name.lower() in games:
        await punish(after)

async def punish(after):
  global channel
  global tolerance
  if tolerance:
    await channel.send(f"{after.mention} is playing league :sick:")
  else:
    await channel.send(f"{after.mention} plays league!!!! BANNED :sick::sick::sick:")
    await after.ban(reason = "ZERO TOLERANCE FOR LEAGUE PLAYERS")


client.run(config('TOKEN'))
