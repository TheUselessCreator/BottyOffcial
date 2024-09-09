import discord
from discord.ext import commands
from discord import app_commands

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='mute', description='Mute a member in the server (Admin only).')
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        """Mute a member in the server. Only Admins can use this."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required Administrator permissions to use this command.", ephemeral=True)
            return

        try:
            mute_role = discord.utils.get(interaction.guild.roles, name="Muted")  # Check for a 'Muted' role
            if not mute_role:
                await interaction.response.send_message("Muted role not found. Please create one named 'Muted'.", ephemeral=True)
                return

            await member.add_roles(mute_role, reason=reason)
            await interaction.response.send_message(f"{member.mention} has been muted. Reason: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message(f"I don't have permission to mute {member.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Mute(bot))
