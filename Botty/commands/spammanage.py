import discord
from discord.ext import commands
from discord import app_commands
import time
import asyncio
import json

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anti_spam_enabled = {}  # Dictionary to keep track of anti-spam status per guild
        self.disabled_channels = {}  # Dictionary to keep track of disabled channels per guild
        self.message_timestamps = {}  # Dictionary to keep track of message timestamps per guild

    def get_guild_settings(self, guild_id):
        if guild_id not in self.anti_spam_enabled:
            self.anti_spam_enabled[guild_id] = True
            self.disabled_channels[guild_id] = []
            self.message_timestamps[guild_id] = {}
        return self.anti_spam_enabled[guild_id], self.disabled_channels[guild_id]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Check for spam messages and take action if needed."""
        if message.author.bot:
            return  # Ignore bot messages

        guild_id = message.guild.id
        is_enabled, disabled_channels = self.get_guild_settings(guild_id)

        if not is_enabled or message.channel.id in disabled_channels:
            return  # Skip anti-spam checks if disabled for this channel

        current_time = time.time()
        user_id = message.author.id

        # Initialize the dictionary for the guild if not already present
        if guild_id not in self.message_timestamps:
            self.message_timestamps[guild_id] = {}

        # Initialize the dictionary for the user if not already present
        if user_id not in self.message_timestamps[guild_id]:
            self.message_timestamps[guild_id][user_id] = []

        # Record the timestamp of the current message
        self.message_timestamps[guild_id][user_id].append(current_time)

        # Check if the user is sending messages too quickly
        timestamps = self.message_timestamps[guild_id][user_id]
        timestamps = [t for t in timestamps if current_time - t < 10]  # Check messages in the last 10 seconds

        if len(timestamps) > 5:  # More than 5 messages in 10 seconds
            # Delete the offending message
            await message.delete()

            # Send a warning message to the user
            warning_message = await message.channel.send(
                f"{message.author.mention}, you are sending messages too quickly. Please slow down."
            )

            # Optionally, delete the warning message after a few seconds
            await asyncio.sleep(10)
            await warning_message.delete()

            # Keep only the last 5 messages
            self.message_timestamps[guild_id][user_id] = timestamps[-5:]

    @app_commands.command(name="antispamdisable", description="Disable anti-spam protection in a specific channel")
    @app_commands.describe(channel="The channel where anti-spam should be disabled")
    async def antispamdisable(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Disable anti-spam protection in a specific channel."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        is_enabled, disabled_channels = self.get_guild_settings(guild_id)

        if channel.id not in disabled_channels:
            disabled_channels.append(channel.id)
            await interaction.response.send_message(f"Anti-spam protection has been disabled in {channel.mention}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Anti-spam protection is already disabled in {channel.mention}.", ephemeral=True)

    @app_commands.command(name="antispamenable", description="Enable anti-spam protection in the server")
    async def antispamenable(self, interaction: discord.Interaction):
        """Enable anti-spam protection in the server."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        self.anti_spam_enabled[guild_id] = True
        self.disabled_channels[guild_id] = []  # Reset the list of disabled channels
        await interaction.response.send_message("Anti-spam protection has been enabled in this server.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(AntiSpam(bot))
