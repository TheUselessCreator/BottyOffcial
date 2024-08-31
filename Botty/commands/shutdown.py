import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class ShutdownCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.password = os.getenv('SHUTDOWN_PASSWORD')  # Get the password from environment variables

    @app_commands.command(name='shutdown', description='Shutdown the bot with a password')
    async def shutdown(self, interaction: discord.Interaction, password: str):
        if password == self.password:
            await interaction.response.send_message("Correct password! Shutting down the bot...")
            await self.bot.close()  # Shut down the bot
        else:
            await interaction.response.send_message("Incorrect password! You do not have permission to shut down the bot.")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(ShutdownCog(bot))
