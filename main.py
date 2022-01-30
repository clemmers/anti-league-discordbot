
import discord
intents = discord.Intents.all()
import requests
import json
from decouple import config

from discord.ext import commands

activity = discord.Activity(type=discord.ActivityType.watching, name="hentai")
client = commands.Bot(command_prefix = '$', activity=activity, status=discord.Status.online, intents=intents)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.command()
async def hello(ctx):
  await ctx.send("hello, i hate league")


@client.event
async def on_member_update(before, after):
    games = ["league of legends"]
    if after.activity and after.activity.name.lower() in games:
            channel = client.get_channel(config('CHANNEL_ID'))
            await channel.send(f"{after.mention} league :sick:")

#keep_alive()

client.run(config('TOKEN'))
