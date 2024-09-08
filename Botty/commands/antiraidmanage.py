import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anti_raid_settings = {}  # Dictionary to store anti-raid settings per guild

    @app_commands.command(name="enableantiraid", description="Enable anti-raid protection with a user count and time limit")
    @app_commands.describe(user_count="The number of users that triggers the anti-raid", time_limit="The time window in minutes")
    async def enable_antiraid(self, interaction: discord.Interaction, user_count: int, time_limit: int):
        """Enable anti-raid protection."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        self.anti_raid_settings[guild_id] = {
            'enabled': True,
            'user_count': user_count,
            'time_limit': time_limit
        }

        await interaction.response.send_message(f"Anti-raid protection enabled! Trigger limit: {user_count} users in {time_limit} minutes.", ephemeral=True)

    @app_commands.command(name="disableantiraid", description="Disable anti-raid protection")
    async def disable_antiraid(self, interaction: discord.Interaction):
        """Disable anti-raid protection."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        if guild_id in self.anti_raid_settings:
            del self.anti_raid_settings[guild_id]
            await interaction.response.send_message("Anti-raid protection has been disabled.", ephemeral=True)
        else:
            await interaction.response.send_message("Anti-raid protection is not enabled for this server.", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Monitor new members to detect potential raids."""
        guild_id = member.guild.id
        if guild_id not in self.anti_raid_settings:
            return

        settings = self.anti_raid_settings[guild_id]
        if not settings['enabled']:
            return

        # Check for potential raid
        recent_join_count = sum(1 for m in member.guild.members if (discord.utils.utcnow() - m.joined_at).total_seconds() < settings['time_limit'] * 60)

        if recent_join_count >= settings['user_count']:
            # Perform anti-raid actions
            await self.perform_anti_raid_actions(member.guild)

    async def perform_anti_raid_actions(self, guild):
        """Perform actions to mitigate a raid."""
        # Disable invites and lock the server
        for channel in guild.channels:
            await channel.set_permissions(guild.default_role, send_messages=False, read_messages=False)

        await guild.system_channel.send("**Anti-Raid Protection Activated:** Too many users joined in a short time. The server is now locked down for 1 hour.")

        # Optionally, you might want to log the event or notify admins
        for admin in guild.members:
            if admin.guild_permissions.administrator:
                try:
                    await admin.send(f"**Anti-Raid Alert:** {guild.name} has been locked down due to a potential raid.")
                except discord.Forbidden:
                    pass

        # Re-enable server permissions after 1 hour
        await asyncio.sleep(3600)  # 1 hour

        for channel in guild.channels:
            await channel.set_permissions(guild.default_role, send_messages=True, read_messages=True)
        
        await guild.system_channel.send("**Anti-Raid Protection Deactivated:** The server has been unlocked.")

async def setup(bot: commands.Bot):
    await bot.add_cog(AntiRaid(bot))
