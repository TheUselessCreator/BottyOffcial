import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class Fact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fact", description="Get a random fun fact")
    async def fact(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://uselessfacts.jsph.pl/random.json?language=en') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await interaction.response.send_message(f"Did you know? {data['text']}")
                else:
                    await interaction.response.send_message("Failed to retrieve fact")

async def setup(bot):
    await bot.add_cog(Fact(bot))
