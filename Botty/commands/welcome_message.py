import discord
from discord.ext import commands

class WelcomeMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open('./assets/welcome_message.txt', 'r') as file:
            welcome_message = file.read()

        try:
            await member.send(f"Welcome to {member.guild.name}!\n\n{welcome_message}")
        except discord.Forbidden:
            # If the user has DMs disabled
            print(f"Couldn't send a welcome message to {member.name}")

async def setup(bot):
    await bot.add_cog(WelcomeMessage(bot))
