import discord
from discord.ext import commands
from discord import app_commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='kick', description='Kick a member from the server (Admin only).')
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        """Kicks a member from the server. Only Admins can use this."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        # Try to kick the member
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"{member.mention} has been kicked for: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message(f"I don't have permission to kick {member.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Kick(bot))
