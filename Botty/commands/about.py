import discord
from discord.ext import commands
from discord import app_commands
import os

class AboutCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='about', description='Get information about the bot')
    async def about(self, interaction: discord.Interaction):
        # Information to include
        support_server_url = "https://discord.gg/TGTaXgA2yr"
        creator_name = "TheUselessCreator"
        website_url = "https://sites.google.com/view/botty-help/home"
        bot_version = "1.0.0"
        bot_description = "Botty is an advanced Discord bot designed to provide various utilities and fun features. From moderation to interactive commands, Botty aims to enhance your server's experience with ease and efficiency."

        # Create embed
        embed = discord.Embed(
            title="About This Bot",
            description="Here's some information about the bot:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Description", value=bot_description, inline=False)
        embed.add_field(name="Creator", value=creator_name, inline=False)
        embed.add_field(name="Website", value=f"[Visit Website]({website_url})", inline=False)
        embed.add_field(name="Support Server", value=f"[Join Support Server]({support_server_url})", inline=False)
        embed.add_field(name="Bot Version", value=bot_version, inline=False)
        embed.set_footer(text="Made with ❤️ by TheUselessCreator")

        # Send the embed
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(AboutCommand(bot))
