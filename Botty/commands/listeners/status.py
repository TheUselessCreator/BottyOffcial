import discord
from discord.ext import commands
import os

class StatusCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_status(self, ctx):
        """Sets the bot's status from the status.txt file"""
        try:
            with open('assets/status.txt', 'r') as file:
                status_text = file.read().strip()
                if not status_text:
                    status_text = "Default status"  # Fallback status text
                await self.bot.change_presence(activity=discord.Game(name=status_text), status=discord.Status.online)
                await ctx.send(f"Status set to: {status_text}")
        except Exception as e:
            await ctx.send(f"Failed to set status: {e}")

async def setup(bot):
    await bot.add_cog(StatusCommand(bot))
