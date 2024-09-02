import discord
from discord.ext import commands
from discord import app_commands

class Interact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='hug', description='Send a virtual hug to someone.')
    async def hug(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"{interaction.user.mention} hugs {member.mention} 🤗")

    @app_commands.command(name='poke', description='Poke someone for fun.')
    async def poke(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"{interaction.user.mention} pokes {member.mention} 🖐")

async def setup(bot: commands.Bot):
    await bot.add_cog(Interact(bot))
