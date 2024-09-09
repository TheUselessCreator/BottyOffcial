import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Load the authorized user ID from the .env file
load_dotenv()
AUTHORIZED_USER_ID = int(os.getenv('USER_ID'))

class LeaveServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ls", description="Make the bot leave a server (Admin only)")
    async def leave_server(self, interaction: discord.Interaction, server_id: str):
        """Allow an authorized user to make the bot leave a specific server by ID."""
        if interaction.user.id != AUTHORIZED_USER_ID:
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return

        try:
            # Find the server by its ID
            guild = self.bot.get_guild(int(server_id))

            if guild is None:
                await interaction.response.send_message(f"The bot is not in a server with the ID {server_id}.", ephemeral=True)
                return

            # Leave the server
            await guild.leave()
            await interaction.response.send_message(f"The bot has left the server: {guild.name} (ID: {guild.id}).", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(LeaveServer(bot))
