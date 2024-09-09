import discord
from discord.ext import commands
from discord import app_commands
import os

class OwnerGive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin_id = int(os.getenv('USER_ID'))

    @app_commands.command(name='ownergive', description='Assign a role to a user. Only the specified user can use this command.')
    async def ownergive(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Assign a role to a user. Only the specified USER_ID can use this command."""
        if interaction.user.id != self.admin_id:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        # Check if the role is higher than the bot's highest role
        if role.position >= interaction.guild.me.top_role.position:
            await interaction.response.send_message("I cannot assign a role higher than my highest role.", ephemeral=True)
            return

        # Check if the bot has permission to manage roles
        if not interaction.guild.me.guild_permissions.manage_roles:
            await interaction.response.send_message("I do not have permission to manage roles.", ephemeral=True)
            return

        # Assign the role to the member
        try:
            await member.add_roles(role)
            await interaction.response.send_message(f"Role {role.name} has been assigned to {member.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to assign this role.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerGive(bot))
