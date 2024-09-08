import discord
from discord.ext import commands
from discord import app_commands

class JoinRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.join_role_id = None  # Store the role ID for automatic assignment

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Assign a role to a user when they join the server."""
        if self.join_role_id is None:
            return  # No role has been set
        
        role = member.guild.get_role(self.join_role_id)
        if role is not None:
            try:
                await member.add_roles(role)
                print(f"Assigned role {role.name} to {member.name}")
            except discord.Forbidden:
                print(f"Missing permissions to assign the role {role.name} to {member.name}")
            except discord.HTTPException as e:
                print(f"Failed to assign role {role.name} to {member.name}: {e}")

    @app_commands.command(name="setjoinrole", description="Set the role to assign to new members")
    @app_commands.describe(role="The role to assign to new members")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_join_role(self, interaction: discord.Interaction, role: discord.Role):
        """Slash command to set the role to assign to new members."""
        self.join_role_id = role.id
        await interaction.response.send_message(f"Join role has been set to {role.name}.", ephemeral=True)

    @app_commands.command(name="clearjoinrole", description="Clear the role for new members")
    @app_commands.checks.has_permissions(administrator=True)
    async def clear_join_role(self, interaction: discord.Interaction):
        """Slash command to clear the current join role."""
        self.join_role_id = None
        await interaction.response.send_message("Join role has been cleared.", ephemeral=True)

    async def cog_load(self):
        # Sync commands globally across all servers
        self.bot.tree.add_command(self.set_join_role)
        self.bot.tree.add_command(self.clear_join_role)
        await self.bot.tree.sync()

async def setup(bot: commands.Bot):
    await bot.add_cog(JoinRole(bot))
