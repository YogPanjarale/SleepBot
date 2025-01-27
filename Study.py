import discord
import random
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command
import Util
from datetime import datetime
from discord.ext import commands
import dpytools.checks

class Study(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.FocusChannelID = 818131313810079744
		self.guildID = 740589508365385839
		self.StudyBuddiesRoleID = 770667627047682058
	
	async def StudyVCJoinMessage(self, member, NoOfRoles):
		StudyVCEmbed = discord.Embed(title = "It's Focus Time, {}!".format(member.name),
								description = "To help you focus, you have been muted in all channels except <#770940461337804810> and the music channels.",
								colour = random.randint(0, 0xffffff))
		StudyVCEmbed.add_field(name="How do I get unmuted?", value="You will be unmuted automatically when you leave the Study VCs.", inline = False)
		if random.randint(0, 200-NoOfRoles) == 0:
			StudyVCEmbed.set_image(url='https://res.cloudinary.com/zeusabhijeet/image/upload/v1615206699/SleepBot/Study%20Commands/Study_you_b_words.png')
		else:
			StudyVCEmbed.set_image(url='https://res.cloudinary.com/zeusabhijeet/image/upload/v1615211844/SleepBot/Study%20Commands/focus_you_b_words.gif')
		return StudyVCEmbed
	
	@commands.command(name='study_buddies', aliases = ['study-buddy', 'studybuddy', 'sb'], help = "Ping Study Buddies Role")
	@commands.cooldown(1, 7200, commands.BucketType.default)
	@dpytools.checks.in_these_channels(770940461337804810)
	async def study_buddies(self, ctx, *, reason = None):
		StudyBuddyRole = self.client.get_guild(Util.GUILD_ID).get_role(self.StudyBuddiesRoleID)
		if reason == None:
			await ctx.send("Hey {}!\n{} wants to study with y'all.".format(StudyBuddyRole.mention, ctx.message.author.mention))
		else:
			await ctx.send("Hey {}!\n{} wants to study with y'all. Here's the reason they pinged: **{}**".format(StudyBuddyRole.mention, ctx.message.author.mention, reason))
	@study_buddies.error
	async def sberror(self, ctx, error):
		await Util.ErrorHandler(ctx, error)	
	
	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if before.channel is None and after.channel is not None:
			guild = self.client.get_guild(self.guildID)
			NoOfRoles = len(guild.get_member(member.id).roles)
			if after.channel.id == 770670934565715998 and not member.bot:
				await self.client.get_channel(self.FocusChannelID).send("<@!{}>".format(member.id))
				await self.client.get_channel(self.FocusChannelID).send(embed = await self.StudyVCJoinMessage(member, NoOfRoles))
			elif after.channel.id == 818011398231687178 and not member.bot:
				await self.client.get_channel(self.FocusChannelID).send("<@!{}>".format(member.id))
				await self.client.get_channel(self.FocusChannelID).send(embed = await self.StudyVCJoinMessage(member, NoOfRoles))
		else:
			return

def setup(client):
	client.add_cog(Study(client))
