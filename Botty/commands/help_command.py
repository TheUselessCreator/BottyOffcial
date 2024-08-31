import discord
from discord.ext import commands
from discord import app_commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Get help with the bot's commands")
    async def help_command(self, interaction: discord.Interaction):
        with open('./assets/help_description.txt', 'r') as file:
            help_message = file.read()
        await interaction.response.send_message(embed=discord.Embed(
            title="Bot Help",
            description=help_message,
            color=discord.Color.blue()
        ))

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
