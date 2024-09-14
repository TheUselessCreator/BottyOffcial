import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Discord user ID from the .env file
USER_ID = os.getenv("USER_ID")
if USER_ID is None:
    raise ValueError("USER_ID environment variable is not set.")
USER_ID = int(USER_ID)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

class GetServerInviteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="getserverinvite", description="Create an invite link for a specified server if the bot is a member.")
    async def getserverinvite(self, interaction: discord.Interaction, server_id: str):
        """Create an invite link for a specified server if the bot is a member."""
        if interaction.user.id != USER_ID:
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return

        # Acknowledge the interaction to prevent timeout
        await interaction.response.defer(thinking=True)

        try:
            # Convert server_id to an integer
            server_id = int(server_id)
        except ValueError:
            await interaction.followup.send("Invalid server ID. Please provide a valid server ID.", ephemeral=True)
            return

        # Debug: Check if server_id is valid
        print(f"Server ID received: {server_id}")

        # Try to get the guild (server)
        guild = self.bot.get_guild(server_id)
        if not guild:
            await interaction.followup.send("I am not in that server, please check the server ID.", ephemeral=True)
            return

        # Debug: Check if guild is found
        print(f"Guild found: {guild.name} (ID: {guild.id})")

        # Find a text channel where the bot can create an invite
        invite_channel = None
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).create_instant_invite:
                invite_channel = channel
                break

        if not invite_channel:
            await interaction.followup.send("I do not have permission to create an invite in any channel in that server.", ephemeral=True)
            return

        # Debug: Check if invite_channel is found
        print(f"Invite channel found: {invite_channel.name} in {guild.name}")

        try:
            # Create the invite link
            invite = await invite_channel.create_invite(max_age=3600)  # Invite link valid for 1 hour
            await interaction.followup.send(f"Here is your invite link for {guild.name}: {invite}")
        except Exception as e:
            # If an error occurs while creating the invite
            print(f"Error while creating invite: {e}")
            await interaction.followup.send("An error occurred while trying to create an invite. Please try again later.", ephemeral=True)

# Load the cog
async def setup(bot):
    await bot.add_cog(GetServerInviteCommand(bot))
