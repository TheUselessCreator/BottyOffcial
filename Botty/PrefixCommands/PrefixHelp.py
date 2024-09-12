import discord
from discord.ext import commands
import json
import os

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Displays a help message with available commands."""
        # Load the prefixes.json to get the current prefix for the server
        guild_id = str(ctx.guild.id)
        default_prefix = "/"
        prefix = default_prefix  # Default prefix if not found in the JSON file

        # Check if prefixes.json exists
        if os.path.exists('prefixes.json'):
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)
            prefix = prefixes.get(guild_id, default_prefix)  # Use server-specific prefix if available

        # Create an embed for the help message
        embed = discord.Embed(
            title="Bot Commands Help",
            description=f"Here are the available commands. Use the prefix `{prefix}` for prefix-based commands.",
            color=discord.Color.blue()
        )

        # Add a list of available commands here (just examples, adjust based on your actual commands)
        embed.add_field(name=f"{prefix}help", value="Shows this help message.", inline=False)
        embed.add_field(name=f"{prefix}setprefix <prefix>", value="Set a custom prefix for this server.", inline=False)
        # Add other prefix commands as needed
        embed.add_field(name=f"{prefix}ping", value="Check the bot's response time.", inline=False)
        # Add more commands as needed

        # Send the embed
        await ctx.send(embed=embed)

# Setup function to load the cog
async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
