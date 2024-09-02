import discord
from discord.ext import commands
from discord import app_commands

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='unmute', description='Unmute a member in the server (Admin only).')
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        """Unmute a member in the server. Only Admins can use this."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required Administrator permissions to use this command.", ephemeral=True)
            return

        try:
            mute_role = discord.utils.get(interaction.guild.roles, name="Muted")  # Check for the 'Muted' role
            if not mute_role:
                await interaction.response.send_message("Muted role not found. Please create one named 'Muted'.", ephemeral=True)
                return

            if mute_role in member.roles:
                await member.remove_roles(mute_role)
                await interaction.response.send_message(f"{member.mention} has been unmuted.")
            else:
                await interaction.response.send_message(f"{member.mention} is not muted.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"I don't have permission to unmute {member.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Unmute(bot))
