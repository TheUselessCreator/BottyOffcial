import discord
from discord.ext import commands
import json
import os

# Path to the JSON file where prefixes are stored for each guild
PREFIX_FILE_PATH = os.path.join(os.path.dirname(__file__), '../assets/prefixes.json')

# Function to load all prefixes from the JSON file
def load_prefixes():
    try:
        with open(PREFIX_FILE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save prefixes to the JSON file
def save_prefixes(prefixes):
    with open(PREFIX_FILE_PATH, 'w') as f:
        json.dump(prefixes, f, indent=4)

# Function to get the prefix for a specific guild
def get_guild_prefix(guild_id):
    prefixes = load_prefixes()
    return prefixes.get(str(guild_id), '/')  # Default prefix is '/'

# Cog for setting and getting the prefix
class SetPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command to set the new prefix for the current guild
    @commands.hybrid_command(name="setprefix")
    async def setprefix(self, ctx, prefix: str):
        """Sets a new prefix for the bot in the current server."""
        if ctx.author.guild_permissions.administrator:
            # Load existing prefixes
            prefixes = load_prefixes()
            # Set the new prefix for the current guild
            prefixes[str(ctx.guild.id)] = prefix
            save_prefixes(prefixes)
            # Update the bot's prefix function
            self.bot.command_prefix = self.get_prefix
            await ctx.send(f"Prefix updated to: `{prefix}` for this server.")
        else:
            await ctx.send("You do not have permission to use this command.")

    # Function to return the current prefix for each guild
    async def get_prefix(self, bot, message):
        if message.guild:
            return get_guild_prefix(message.guild.id)
        else:
            return '/'  # Default prefix in DMs

async def setup(bot):
    await bot.add_cog(SetPrefix(bot))

