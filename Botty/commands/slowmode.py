import discord
from discord.ext import commands
from discord import app_commands

class SetSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='setslowmode', description='Set slowmode for a channel (Admin only) Choose between 0-21600 seconds.')
    async def setslowmode(self, interaction: discord.Interaction, channel: discord.TextChannel, amount: int):
        """Set slowmode in a channel. Only Admins can use this."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required Administrator permissions to use this command.", ephemeral=True)
            return
        
        # Check if the amount is within a reasonable range
        if amount < 0 or amount > 21600:
            await interaction.response.send_message("Slowmode amount must be between 0 and 21600 seconds (6 hours).", ephemeral=True)
            return

        try:
            await channel.edit(slowmode_delay=amount)
            if amount == 0:
                await interaction.response.send_message(f"Slowmode has been removed from {channel.mention}.")
            else:
                await interaction.response.send_message(f"Slowmode in {channel.mention} has been set to {amount} seconds.")
        except discord.Forbidden:
            await interaction.response.send_message(f"I don't have permission to change the slowmode for {channel.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(SetSlowmode(bot))
