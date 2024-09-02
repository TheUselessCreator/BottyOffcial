import discord
from discord.ext import commands
from discord import app_commands

class PauseInvites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='pauseinvites', description='Pause invites in the server (Admin only).')
    async def pauseinvites(self, interaction: discord.Interaction):
        """Pause server invites. Only Admins can use this."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required Administrator permissions to use this command.", ephemeral=True)
            return

        guild = interaction.guild

        # Revoke all existing invites
        try:
            invites = await guild.invites()
            for invite in invites:
                await invite.delete()
            await interaction.response.send_message("All existing invites have been revoked.")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to revoke invites.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

        # Disable invite creation by changing permissions
        try:
            for channel in guild.text_channels:
                overwrite = channel.overwrites_for(guild.default_role)
                overwrite.create_instant_invite = False
                await channel.set_permissions(guild.default_role, overwrite=overwrite)
            await interaction.response.send_message("New invites have been disabled in all text channels.")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to change channel permissions.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(PauseInvites(bot))
