import discord
from discord.ext import commands
from discord import app_commands
import datetime
import pytz

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="time", description="Get the current time for a timezone")
    async def time(self, interaction: discord.Interaction, timezone: str):
        try:
            tz = pytz.timezone(timezone)
            now = datetime.datetime.now(tz)
            await interaction.response.send_message(f"The current time in {timezone} is {now.strftime('%Y-%m-%d %H:%M:%S')}")
        except pytz.UnknownTimeZoneError:
            await interaction.response.send_message("Unknown timezone. Please provide a valid timezone.")

async def setup(bot):
    await bot.add_cog(Time(bot))
