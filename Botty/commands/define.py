import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class Define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="define", description="Get the definition of a word")
    async def define(self, interaction: discord.Interaction, word: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    definition = data[0]['meanings'][0]['definitions'][0]['definition']
                    await interaction.response.send_message(f"Definition of {word}: {definition}")
                else:
                    await interaction.response.send_message(f"Could not retrieve definition for {word}")

async def setup(bot):
    await bot.add_cog(Define(bot))
