import discord
from discord.ext import commands
from discord import app_commands
import requests

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="meme", description="Get a random meme from a public API.")
    async def meme(self, interaction: discord.Interaction):
        # Public Meme API URL
        url = "https://meme-api.com/gimme"

        # Fetch meme data from the public API
        response = requests.get(url)

        if response.status_code != 200:
            await interaction.response.send_message("Failed to retrieve meme.", ephemeral=True)
            return

        # Parse the JSON response
        json_response = response.json()

        # Get the meme URL and title
        meme_url = json_response.get('url')
        meme_title = json_response.get('title', 'Random Meme')

        if not meme_url:
            await interaction.response.send_message("No meme found.", ephemeral=True)
            return

        # Send the meme as an embed
        embed = discord.Embed(title=meme_title, color=discord.Color.random())
        embed.set_image(url=meme_url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Meme(bot))
