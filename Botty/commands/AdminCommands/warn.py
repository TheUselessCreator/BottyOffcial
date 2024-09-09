import discord
from discord.ext import commands
from discord import app_commands
from collections import defaultdict
from datetime import timedelta

class WarnCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Dictionary to store warnings. Key: member ID, Value: warning count.
        self.warns = defaultdict(int)

    @app_commands.command(name="warn", description="Warn a user. After 5 warnings, they receive a 1-day timeout.")
    @app_commands.checks.has_permissions(administrator=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        """Warn a user and apply a timeout after 5 warnings."""
        # Increment the user's warning count
        self.warns[member.id] += 1
        warn_count = self.warns[member.id]

        # Notify the moderator and the warned user
        await interaction.response.send_message(f"{member.mention} has been warned for: {reason}. This is warning {warn_count}/5.")
        await member.send(f"You have been warned in {interaction.guild.name} for: {reason}. Warning count: {warn_count}/5.")

        # Check if the user has reached 5 warnings
        if warn_count >= 5:
            # Apply a 1-day timeout (86400 seconds)
            duration = timedelta(days=1)
            await member.timeout_for(duration, reason="Reached 5 warnings.")
            await interaction.channel.send(f"{member.mention} has been timed out for 1 day due to receiving 5 warnings.")
            self.warns[member.id] = 0  # Reset the warning count after timeout

    @warn.error
    async def warn_error(self, interaction: discord.Interaction, error):
        """Error handler for the warn command."""
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message("An error occurred while trying to warn the user.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(WarnCog(bot))
