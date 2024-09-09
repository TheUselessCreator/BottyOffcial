import discord
from discord.ext import commands
from discord import app_commands
import os

class Website(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Fetch the website link from environment variables
        self.website_link = os.getenv("WEBSITE_LINK", "https://sites.google.com/view/botty-help/home")

    @app_commands.command(name='website', description='Get the link to the bot\'s website.')
    async def website(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Website",
            description=f"Visit our official website: [Click Here]({self.website_link})",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Website(bot))
