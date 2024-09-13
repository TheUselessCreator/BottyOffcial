import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Discord user ID from the .env file
USER_ID = int(os.getenv("DISCORD_USER_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

class InviteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Define the /invite command
    @app_commands.command(name="invite", description="Create an invite link for a specified server if the bot is a member.")
    async def invite(self, interaction: discord.Interaction, server_id: int):
        """Create an invite link for a specified server if the bot is a member."""
        # Check if the user is allowed to use the command
        if interaction.user.id != USER_ID:
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return
        
        guild = self.bot.get_guild(server_id)
        if not guild:
            await interaction.response.send_message("I am not in that server, please check the server ID.", ephemeral=True)
            return

        invite_channel = discord.utils.get(guild.text_channels, permissions_for=guild.me.create_instant_invite)
        if not invite_channel:
            await interaction.response.send_message("I cannot create an invite link in this server. Please check my permissions.", ephemeral=True)
            return

        invite = await invite_channel.create_invite(max_age=3600)  # Invite link valid for 1 hour
        await interaction.response.send_message(f"Here is your invite link for {guild.name}: {invite}")

# Load the cog
async def setup(bot):
    await bot.add_cog(InviteCommand(bot))
