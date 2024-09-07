import discord
from discord.ext import commands
from discord import app_commands

class RolesCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='rolescount', description='Displays the total number of roles in the server.')
    async def rolescount(self, interaction: discord.Interaction):
        """Send the total role count of the server."""
        guild = interaction.guild
        if guild:
            roles_count = len(guild.roles)
            embed = discord.Embed(
                title="Roles Count",
                description=f"There are currently **{roles_count}** roles in this server.",
                color=discord.Color.purple()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RolesCount(bot))
