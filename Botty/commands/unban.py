import discord
from discord.ext import commands
from discord import app_commands

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unban", description="Unban a user by their ID")
    @app_commands.describe(user_id="The ID of the user to unban")
    async def unban(self, interaction: discord.Interaction, user_id: str):
        """Unban a user by their Discord ID."""
        # Check if the user invoking the command has administrator permission
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        # Try to find the user in the ban list using their ID
        try:
            user = await self.bot.fetch_user(int(user_id))
        except ValueError:
            await interaction.response.send_message(f"Invalid ID format: {user_id}. Please provide a valid user ID.", ephemeral=True)
            return

        try:
            # Unban the user by ID
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"Successfully unbanned {user}.")
        except discord.NotFound:
            await interaction.response.send_message(f"User with ID {user_id} not found in the ban list.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to unban users.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred while trying to unban: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Unban(bot))
