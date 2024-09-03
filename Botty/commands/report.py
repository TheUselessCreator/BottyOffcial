import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import datetime
import os

# Load the Webhook URL from environment variables
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report", description="Report an issue or problem")
    async def report(self, interaction: discord.Interaction, reason: str, info: str):
        """Handle the /report command."""
        report_id = interaction.id
        user = interaction.user
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        embed = discord.Embed(
            title=f"Report #{report_id}",
            color=discord.Color.red(),
            timestamp=interaction.created_at
        )
        embed.add_field(name="Time", value=current_time, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Info", value=info, inline=False)
        embed.add_field(name="Reported by", value=f"{user} ({user.id})", inline=False)

        async with aiohttp.ClientSession() as session:
            webhook_data = {"embeds": [embed.to_dict()]}
            async with session.post(WEBHOOK_URL, json=webhook_data) as response:
                if response.status == 204:
                    await interaction.response.send_message("Report submitted successfully.", ephemeral=True)
                else:
                    await interaction.response.send_message("Failed to submit report.", ephemeral=True)
                    print(f"Failed to send report: {response.status} - {await response.text()}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Report(bot))
