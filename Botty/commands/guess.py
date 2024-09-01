import discord
from discord.ext import commands
from discord import app_commands
import random

class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_number = None
        self.guesses = {}  # Store guesses by user

    @app_commands.command(name="guess", description="Guess the number the bot is thinking of.")
    async def guess(self, interaction: discord.Interaction, number: int):
        if self.current_number is None:
            self.current_number = random.randint(1, 10)  # Pick a random number between 1 and 10

        if number == self.current_number:
            await interaction.response.send_message(f"Congratulations {interaction.user.mention}! You guessed the number {self.current_number} correctly!")
            self.current_number = None  # Reset the number for the next round
        else:
            await interaction.response.send_message(f"Sorry {interaction.user.mention}, that's not the number I was thinking of. Try again!")
            # Optionally, you could give hints or allow multiple guesses

async def setup(bot):
    await bot.add_cog(Guess(bot))
