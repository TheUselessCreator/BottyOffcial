import discord
from discord.ext import commands
from discord import app_commands

class Share(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='share', description='Share an image, video, or link.')
    async def share(self, interaction: discord.Interaction, url: str):
        if not url.startswith(('http://', 'https://')):
            await interaction.response.send_message("Please provide a valid URL starting with http:// or https://.")
            return

        await interaction.response.send_message(f"Shared media: {url}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Share(bot))
