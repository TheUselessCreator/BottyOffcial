import discord
from discord.ext import commands
from discord import app_commands
import time

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anti_spam_enabled = True  # Default state is enabled
        self.disabled_channels = []  # List of channel IDs where anti-spam is disabled
        self.message_timestamps = {}  # Dictionary to keep track of message timestamps

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Check for spam messages and take action if needed."""
        if message.author.bot:
            return  # Ignore bot messages
        
        if not self.anti_spam_enabled or message.channel.id in self.disabled_channels:
            return  # Skip anti-spam checks if disabled for this channel

        current_time = time.time()
        channel_id = message.channel.id
        user_id = message.author.id

        # Initialize the dictionary for the channel if not already present
        if channel_id not in self.message_timestamps:
            self.message_timestamps[channel_id] = {}

        # Initialize the dictionary for the user if not already present
        if user_id not in self.message_timestamps[channel_id]:
            self.message_timestamps[channel_id][user_id] = []

        # Record the timestamp of the current message
        self.message_timestamps[channel_id][user_id].append(current_time)

        # Check if the user is sending messages too quickly
        timestamps = self.message_timestamps[channel_id][user_id]
        timestamps = [t for t in timestamps if current_time - t < 10]  # Check messages in the last 10 seconds

        if len(timestamps) > 5:  # More than 5 messages in 10 seconds
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you are sending messages too quickly. Please slow down.")
            self.message_timestamps[channel_id][user_id] = timestamps[-5:]  # Keep only the last 5 messages

    @app_commands.command(name="antispamdisable", description="Disable anti-spam protection in a specific channel")
    @app_commands.describe(channel="The channel where anti-spam should be disabled")
    async def antispamdisable(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Disable anti-spam protection in a specific channel."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        if channel.id not in self.disabled_channels:
            self.disabled_channels.append(channel.id)
            await interaction.response.send_message(f"Anti-spam protection has been disabled in {channel.mention}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Anti-spam protection is already disabled in {channel.mention}.", ephemeral=True)

    @app_commands.command(name="antispamenable", description="Enable anti-spam protection globally")
    async def antispamenable(self, interaction: discord.Interaction):
        """Enable anti-spam protection globally for all channels."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        self.anti_spam_enabled = True
        self.disabled_channels = []  # Reset the list of disabled channels
        await interaction.response.send_message("Anti-spam protection has been enabled globally.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(AntiSpam(bot))

