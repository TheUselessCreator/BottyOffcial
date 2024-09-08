import discord
from discord.ext import commands
from collections import defaultdict
import asyncio

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_count = defaultdict(int)  # Track messages per user per server
        self.spam_threshold = 5  # Max messages allowed in the time window
        self.time_window = 10  # Time window in seconds for spam detection
        self.timeout_duration = 3600  # Timeout duration in seconds (1 hour)
        self.anti_spam_enabled = defaultdict(bool)  # Tracks anti-spam status per server

    # Enable anti-spam command
    @commands.command(name="antispamenable")
    @commands.has_permissions(administrator=True)
    async def enable_antispam(self, ctx):
        self.anti_spam_enabled[ctx.guild.id] = True
        await ctx.send("Anti-spam has been enabled in this server.")

    # Disable anti-spam command
    @commands.command(name="antispamdisable")
    @commands.has_permissions(administrator=True)
    async def disable_antispam(self, ctx):
        self.anti_spam_enabled[ctx.guild.id] = False
        await ctx.send("Anti-spam has been disabled in this server.")

    # Listener for message events
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return  # Ignore DMs

        if message.author.bot:
            return  # Ignore bot messages

        if not self.anti_spam_enabled[message.guild.id]:
            return  # Ignore if anti-spam is disabled

        user = message.author
        guild_id = message.guild.id

        # Increment message count for the user
        self.message_count[(guild_id, user.id)] += 1

        # Wait for the time window before resetting message count
        await asyncio.sleep(self.time_window)
        self.message_count[(guild_id, user.id)] -= 1

        # Check if user exceeded spam threshold
        if self.message_count[(guild_id, user.id)] >= self.spam_threshold:
            await message.delete()
            await self.timeout_user(user, message.channel)
            self.message_count[(guild_id, user.id)] = 0  # Reset their count after action

    async def timeout_user(self, user, channel):
        """ Timeout the user and notify them. """
        try:
            await user.timeout_for(discord.utils.utcnow(), self.timeout_duration)  # Timeout the user for 1 hour
            await channel.send(f"{user.mention} has been timed out for spamming.")
        except discord.Forbidden:
            await channel.send(f"Failed to timeout {user.mention}. I might not have the right permissions.")
        except Exception as e:
            print(f"Error while trying to timeout user: {e}")

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
