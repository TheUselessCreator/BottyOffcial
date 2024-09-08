import discord
from discord.ext import commands
from discord import app_commands
import time

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.raid_settings = {}  # Dictionary to store raid settings per guild
        self.join_timestamps = {}  # Dictionary to store join timestamps per guild

    def get_guild_settings(self, guild_id):
        if guild_id not in self.raid_settings:
            self.raid_settings[guild_id] = {'enabled': False, 'user_limit': 0, 'time_limit': 0}
            self.join_timestamps[guild_id] = []
        return self.raid_settings[guild_id]

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Monitor user joins to detect potential raids."""
        guild_id = member.guild.id
        settings = self.get_guild_settings(guild_id)

        if settings['enabled']:
            current_time = time.time()
            join_timestamps = self.join_timestamps[guild_id]

            # Record the timestamp of the new join
            join_timestamps.append(current_time)
            join_timestamps = [t for t in join_timestamps if current_time - t < settings['time_limit']]

            if len(join_timestamps) > settings['user_limit']:
                # Trigger anti-raid actions
                await self.lockdown_server(member.guild)
                self.raid_settings[guild_id]['enabled'] = False
                self.join_timestamps[guild_id] = []  # Clear the timestamps
                return

            self.join_timestamps[guild_id] = join_timestamps

    async def lockdown_server(self, guild):
        """Disable invites and lock down the server for 1 hour."""
        # Disable invites
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(guild.default_role, send_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(guild.default_role, connect=False)

        # Send a notification
        await guild.system_channel.send("Anti-raid triggered! The server is locked down for 1 hour.")

        # Wait for 1 hour
        await asyncio.sleep(3600)

        # Re-enable permissions
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(guild.default_role, send_messages=True)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(guild.default_role, connect=True)

        # Send a notification
        await guild.system_channel.send("The server is now unlocked.")

    @app_commands.command(name="enableantiraid", description="Enable anti-raid protection")
    @app_commands.describe(user_limit="The number of users to trigger the anti-raid", time_limit="The time window in seconds")
    async def enableantiraid(self, interaction: discord.Interaction, user_limit: int, time_limit: int):
        """Enable anti-raid protection with a user limit and time window."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        self.raid_settings[guild_id] = {
            'enabled': True,
            'user_limit': user_limit,
            'time_limit': time_limit
        }

        await interaction.response.send_message(f"Anti-raid protection enabled! Trigger limit: {user_limit} users in {time_limit} seconds.", ephemeral=True)

    @app_commands.command(name="disableantiraid", description="Disable anti-raid protection")
    async def disableantiraid(self, interaction: discord.Interaction):
        """Disable anti-raid protection."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        guild_id = interaction.guild.id
        self.raid_settings[guild_id]['enabled'] = False
        await interaction.response.send_message("Anti-raid protection has been disabled.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(AntiRaid(bot))
