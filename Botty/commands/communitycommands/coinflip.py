import discord
from discord.ext import commands
from discord import app_commands
import random

class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='coinflip', description='Flip a coin to get heads or tails.')
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(['Heads', 'Tails'])
        await interaction.response.send_message(f"The coin landed on: **{result}**")

async def setup(bot: commands.Bot):
    await bot.add_cog(CoinFlip(bot))
