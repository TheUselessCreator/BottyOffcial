import discord
from discord.ext import commands
from discord import app_commands

class JoinRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.join_role = None  # Role to be assigned to new members

    @app_commands.command(name='joinrole', description='Set the role that will be assigned to new members')
    @app_commands.describe(role='The role to assign to new members')
    @commands.has_permissions(administrator=True)
    async def set_join_role(self, interaction: discord.Interaction, role: discord.Role):
        self.join_role = role
        await interaction.response.send_message(f"The role {role.name} will be assigned to new members.", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if self.join_role:
            try:
                await member.add_roles(self.join_role)
                print(f"Assigned role {self.join_role.name} to {member.name}.")
            except discord.Forbidden:
                print(f"Failed to assign role {self.join_role.name} to {member.name}.")
            except Exception as e:
                print(f"Error assigning role to {member.name}: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(JoinRole(bot))
