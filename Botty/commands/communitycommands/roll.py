import discord
from discord.ext import commands
from discord import app_commands
import random

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Roll a six-sided die.")
    async def roll(self, interaction: discord.Interaction):
        roll = random.randint(1, 6)
        await interaction.response.send_message(f"You rolled a {roll}!")

async def setup(bot):
    await bot.add_cog(Roll(bot))
