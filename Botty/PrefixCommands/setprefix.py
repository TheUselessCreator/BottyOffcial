import discord
from discord.ext import commands
import json
import os

class SetPrefixCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixes = {}  # Dictionary to store prefixes
        self.load_prefixes()  # Load prefixes from file on initialization

    # Load prefixes from JSON file
    def load_prefixes(self):
        if os.path.exists('prefixes.json'):
            with open('prefixes.json', 'r') as f:
                self.prefixes = json.load(f)
        else:
            self.prefixes = {}

    # Save prefixes to JSON file
    def save_prefixes(self):
        with open('prefixes.json', 'w') as f:
            json.dump(self.prefixes, f, indent=4)

    # Command to set the prefix for a server
    @commands.command(name="setprefix")
    async def set_prefix(self, ctx, prefix):
        """Sets a custom prefix for this server."""
        guild_id = str(ctx.guild.id)
        self.prefixes[guild_id] = prefix  # Set the new prefix for this server
        self.save_prefixes()  # Save the updated prefixes to file
        await ctx.send(f"Prefix set to `{prefix}` for this server.")

    # Method to get the prefix for a server
    async def get_prefix(self, bot, message):
        guild_id = str(message.guild.id)
        return self.prefixes.get(guild_id, "/")  # Return the custom prefix or default "/" if not set

# Setup function to load the cog
async def setup(bot):
    await bot.add_cog(SetPrefixCommand(bot))
