import discord
from discord import app_commands
from discord.ext import commands

class PellaCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Define the /pella slash command
    @app_commands.command(name="pella", description="Send an embed for a Discord hosting site")
    async def pella(self, interaction: discord.Interaction):
        # Create the embed message
        embed = discord.Embed(
            title="Join Pella Hosting",
            description="Looking for a reliable Discord bot hosting service? Join using the link below!",
            color=discord.Color.blue()
        )
        
        # Add the link to the embed
        embed.add_field(name="Link", value="[Join Pella Hosting](https://pella.app/?r=805b057c)", inline=False)
        
        # Set the footer and other details
        embed.set_footer(text="Powered by Pella.app")
        
        # Send the embed
        await interaction.response.send_message(embed=embed)

# Set up the cog and add it to the bot
async def setup(bot):
    await bot.add_cog(PellaCommand(bot))
