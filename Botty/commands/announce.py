import discord
from discord.ext import commands
from discord import app_commands

class Announcement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='announce', description='Send an announcement to a specific channel')
    @app_commands.checks.has_permissions(administrator=True)
    async def announce(self, interaction: discord.Interaction, channel: discord.TextChannel, *, message: str):
        """Send a message to a specific channel for announcements."""
        try:
            # Send the announcement message to the specified channel
            await channel.send(message)
            await interaction.response.send_message(f"Announcement sent to {channel.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to send messages in that channel.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Announcement(bot))
