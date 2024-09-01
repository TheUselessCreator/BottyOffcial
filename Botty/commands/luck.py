import discord
from discord.ext import commands
from discord import app_commands
import random

class LuckCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='luck', description='Pick a lucky number between 1 and 100.')
    async def luck(self, interaction: discord.Interaction):
        # Generate a random number between 1 and 100
        number = random.randint(1, 100)
        
        # Define messages based on the number
        if number <= 25:
            message = "Better luck next time!"
        elif number <= 50:
            message = "Not bad, but you can do better!"
        elif number <= 75:
            message = "Pretty good! You're getting there!"
        else:
            message = "Excellent! You're on fire!"

        # Create an embed
        embed = discord.Embed(
            title="Your Luck!",
            description=f"You rolled a **{number}**. {message}",
            color=discord.Color.blue()
        )

        # Send the embed
        await interaction.response.send_message(embed=embed)

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(LuckCog(bot))
