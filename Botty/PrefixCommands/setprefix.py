import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class SetPrefixCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixes = self.load_prefixes()

    # Load prefixes from JSON file
    def load_prefixes(self):
        if os.path.exists('prefixes.json'):
            with open('prefixes.json', 'r') as f:
                return json.load(f)
        else:
            return {}

    # Save prefixes to JSON file
    def save_prefixes(self):
        with open('prefixes.json', 'w') as f:
            json.dump(self.prefixes, f, indent=4)

    # Slash command to set the prefix for the current server
    @app_commands.command(name="setprefix", description="Set a custom prefix for this server.")
    async def set_prefix(self, interaction: discord.Interaction, prefix: str):
        """Set a custom prefix for the server using a slash command."""
        guild_id = str(interaction.guild.id)
        self.prefixes[guild_id] = prefix  # Set the new prefix for this guild
        self.save_prefixes()  # Save the prefixes to file

        await interaction.response.send_message(f"Prefix set to `{prefix}` for this server.")

    # Function to get the custom prefix for each server
    async def get_prefix(self, guild_id):
        return self.prefixes.get(guild_id, "/")  # Default to "/" if no custom prefix is set

# Setup function to load the cog
async def setup(bot):
    await bot.add_cog(SetPrefixCommand(bot))
