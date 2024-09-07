import discord
from discord.ext import commands
import os

class OwnerGive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.admin_id = int(os.getenv('USER_ID'))

    @commands.command(name='ownergive', help='Assigns a role to a user. Only the specified user can use this command.')
    async def ownergive(self, ctx, member: discord.Member, role: discord.Role):
        """Assign a role to a user. Only the specified USER_ID can use this command."""
        if ctx.author.id != self.admin_id:
            await ctx.send("You do not have permission to use this command.")
            return

        # Check if the role is higher than the bot's highest role
        if role.position >= ctx.guild.me.top_role.position:
            await ctx.send("I cannot assign a role higher than my highest role.")
            return

        # Check if the bot has permission to manage roles
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.send("I do not have permission to manage roles.")
            return

        # Assign the role to the member
        try:
            await member.add_roles(role)
            await ctx.send(f"Role {role.name} has been assigned to {member.mention}.")
        except discord.Forbidden:
            await ctx.send("I do not have permission to assign this role.")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerGive(bot))
