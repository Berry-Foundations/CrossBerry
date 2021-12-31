# Cross Server

import discord

async def broadcast(client, data:dict):
	channel_file = open("channels.csv", "r")
	channels = channel_file.read().split(',')
	channel_file.close()

	try:
		await data["ctx"].delete()
	except:
		pass

	fail_channels = []
	for channel in channels:
		if channel == "":
			pass
		else:
			try:
				ch = await client.fetch_channel(int(channel))
				awh = await ch.webhooks()
				if len(awh) > 0:
					c = awh[0]
				else:
					c = await ch.create_webhook(name="CrossBerry")

				ctx = data["ctx"]

				if data["type"] == "c-add":
					embed = discord.Embed(
						title = f"`{ctx.guild.name}/#{ctx.channel.name}` is now connected to **Cross-Server Chat**!",
						color = 0x586aea
					)
					embed.set_thumbnail(url=ctx.guild.icon_url)

					await c.send(embed=embed, username="CrossBerry", avatar_url=ctx.guild.me.avatar_url)
				elif data["type"] == "c-rem":
					embed = discord.Embed(
						title = f"`{ctx.guild.name}/#{ctx.channel.name}` is no more connected to **Cross-Server Chat**!",
						color = 0x586aea
					)
					embed.set_thumbnail(url=ctx.guild.icon_url)
					
					await c.send(embed=embed, username="CrossBerry", avatar_url=ctx.guild.me.avatar_url)
				elif data["type"] == "v1":
					await c.send(data["content"], username=ctx.author.name, avatar_url=ctx.author.avatar_url)
			except:
				fail_channels.append(int(channel))
			
	for failed_channel in fail_channels:
		channel_file = open('channels.csv', "w")
		channels = ",".join(channels).replace("," + str(int(failed_channel)) + ",", "")
		channel_file.write(f'{channels}')
		channel_file.close()

