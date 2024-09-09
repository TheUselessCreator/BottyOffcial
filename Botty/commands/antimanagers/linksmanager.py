import discord
from discord.ext import commands
from discord import app_commands

class LinkControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.link_protection_enabled = False  # Default state is disabled
        self.allowed_channels = []  # List of channel IDs where links are allowed

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Delete messages with links if link protection is enabled and not in an allowed channel."""
        if message.author.bot:
            return  # Ignore bot messages
        
        if self.link_protection_enabled and message.channel.id not in self.allowed_channels:
            # Check if the message contains a link
            if "http://" in message.content or "https://" in message.content:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, links are not allowed in this channel!")
                # Optionally warn the user (this could be enhanced with a proper warning system)
                await message.author.send("You have been warned for posting links in a restricted channel.")
    
    @app_commands.command(name="linksdisable", description="Disable links in all channels except allowed ones")
    async def linksdisable(self, interaction: discord.Interaction):
        """Disable links in all channels except allowed ones."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        self.link_protection_enabled = True
        await interaction.response.send_message("Link protection has been enabled. Links will be deleted in restricted channels.", ephemeral=True)

    @app_commands.command(name="linksenable", description="Enable links in a specific channel")
    @app_commands.describe(channel="The channel where links should be allowed")
    async def linksenable(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Enable links in a specific channel."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        if channel.id not in self.allowed_channels:
            self.allowed_channels.append(channel.id)
            await interaction.response.send_message(f"Links are now allowed in {channel.mention}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Links are already allowed in {channel.mention}.", ephemeral=True)

    @app_commands.command(name="linksdisablechannel", description="Disable links in a specific channel")
    @app_commands.describe(channel="The channel where links should be disabled")
    async def linksdisablechannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Disable links in a specific channel."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        if channel.id in self.allowed_channels:
            self.allowed_channels.remove(channel.id)
            await interaction.response.send_message(f"Links are now disabled in {channel.mention}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Links are already disabled in {channel.mention}.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(LinkControl(bot))
