import discord
from discord.ext import commands
from discord import app_commands
from collections import defaultdict

class EmojiLimit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_limit_enabled = defaultdict(bool)  # Track if emoji limit is enabled per server
        self.emoji_limit_count = defaultdict(int)  # Track the emoji limit per server

    @app_commands.command(name='emojilimitenable', description='Enable emoji limit for this server')
    @commands.has_permissions(administrator=True)
    @app_commands.describe(amount="Maximum number of emojis allowed per message")
    async def emojilimitenable(self, interaction: discord.Interaction, amount: int):
        """Enable emoji limit for the server with a specified amount."""
        if amount <= 0:
            await interaction.response.send_message("Emoji limit must be a positive number.", ephemeral=True)
            return
        
        self.emoji_limit_enabled[interaction.guild.id] = True
        self.emoji_limit_count[interaction.guild.id] = amount
        await interaction.response.send_message(f"Emoji limit has been enabled with a maximum of {amount} emojis per message.", ephemeral=True)

    @app_commands.command(name='emojilimitdisable', description='Disable emoji limit for this server')
    @commands.has_permissions(administrator=True)
    async def emojilimitdisable(self, interaction: discord.Interaction):
        """Disable emoji limit for the server."""
        self.emoji_limit_enabled[interaction.guild.id] = False
        await interaction.response.send_message("Emoji limit has been disabled for this server.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Detect and handle messages exceeding emoji limit."""
        if message.author.bot:
            return

        guild_id = message.guild.id
        if not self.emoji_limit_enabled[guild_id]:
            return

        # Count the number of emojis in the message
        emoji_count = sum(1 for char in message.content if char in self.bot.emojis or char in set("\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF"))

        if emoji_count > self.emoji_limit_count[guild_id]:
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, your message contains too many emojis! (Limit: {self.emoji_limit_count[guild_id]})")
            except discord.Forbidden:
                print(f"Failed to delete message from {message.author.name} due to missing permissions.")
            except Exception as e:
                print(f"Error while processing emoji limit: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(EmojiLimit(bot))
