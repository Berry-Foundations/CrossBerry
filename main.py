# CrossBerry

import discord
import os
import server
import crossbot

client = discord.Client()

@client.event
async def on_ready():
	print(f"{client.user} is ready!")
	activity = discord.Activity(type=discord.ActivityType.watching, name="Two Roads Meet!")
	await client.change_presence(activity=activity)
	server.super_run()

@client.event
async def on_message(ctx):
	await crossbot.message(ctx, client)

@client.event
async def on_guild_channel_delete(channel):
	await crossbot.delete_channel(channel, client)

@client.event
async def on_raw_reaction_add(payload):
	await crossbot.reactions(payload, client)

try:
	token = os.getenv('TOKEN')
	client.run(token)
except Exception as e:
	print(e)

