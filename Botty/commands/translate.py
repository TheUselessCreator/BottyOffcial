import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="translate", description="Translate text to another language")
    async def translate(self, interaction: discord.Interaction, text: str, target_language: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_language}') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    translated_text = data['responseData']['translatedText']
                    await interaction.response.send_message(f"Translated to {target_language}: {translated_text}")
                else:
                    await interaction.response.send_message("Failed to translate")

async def setup(bot):
    await bot.add_cog(Translate(bot))
