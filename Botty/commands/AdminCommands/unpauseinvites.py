import discord
from discord.ext import commands
from discord import app_commands

class UnpauseInvites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='unpauseinvites', description='Unpause invites in the server (Admin only).')
    async def unpauseinvites(self, interaction: discord.Interaction):
        """Unpause server invites. Only Admins can use this."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required Administrator permissions to use this command.", ephemeral=True)
            return

        guild = interaction.guild

        # Restore invite creation permissions
        try:
            for channel in guild.text_channels:
                overwrite = channel.overwrites_for(guild.default_role)
                overwrite.create_instant_invite = True
                await channel.set_permissions(guild.default_role, overwrite=overwrite)
            await interaction.response.send_message("Invite creation has been re-enabled in all text channels.")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to change channel permissions.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(UnpauseInvites(bot))
