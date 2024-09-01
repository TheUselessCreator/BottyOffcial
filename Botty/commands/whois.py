import discord
from discord.ext import commands
from discord import app_commands

class Whois(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="whois", description="Get information about a user.")
    @app_commands.describe(user="The user to get information about.")
    async def whois(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user  # Default to the command user if no user is specified

        # Create an embed with user information
        embed = discord.Embed(title=f"User Information: {user}", color=discord.Color.blue())
        embed.add_field(name="Username", value=user.name, inline=True)
        embed.add_field(name="Discriminator", value=user.discriminator, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Bot", value="Yes" if user.bot else "No", inline=True)
        embed.add_field(name="Joined At", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(user, 'joined_at') else "N/A", inline=True)
        embed.add_field(name="Created At", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.set_thumbnail(url=user.avatar.url if user.avatar else discord.Embed.Empty)

        # Send the embed message
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Whois(bot))
