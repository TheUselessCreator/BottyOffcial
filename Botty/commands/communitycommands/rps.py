import discord
from discord.ext import commands
from discord import app_commands
import random

class RPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rps", description="Play Rock, Paper, Scissors against the bot.")
    @app_commands.describe(choice="Your choice: rock, paper, or scissors")
    async def rps(self, interaction: discord.Interaction, choice: str):
        # Define the valid choices
        choices = ["rock", "paper", "scissors"]

        # Validate the user choice
        if choice.lower() not in choices:
            await interaction.response.send_message("Invalid choice. Please choose 'rock', 'paper', or 'scissors'.", ephemeral=True)
            return

        # Bot's choice
        bot_choice = random.choice(choices)

        # Determine the result
        if choice.lower() == bot_choice:
            result = "It's a tie!"
        elif (choice.lower() == "rock" and bot_choice == "scissors") or \
             (choice.lower() == "paper" and bot_choice == "rock") or \
             (choice.lower() == "scissors" and bot_choice == "paper"):
            result = "You win!"
        else:
            result = "You lose!"

        # Send the result
        embed = discord.Embed(title="Rock, Paper, Scissors", color=discord.Color.blue())
        embed.add_field(name="Your choice", value=choice.capitalize(), inline=True)
        embed.add_field(name="Bot's choice", value=bot_choice.capitalize(), inline=True)
        embed.add_field(name="Result", value=result, inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(RPS(bot))
