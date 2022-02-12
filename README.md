# anti-league-discordbot
[![Docker Image CI](https://github.com/chriss-clem/anti-league-discordbot/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/chriss-clem/anti-league-discordbot/actions/workflows/docker-image.yml)
<br>
harrasses imbeciles for playing league of legends

***To invite the bot into your sever, paste the following link into your browser***
<code>https://discord.com/api/oauth2/authorize?client_id=937062519317598248&permissions=8&scope=bot</code>

When joining a server, the bot will create a channel called "channel-of-shame"
if not already created. In that channel, the bot will harrass anyone who
is playing league and has Activity Status enabled.
(By default, bot will @ the league player with a message insulting
them for playing league)


## Commands 
*You need server administrator to run commands*<br><br>

**$zeroTolerance** enable/disable - if enabled, anyone who plays league
will be permanently banned from the server. Disabled by default.<br><br>

**$games** add/remove "game name" - Edits the list of games that the bot
will yell at you for playing *$games view* will print a list of all of
the games.<br><br>

**$resetSettingsToDefault** - resets config file to its default state
(This resets all unique settings, such as custom games and messages)

## Hosting

*If you wish to host this bot by yourself, follow below instructions*<br>
First set TOKEN in the .env file<br>
Ensure that Presence Intent and Server Members Intent are enabled
in the bot page of your discord developer portal

Install the following packages using pip
<code>pip install python-decouple</code>
<code>pip install discord</code>
Then execute your main.py

