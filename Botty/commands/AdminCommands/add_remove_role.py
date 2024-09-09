import discord
from discord.ext import commands
from discord import app_commands

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='addrole', description='Add a role to a user')
    @app_commands.checks.has_permissions(administrator=True)
    async def addrole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Add a specified role to a user."""
        # Check if the bot has permission to manage roles
        if not interaction.guild.me.guild_permissions.manage_roles:
            await interaction.response.send_message("I don't have permission to manage roles.", ephemeral=True)
            return

        # Check if the role is lower than the bot's highest role
        if role.position >= interaction.guild.me.top_role.position:
            await interaction.response.send_message("I cannot assign this role due to role hierarchy.", ephemeral=True)
            return

        try:
            await member.add_roles(role)
            await interaction.response.send_message(f"Added role {role.mention} to {member.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to add roles to this user.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name='removerole', description='Remove a role from a user')
    @app_commands.checks.has_permissions(administrator=True)
    async def removerole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        """Remove a specified role from a user."""
        # Check if the bot has permission to manage roles
        if not interaction.guild.me.guild_permissions.manage_roles:
            await interaction.response.send_message("I don't have permission to manage roles.", ephemeral=True)
            return

        # Check if the role is lower than the bot's highest role
        if role.position >= interaction.guild.me.top_role.position:
            await interaction.response.send_message("I cannot remove this role due to role hierarchy.", ephemeral=True)
            return

        try:
            await member.remove_roles(role)
            await interaction.response.send_message(f"Removed role {role.mention} from {member.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to remove roles from this user.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RoleManagement(bot))
