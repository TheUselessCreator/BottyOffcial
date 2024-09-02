import discord
from discord.ext import commands
import random

class BotJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Send a welcome message to a random text channel when the bot joins a server."""
        # Filter to get only text channels
        text_channels = [channel for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages]
        
        if not text_channels:
            print(f"No text channels available in {guild.name}")
            return
        
        # Choose a random text channel
        channel = random.choice(text_channels)

        # Create an embed message with information about the bot
        embed = discord.Embed(
            title="Hello from Botty!",
            description=(
                "Thank you for adding me to your server! 🎉\n\n"
                "I'm Botty, a bot designed to help with various tasks and provide entertainment.\n"
                "Feel free to use my commands and have fun! 😊\n\n"
                "Here are a few things you can do with me:\n"
                "- Use `/extrahelp` to see a list of commands.\n"
                "- Check out `/report` for reporting issues.\n"
                "- Use `/welcomeset` to set a welcome message channel."
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Bot version 9.7 | Discord server: {guild.name}")

        # Send the embed to the chosen channel
        await channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(BotJoin(bot))
