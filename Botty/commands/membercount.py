import discord
from discord.ext import commands
from discord import app_commands

class MembersCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='memberscount', description='Displays the total number of members in the server.')
    async def memberscount(self, interaction: discord.Interaction):
        """Send the total member count of the server."""
        guild = interaction.guild
        if guild:
            member_count = guild.member_count
            embed = discord.Embed(
                title="Member Count",
                description=f"There are currently **{member_count}** members in this server.",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(MembersCount(bot))
