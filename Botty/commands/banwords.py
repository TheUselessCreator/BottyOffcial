import discord
from discord.ext import commands
from discord import app_commands

class BannedWords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_words = set()  # Set to store banned words

    # Command to add a banned word
    @app_commands.command(name='banwords', description='Add a word to the banned words list')
    @app_commands.checks.has_permissions(administrator=True)
    async def banwords(self, interaction: discord.Interaction, word: str):
        """Add a word to the banned words list."""
        word = word.lower()
        self.banned_words.add(word)
        await interaction.response.send_message(f"Word '{word}' has been banned.", ephemeral=True)

    # Command to get the list of banned words
    @app_commands.command(name='banwordsget', description='Get the list of banned words')
    @app_commands.checks.has_permissions(administrator=True)
    async def banwordsget(self, interaction: discord.Interaction):
        """Get the list of banned words."""
        if not self.banned_words:
            await interaction.response.send_message("No banned words have been set.", ephemeral=True)
            return

        banned_words_list = "\n".join(self.banned_words)
        embed = discord.Embed(
            title="Banned Words List",
            description=banned_words_list,
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # Event listener to check for banned words in messages
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Check messages for banned words."""
        if message.author == self.bot.user:
            return  # Ignore messages from the bot itself

        for word in self.banned_words:
            if word in message.content.lower():
                # Apply a timeout and warning
                try:
                    await message.author.timeout_for(discord.utils.utcnow() + discord.timedelta(days=1), reason="Used a banned word.")
                    await message.author.send("You have been timed out for using a banned word.")
                except Exception as e:
                    print(f"Failed to apply timeout: {e}")

                await message.channel.send(f"{message.author.mention}, you used a banned word and have been timed out.")
                break

async def setup(bot: commands.Bot):
    await bot.add_cog(BannedWords(bot))
