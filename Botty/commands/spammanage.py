import discord
from discord.ext import commands
from discord import app_commands
from collections import defaultdict
import asyncio

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_count = defaultdict(int)  # Track messages per user per server
        self.spam_threshold = 5  # Default max messages allowed in the time window
        self.time_window = 10  # Default time window in seconds for spam detection
        self.timeout_duration = 3600  # Timeout duration in seconds (1 hour)
        self.anti_spam_enabled = defaultdict(bool)  # Tracks anti-spam status per server

    @app_commands.command(name='antispamenable', description='Enable anti-spam for this server')
    @commands.has_permissions(administrator=True)
    async def antispam_enable(self, interaction: discord.Interaction):
        """Enable anti-spam for the server."""
        self.anti_spam_enabled[interaction.guild.id] = True
        await interaction.response.send_message("Anti-spam has been enabled for this server.", ephemeral=True)

    @app_commands.command(name='antispamdisable', description='Disable anti-spam for this server')
    @commands.has_permissions(administrator=True)
    async def antispam_disable(self, interaction: discord.Interaction):
        """Disable anti-spam for the server."""
        self.anti_spam_enabled[interaction.guild.id] = False
        await interaction.response.send_message("Anti-spam has been disabled for this server.", ephemeral=True)

    @app_commands.command(name='setspammessages', description='Set the maximum number of messages allowed in the time window')
    @commands.has_permissions(administrator=True)
    @app_commands.describe(threshold="Maximum number of messages allowed")
    async def set_spam_messages(self, interaction: discord.Interaction, threshold: int):
        """Set the maximum number of messages allowed in the time window."""
        if threshold <= 0:
            await interaction.response.send_message("Threshold must be a positive number.", ephemeral=True)
            return
        
        self.spam_threshold = threshold
        await interaction.response.send_message(f"Spam threshold set to {threshold} messages.", ephemeral=True)

    @app_commands.command(name='setspamtime', description='Set the time window for spam detection')
    @commands.has_permissions(administrator=True)
    @app_commands.describe(window="Time window in seconds")
    async def set_spam_time(self, interaction: discord.Interaction, window: int):
        """Set the time window in seconds for spam detection."""
        if window <= 0:
            await interaction.response.send_message("Time window must be a positive number.", ephemeral=True)
            return
        
        self.time_window = window
        await interaction.response.send_message(f"Time window set to {window} seconds.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Detect and handle spam messages."""
        if message.author.bot:
            return

        guild_id = message.guild.id
        if guild_id not in self.anti_spam_enabled or not self.anti_spam_enabled[guild_id]:
            return

        user_id = message.author.id
        self.message_count[user_id] += 1

        # Check if the user has exceeded the spam threshold
        if self.message_count[user_id] > self.spam_threshold:
            try:
                await message.author.timeout(reason="Exceeded spam threshold", duration=self.timeout_duration)
                await message.delete()
                await message.channel.send(f"{message.author.mention} has been timed out for spamming.")
            except discord.Forbidden:
                print(f"Failed to timeout {message.author.name} due to missing permissions.")
            except Exception as e:
                print(f"Error while processing anti-spam: {e}")

        # Reset the count after the time window
        await asyncio.sleep(self.time_window)
        self.message_count[user_id] -= 1

async def setup(bot: commands.Bot):
    await bot.add_cog(AntiSpam(bot))
