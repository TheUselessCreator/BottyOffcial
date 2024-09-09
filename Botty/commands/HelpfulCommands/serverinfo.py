import discord
from discord.ext import commands
from discord import app_commands
import os

class ServerInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='serverinfo', description='Get information about the server')
    async def serverinfo(self, interaction: discord.Interaction):
        try:
            # Gather server information
            guild = interaction.guild
            server_name = guild.name
            server_id = guild.id
            member_count = guild.member_count
            creation_date = guild.created_at.strftime("%Y-%m-%d %H:%M:%S")

            # Fetch the server owner
            owner = await guild.fetch_member(guild.owner_id)
            owner_name = owner.name if owner else "Unknown"
            owner_mention = owner.mention if owner else "Unknown"

            # Create embed
            embed = discord.Embed(
                title="Server Information",
                color=discord.Color.green()
            )
            embed.add_field(name="Server Name", value=server_name, inline=False)
            embed.add_field(name="Server ID", value=server_id, inline=False)
            embed.add_field(name="Members", value=member_count, inline=False)
            embed.add_field(name="Created At", value=creation_date, inline=False)
            embed.add_field(name="Owner", value=f"{owner_name} ({owner_mention})", inline=False)
            embed.set_footer(text="Botty - Server Info")

            # Send the embed
            await interaction.response.send_message(embed=embed)
            print("Server info command executed successfully")

        except Exception as e:
            print(f"An error occurred: {e}")
            await interaction.response.send_message("An error occurred while retrieving server information.")

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfoCommand(bot))
