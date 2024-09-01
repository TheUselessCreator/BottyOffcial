import discord
from discord.ext import commands
from discord import app_commands

class NicknameChange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='nick', description='Change a user’s nickname')
    @app_commands.checks.has_permissions(administrator=True)
    async def nick(self, interaction: discord.Interaction, user: discord.Member, *, new_nickname: str):
        """Change a user’s nickname."""
        try:
            # Change the nickname
            await user.edit(nick=new_nickname)
            await interaction.response.send_message(f"Nickname changed for {user.mention} to `{new_nickname}`.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to change nicknames.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(NicknameChange(bot))
