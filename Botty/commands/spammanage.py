import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_settings = {}  # Dictionary to store spam settings per guild
        self.user_message_times = {}  # Dictionary to store user message timestamps per guild
        self.spam_check.start()  # Start the periodic spam check task

    def get_guild_settings(self, guild_id):
        if guild_id not in self.spam_settings:
            self.spam_settings[guild_id] = {'enabled': False, 'message_limit': 5, 'time_limit': 10}
            self.user_message_times[guild_id] = {}
        return self.spam_settings[guild_id]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Monitor messages to detect spam."""
        if message.author.bot:
            return  # Ignore bot messages

        guild_id = message.guild.id
        settings = self.get_guild_settings(guild_id)

        if not settings['enabled']:
            return

        user_id = message.author.id
        current_time = message.created_at.timestamp()

        if user_id not in self.user_message_times[guild_id]:
            self.user_message_times[guild_id][user_id] = []

        # Add the current message timestamp
        self.user_message_times[guild_id][user_id].append(current_time)

        # Remove timestamps outside the time limit window
        self.user_message_times[guild_id][user_id] = [t for t in self.user_message_times[guild_id][user_id] if current_time - t < settings['time_limit']]

        if len(self.user_message_times[guild_id][user_id]) > settings['message_limit']:
            # Detect spam and take action
            await self.handle_spam(message.author, message.guild)
            self.user_message_times[guild_id][user_id] = []  # Clear the timestamps after action

    async def handle_spam(self, user, guild):
        """Handle a spam detection by timing out the user."""
        try:
            # Apply a 1-hour timeout
            timeout_duration = discord.utils.utcnow() + discord.utils.timedelta(hours=1)
            await user.timeout(timeout_duration, reason="Detected spamming.")
            
            # Notify the user about the timeout
            try:
                await user.send("You have been timed out for 1 hour due to spamming.")
            except discord.Forbidden:
                pass  # If we can't DM the user, that's okay

            # Optionally send a message in the guild
            await guild.system_channel.send(f"{user.mention} has been timed out for spamming.")
        except Exception as e:
            print(f"Failed to handle spam: {e}")

    @app_commands.command(name="antispamenable", description="Enable anti-spam protection")
    @app_commands.describe(message_limit="The number of messages to trigger spam detection", time_limit="The time window in seconds")
    async def antispamenable(self, interaction: discord.Interaction, message_limit: int, time_limit: int):
        """Enable anti-spam protection with a message limit and time window."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        self.spam_settings[guild_id] = {
            'enabled': True,
            'message_limit': message_limit,
            'time_limit': time_limit
        }

        await interaction.response.send_message(f"Anti-spam protection enabled! Trigger limit: {message_limit} messages in {time_limit} seconds.", ephemeral=True)

    @app_commands.command(name="antispamdisable", description="Disable anti-spam protection")
    async def antispamdisable(self, interaction: discord.Interaction):
        """Disable anti-spam protection."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        self.spam_settings[guild_id]['enabled'] = False
        await interaction.response.send_message("Anti-spam protection has been disabled.", ephemeral=True)

    @tasks.loop(minutes=1)
    async def spam_check(self):
        """Periodically clean up old messages."""
        for guild_id, user_times in self.user_message_times.items():
            current_time = discord.utils.utcnow().timestamp()
            for user_id, timestamps in list(user_times.items()):
                self.user_message_times[guild_id][user_id] = [t for t in timestamps if current_time - t < self.get_guild_settings(guild_id)['time_limit']]
                if not self.user_message_times[guild_id][user_id]:
                    del self.user_message_times[guild_id][user_id]

async def setup(bot: commands.Bot):
    await bot.add_cog(AntiSpam(bot))

