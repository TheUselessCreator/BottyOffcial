import discord
from discord.ext import commands
from discord import app_commands
import re

class AntiCaps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anti_caps_settings = {}  # Dictionary to store anti-caps settings per guild

    @app_commands.command(name="anticapsenable", description="Enable anti-caps protection with a specified amount of caps")
    @app_commands.describe(amount_of_caps="The number of capital letters that triggers the anti-caps")
    async def anticaps_enable(self, interaction: discord.Interaction, amount_of_caps: int):
        """Enable anti-caps protection."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        self.anti_caps_settings[guild_id] = {
            'enabled': True,
            'amount_of_caps': amount_of_caps
        }

        await interaction.response.send_message(f"Anti-caps protection enabled! Trigger limit: {amount_of_caps} capital letters.", ephemeral=True)

    @app_commands.command(name="anticapsdisable", description="Disable anti-caps protection")
    async def anticaps_disable(self, interaction: discord.Interaction):
        """Disable anti-caps protection."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        if guild_id in self.anti_caps_settings:
            del self.anti_caps_settings[guild_id]
            await interaction.response.send_message("Anti-caps protection has been disabled.", ephemeral=True)
        else:
            await interaction.response.send_message("Anti-caps protection is not enabled for this server.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Monitor messages for excessive capital letters."""
        if message.author.bot:
            return

        guild_id = message.guild.id
        if guild_id not in self.anti_caps_settings:
            return

        settings = self.anti_caps_settings[guild_id]
        if not settings['enabled']:
            return

        amount_of_caps = settings['amount_of_caps']
        if sum(1 for char in message.content if char.isupper()) > amount_of_caps:
            # Delete the message
            await message.delete()
            
            # Warn the user
            await message.author.send("You have been warned for using too many capital letters. Please avoid excessive capitalization.")
            
            # Timeout the user for 20 minutes
            timeout_duration = discord.utils.utcnow() + discord.timedelta(minutes=20)
            try:
                await message.author.edit(timed_out_until=timeout_duration)
            except discord.Forbidden:
                await message.author.send("I do not have permission to apply a timeout to you.")
            
            # Optionally, you might want to log the event or notify admins
            admin_channel = message.guild.system_channel
            if admin_channel:
                await admin_channel.send(f"User {message.author} was warned and timed out for using too many capital letters.")

async def setup(bot: commands.Bot):
    await bot.add_cog(AntiCaps(bot))
