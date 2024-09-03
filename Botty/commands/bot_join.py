import discord
from discord.ext import commands
import random

class BotJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Send a welcome message to a channel that contains 'announcement' or a random one if not found."""
        # Try to find a channel with 'announcement' in its name (case-insensitive)
        target_channel = None
        for channel in guild.text_channels:
            if 'announcement' in channel.name.lower():  # Case-insensitive search
                target_channel = channel
                break
        
        # If no channel with 'announcement' is found, choose a random channel
        if target_channel is None:
            target_channel = random.choice(guild.text_channels)

        # Create an embed message with information about the bot
        embed = discord.Embed(
            title="Hello from Botty!",
            description=(
                "Thank you for adding me to your server! 🎉\n\n"
                "I'm Botty, a bot designed to help with various tasks and provide entertainment.\n"
                "Feel free to use my commands and have fun! 😊\n\n"
                "Here are a few things you can do with me:\n"
                "- Use `/help` to see a list of commands.\n"
                "- Check out `/report` for reporting issues.\n"
                "- Use `/welcomeset` to set a welcome message channel."
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Bot version 1.0 | Discord server: {guild.name}")

        # Send the embed to the selected channel
        await target_channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(BotJoin(bot))
