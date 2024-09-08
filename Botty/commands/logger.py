import discord
from discord.ext import commands
from discord import app_commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logs_channels = {}  # Dictionary to store logs channels for each guild

    def save_logs_channel(self, guild_id, channel_id):
        self.logs_channels[guild_id] = channel_id

    def get_logs_channel(self, guild_id):
        return self.logs_channels.get(guild_id)

    @app_commands.command(name="logsset", description="Set the logging channel")
    @app_commands.checks.has_permissions(administrator=True)
    async def logsset(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Command to set the logging channel."""
        self.save_logs_channel(interaction.guild.id, channel.id)
        await interaction.response.send_message(f"Logs will be sent to {channel.mention}")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """Log when a message is deleted."""
        logs_channel_id = self.get_logs_channel(message.guild.id)
        if logs_channel_id:
            logs_channel = message.guild.get_channel(int(logs_channel_id))
            if logs_channel:
                embed = discord.Embed(
                    title="Message Deleted",
                    description=f"A message by {message.author.mention} was deleted in {message.channel.mention}",
                    color=discord.Color.red()
                )
                embed.add_field(name="Content", value=message.content or "No content", inline=False)
                embed.set_footer(text=f"Message ID: {message.id}")
                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """Log when a message is edited."""
        logs_channel_id = self.get_logs_channel(before.guild.id)
        if logs_channel_id:
            logs_channel = before.guild.get_channel(int(logs_channel_id))
            if logs_channel:
                embed = discord.Embed(
                    title="Message Edited",
                    description=f"A message by {before.author.mention} was edited in {before.channel.mention}",
                    color=discord.Color.orange()
                )
                embed.add_field(name="Before", value=before.content or "No content", inline=False)
                embed.add_field(name="After", value=after.content or "No content", inline=False)
                embed.set_footer(text=f"Message ID: {before.id}")
                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        """Log when a member is banned."""
        logs_channel_id = self.get_logs_channel(guild.id)
        if logs_channel_id:
            logs_channel = guild.get_channel(int(logs_channel_id))
            if logs_channel:
                embed = discord.Embed(
                    title="Member Banned",
                    description=f"{user.mention} has been banned from the server.",
                    color=discord.Color.dark_red()
                )
                embed.set_footer(text=f"User ID: {user.id}")
                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Log when a member leaves the server (kick or leave)."""
        logs_channel_id = self.get_logs_channel(member.guild.id)
        if logs_channel_id:
            logs_channel = member.guild.get_channel(int(logs_channel_id))
            if logs_channel:
                embed = discord.Embed(
                    title="Member Left/Kicked",
                    description=f"{member.mention} has left or was kicked from the server.",
                    color=discord.Color.light_grey()
                )
                embed.set_footer(text=f"User ID: {member.id}")
                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Log when a member is timed out or other role changes."""
        logs_channel_id = self.get_logs_channel(before.guild.id)
        if logs_channel_id:
            logs_channel = before.guild.get_channel(int(logs_channel_id))
            if logs_channel:
                if before.timed_out_until != after.timed_out_until:
                    if after.timed_out_until:
                        embed = discord.Embed(
                            title="Member Timed Out",
                            description=f"{after.mention} has been timed out.",
                            color=discord.Color.dark_orange()
                        )
                        embed.set_footer(text=f"User ID: {after.id}")
                        await logs_channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Member Timeout Ended",
                            description=f"{after.mention}'s timeout has ended.",
                            color=discord.Color.green()
                        )
                        embed.set_footer(text=f"User ID: {after.id}")
                        await logs_channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Logs(bot))
