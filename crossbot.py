# Cross-Server Bot

import discord
import os
import cross_server

async def commands(ctx, client):
	prefix_file = open("internals/prefixes.csv", 'r')
	prefixes = prefix_file.read().split(',')
	prefix_file.close()
	m = ctx.content.split(' ')

	if m[0].lower() in prefixes:
		if len(m) > 1:
			c = m[1].lower()

			if c == "help":
				filename = "main"
				if len(m) > 2:
					filename = (" ".join(m[2:])).lower()
					if os.path.isfile(f"internals/{filename.lower()}.md"):
						pass
					else:
						filename = "main"
				
				file = open(f"internals/{filename.lower()}.md", 'r')
				help_content = file.read()
				file.close()

				embed = discord.Embed(
					title = "CrossBerry",
					color = 0x586aea,
					description = "Cross Server Messenger"
				)
				embed.add_field(
					name = f"Help - `{filename.lower()}`",
					value = help_content
				)
				embed.set_thumbnail(url=ctx.guild.me.avatar_url)
				embed.set_footer(
					text = "Services under Berry Foundations - Attachment Studios",
					icon_url = "https://images-ext-1.discordapp.net/external/x_dF_ppBthHmRPQi75iuRXLMfK0wuAW2sBLTdtNlXAc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/894098855220617216/d9b9a3b48a054b9847401bb9178ed438.webp"
				)

				____m = await ctx.channel.send(embed=embed)

				try:
					await ____m.add_reaction('❌')
				except:
					pass

				try:
					await ctx.delete()
				except:
					pass
				
				return "COMMAND"
			elif c == "add":
				await add_channel(ctx, client)
				
				try:
					await ctx.delete()
				except:
					pass
				
				return "COMMAND"
			elif c == "remove":
				await remove_channel(ctx, client)

				try:
					await ctx.delete()
				except:
					pass
				
				return "COMMAND"

	return None

async def message(ctx, client):
	if ctx.author.bot:
		return
	
	run = await commands(ctx, client)
	if run == None:
		pass
	else:
		return

	channel_file = open('channels.csv', "r")
	channel_list = str(channel_file.read()).split(',')
	channel_file.close()

	if str(ctx.channel.id) in channel_list:
		await cross_server.broadcast(
			client,
			{
				"type" : "v1",
				"content" : ctx.content,
				"ctx" : ctx
			}
		)

async def add_channel(ctx, client):
	channel_file = open('channels.csv', "r")
	channel_list = str(channel_file.read()).split(',')
	channel_file.close()

	embed = discord.Embed(
		title = "CrossBerry",
		color = 0x586aea,
		description = "Cross Server Messenger"
	)
	embed.set_thumbnail(url=ctx.guild.me.avatar_url)
	embed.set_footer(
		text = "Services under Berry Foundations - Attachment Studios",
		icon_url = "https://images-ext-1.discordapp.net/external/x_dF_ppBthHmRPQi75iuRXLMfK0wuAW2sBLTdtNlXAc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/894098855220617216/d9b9a3b48a054b9847401bb9178ed438.webp"
	)
	
	if str(ctx.channel.id) in channel_list:
		embed.add_field(
			name = "Error",
			value = "This channel is already a `cross-server` channel. It can not be added again to the list."
		)
	else:
		channel_file = open('channels.csv', "a")
		channel_file.write(f',{str(ctx.channel.id)},')
		channel_file.close()

		embed.add_field(
			name = "`Cross-Server` Activated",
			value = "This channel is now a `cross-server` channel."
		)

		await cross_server.broadcast(
			client,
			{
				"type" : "c-add",
				"content" : "A new channel added!",
				"ctx" : ctx
			}
		)
	
	____m = await ctx.channel.send(embed=embed)
	
	try:
		await ____m.add_reaction('❌')
	except:
		pass

async def remove_channel(ctx, client):
	channel_file = open('channels.csv', "r")
	channel_list = str(channel_file.read()).split(',')
	channel_file.close()

	embed = discord.Embed(
		title = "CrossBerry",
		color = 0x586aea,
		description = "Cross Server Messenger"
	)
	embed.set_thumbnail(url=ctx.guild.me.avatar_url)
	embed.set_footer(
		text = "Services under Berry Foundations - Attachment Studios",
		icon_url = "https://images-ext-1.discordapp.net/external/x_dF_ppBthHmRPQi75iuRXLMfK0wuAW2sBLTdtNlXAc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/894098855220617216/d9b9a3b48a054b9847401bb9178ed438.webp"
	)

	if str(ctx.channel.id) in channel_list:
		channel_file = open('channels.csv', "w")
		channel_file.write(f'{",".join(channel_list).replace("," + str(ctx.channel.id) + ",", "")}')
		channel_file.close()

		embed.add_field(
			name = "`Cross-Server` Disabled",
			value = "This channel is no more a `cross-server` channel."
		)

		await cross_server.broadcast(
			client,
			{
				"type" : "c-rem",
				"content" : "A channel removed!",
				"ctx" : ctx
			}
		)
	else:
		embed.add_field(
			name = "Error",
			value = "This channel is already not a `cross-server` channel. It can not be removed from the list."
		)

	____m = await ctx.channel.send(embed=embed)

	try:
		await ____m.add_reaction('❌')
	except:
		pass

async def delete_channel(channel, client):
	channel_file = open('channels.csv', "r")
	channel_list = str(channel_file.read()).split(',')
	channel_file.close()

	if str(channel.id) in channel_list:
		channel_file = open('channels.csv', "w")
		channel_file.write(f'{",".join(channel_list).replace("," + str(channel.id) + ",", "")}')
		channel_file.close()

		await cross_server.broadcast(
			client,
			{
				"type" : "c-del",
				"content" : "A channel removed!",
				"ctx" : None,
				"channel" : channel,
				"guild" : channel.guild
			}
		)
	else:
		pass

async def reactions(payload, client):
	try:
		if payload.member.bot:
			return
		
		if payload.emoji.name == "❌":
			c = await client.fetch_channel(payload.channel_id)
			m = await c.fetch_message(payload.message_id)

			if m.author == m.guild.me:
				await m.delete()
	except Exception as e:
		print(e)

