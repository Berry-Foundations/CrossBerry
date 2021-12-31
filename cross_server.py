# Cross Server

import discord
import os

async def broadcast(client, data:dict):
	channel_file = open("channels.csv", "r")
	channels = channel_file.read().split(',')
	channel_file.close()

	for fname in os.listdir('extras'):
		os.remove(f'extras/{fname}')

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
				elif data["type"] == "c-del":
					embed = discord.Embed(
						title = f"`{data['guild'].name}/#{data['channel'].name}` is no more connected to **Cross-Server Chat**!",
						color = 0x586aea
					)
					embed.set_thumbnail(url=data['guild'].icon_url)
					
					await c.send(embed=embed, username="CrossBerry", avatar_url=client.user.avatar_url)
				elif data["type"] == "c-rem":
					embed = discord.Embed(
						title = f"`{ctx.guild.name}/#{ctx.channel.name}` is no more connected to **Cross-Server Chat**!",
						color = 0x586aea
					)
					embed.set_thumbnail(url=ctx.guild.icon_url)
					
					await c.send(embed=embed, username="CrossBerry", avatar_url=ctx.guild.me.avatar_url)
				elif data["type"] == "v1":
					for fname in os.listdir('extras'):
						os.remove(f'extras/{fname}')

					attachments = data["ctx"].attachments
					files = []

					for attachment in attachments:
						await attachment.save(f"extras/{len(files)}__{attachment.filename}")
						files.append(discord.File(
								f"extras/{len(files)}__{attachment.filename}",
								filename = attachment.filename,
								spoiler = attachment.is_spoiler()
							))
					
					if data["content"].strip(" ") == "":
						await c.send("`<[[CONTENT:`**`MEDIA`**`]]>`", files=files, username=ctx.author.name, avatar_url=ctx.author.avatar_url)
					else:
						await c.send(data["content"], files=files, username=ctx.author.name, avatar_url=ctx.author.avatar_url)
			except Exception as e:
				print(e)
				fail_channels.append(int(channel))
			
	for failed_channel in fail_channels:
		channel_file = open('channels.csv', "w")
		channels = ",".join(channels).replace("," + str(int(failed_channel)) + ",", "")
		channel_file.write(f'{channels}')
		channel_file.close()

