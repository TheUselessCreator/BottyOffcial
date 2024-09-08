import discord
from discord.ext import commands
from collections import defaultdict
import asyncio

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_count = defaultdict(int)  # Track messages per user per server
        self.anti_spam_enabled = defaultdict(bool)  # Tracks anti-spam status per server
        self.server_settings = defaultdict(lambda: {"spam_threshold": 5, "time_window": 10, "timeout_duration": 3600})  # Default settings per server

    # Enable anti-spam command with custom settings
    @commands.command(name="antispamenable")
    @commands.has_permissions(administrator=True)
    async def enable_antispam(self, ctx, spam_threshold: int, time_window: int, timeout_duration: int):
        self.anti_spam_enabled[ctx.guild.id] = True
        self.server_settings[ctx.guild.id] = {
            "spam_threshold": spam_threshold,
            "time_window": time_window,
            "timeout_duration": timeout_duration
        }
        await ctx.send(f"Anti-spam has been enabled in this server with the following settings:\n"
                       f"- Spam threshold: {spam_threshold} messages\n"
                       f"- Time window: {time_window} seconds\n"
                       f"- Timeout duration: {timeout_duration} seconds")

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
        settings = self.server_settings[guild_id]

        # Increment message count for the user
        self.message_count[(guild_id, user.id)] += 1

        # Check if user exceeded spam threshold
        if self.message_count[(guild_id, user.id)] >= settings["spam_threshold"]:
            await message.delete()
            await self.timeout_user(user, message.channel, settings["timeout_duration"])
            self.message_count[(guild_id, user.id)] = 0  # Reset their count after action

        # Reset message count after the time window
        await asyncio.sleep(settings["time_window"])
        self.message_count[(guild_id, user.id)] -= 1

    async def timeout_user(self, user, channel, timeout_duration):
        """ Timeout the user and notify them. """
        try:
            await user.timeout_for(discord.utils.utcnow(), timeout_duration)  # Timeout the user for the given duration
            await channel.send(f"{user.mention} has been timed out for spamming for {timeout_duration} seconds.")
        except discord.Forbidden:
            await channel.send(f"Failed to timeout {user.mention}. I might not have the right permissions.")
        except Exception as e:
            print(f"Error while trying to timeout user: {e}")

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
