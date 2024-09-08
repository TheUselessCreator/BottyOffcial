import discord
from discord.ext import commands

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

    @commands.command(name="setjoinrole")
    @commands.has_permissions(administrator=True)
    async def set_join_role(self, ctx, role: discord.Role):
        """Set the role to assign to new members."""
        self.join_role_id = role.id
        await ctx.send(f"Join role has been set to {role.name}.")

    @commands.command(name="clearjoinrole")
    @commands.has_permissions(administrator=True)
    async def clear_join_role(self, ctx):
        """Clear the current join role."""
        self.join_role_id = None
        await ctx.send("Join role has been cleared.")

async def setup(bot: commands.Bot):
    await bot.add_cog(JoinRole(bot))
