import discord
from discord.ext import commands

class LockdownServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lockdown-server', description='Lock down the entire server.')
    @commands.has_permissions(administrator=True)
    async def lockdown_server(self, ctx):
        """Lock down the server by disabling everyone’s permissions."""
        guild = ctx.guild
        for role in guild.roles:
            try:
                await role.edit(permissions=discord.Permissions.none())
            except discord.Forbidden:
                await ctx.send(f"Could not modify permissions for the role {role.name}.")
                continue
        await ctx.send("The server has been locked down.")

    @commands.command(name='unlockdown-server', description='Unlock the server and restore default permissions.')
    @commands.has_permissions(administrator=True)
    async def unlockdown_server(self, ctx):
        """Unlock the server by restoring default permissions for everyone."""
        guild = ctx.guild
        for role in guild.roles:
            try:
                # Restoring default permissions for @everyone
                if role.name == '@everyone':
                    await role.edit(permissions=discord.Permissions.default())
                else:
                    # Other roles can be restored as needed
                    await role.edit(permissions=discord.Permissions.default())
            except discord.Forbidden:
                await ctx.send(f"Could not modify permissions for the role {role.name}.")
                continue
        await ctx.send("The server has been unlocked.")

async def setup(bot: commands.Bot):
    await bot.add_cog(LockdownServer(bot))
