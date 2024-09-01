import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='clearmessages', description='Clear a specified number of messages from a channel')
    @app_commands.checks.has_permissions(administrator=True)
    async def clearmessages(self, interaction: discord.Interaction, amount: int):
        """Clear a specified number of messages from the channel."""
        if amount <= 0:
            await interaction.response.send_message("Please provide a number greater than 0.")
            return

        # Fetch the channel where the command was used
        channel = interaction.channel

        # Try to delete the messages
        try:
            deleted = await channel.purge(limit=amount + 1)  # +1 to include the command message itself
            await interaction.response.send_message(f"Deleted {len(deleted) - 1} messages.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to delete messages in this channel.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
