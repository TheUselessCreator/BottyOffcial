import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio

class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="remind", description="Set a reminder")
    async def remind(self, interaction: discord.Interaction, time_in_seconds: int, message: str):
        await interaction.response.send_message(f"Reminder set for {time_in_seconds} seconds: {message}")
        await asyncio.sleep(time_in_seconds)
        await interaction.followup.send(f"Reminder: {message}")

async def setup(bot):
    await bot.add_cog(Remind(bot))
