import discord
from discord.ext import commands
from discord import app_commands

class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='echo', description='Make the bot repeat your message.')
    @app_commands.describe(message='The message you want the bot to repeat.')
    async def echo(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Echo(bot))
