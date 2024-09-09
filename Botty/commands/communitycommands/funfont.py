import discord
from discord.ext import commands
from discord import app_commands

class FunFontCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='funfont', description='Convert text to fun font style')
    async def funfont(self, interaction: discord.Interaction, text: str):
        def to_fullwidth(text):
            """Convert ASCII text to full-width characters."""
            return ''.join(chr(0x1100 + (ord(char) - ord(' ') + 0x20)) if ' ' <= char <= '~' else char for char in text)

        # Convert text
        converted_text = to_fullwidth(text)

        # Send the response
        await interaction.response.send_message(converted_text)

async def setup(bot: commands.Bot):
    await bot.add_cog(FunFontCommand(bot))
