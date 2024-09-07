import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the user ID and shutdown password from environment variables
USER_ID = int(os.getenv('USER_ID'))
SHUTDOWN_PASSWORD = os.getenv('SHUTDOWN_PASSWORD')

class ShutdownCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.password = SHUTDOWN_PASSWORD  # Get the shutdown password from the environment variables

    @app_commands.command(name='shutdown', description='Shutdown the bot with a password (Owner only)')
    async def shutdown(self, interaction: discord.Interaction, password: str):
        # Check if the user has the correct USER_ID
        if interaction.user.id != USER_ID:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        # Check if the password is correct
        if password == self.password:
            await interaction.response.send_message("Correct password! Shutting down the bot...", ephemeral=True)
            await self.bot.close()  # Shut down the bot
        else:
            await interaction.response.send_message("Incorrect password! You do not have permission to shut down the bot.", ephemeral=True)

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(ShutdownCog(bot))
