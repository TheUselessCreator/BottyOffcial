import discord
from discord.ext import commands
from discord import app_commands

class CountGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counting_channels = {}  # Dictionary to store counting game settings per channel

    @app_commands.command(name="countcreate", description="Start an infinite counting game in a specified channel")
    @app_commands.describe(channel="The channel where the counting game should be started")
    async def count_create(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Start counting game in the specified channel."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        self.counting_channels[channel.id] = 1  # Start counting from 1

        await interaction.response.send_message(f"Counting game started in {channel.mention}. Messages should be the next number in sequence.", ephemeral=True)

    @app_commands.command(name="countdisable", description="Disable the counting game")
    async def count_disable(self, interaction: discord.Interaction):
        """Disable the counting game."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        # Remove all channels from the counting game
        self.counting_channels.clear()
        await interaction.response.send_message("Counting game disabled in all channels.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Check messages for the counting game."""
        if message.author.bot:
            return
        
        if message.channel.id in self.counting_channels:
            expected_number = self.counting_channels[message.channel.id]
            
            # Check if the message content is a number and matches the expected number
            if message.content.isdigit() and int(message.content) == expected_number:
                # Increment the number for the next expected message
                self.counting_channels[message.channel.id] += 1
            else:
                # Delete the message if it is not the expected number
                await message.delete()
                # Optionally, send a notification that the message was deleted
                await message.channel.send(f"Message from {message.author.mention} was deleted because it was not the correct number.")
                
async def setup(bot: commands.Bot):
    await bot.add_cog(CountGame(bot))
