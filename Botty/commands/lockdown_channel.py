import discord
from discord.ext import commands
from discord import app_commands

class Lockdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='lockdown', description='Lockdown a channel (Admin only).')
    async def lockdown(self, interaction: discord.Interaction):
        """Lockdown the current channel. Only Admins can use this."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required Administrator permissions to use this command.", ephemeral=True)
            return

        channel = interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False

        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            await interaction.response.send_message(f"The channel {channel.mention} has been locked down.")
        except discord.Forbidden:
            await interaction.response.send_message(f"I don't have permission to lockdown {channel.mention}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Lockdown(bot))
