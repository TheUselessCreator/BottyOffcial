import discord
from discord.ext import commands
from discord import app_commands

class WelcomeSet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = None  # This will store the channel ID for welcome messages

    @app_commands.command(name="welcomeset", description="Set the channel for welcome messages")
    @app_commands.describe(channel="The channel where welcome messages should be sent")
    async def welcomeset(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Set the channel for welcome messages."""
        # Check if the user has administrator permission
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        
        # Set the welcome channel
        self.welcome_channel_id = channel.id
        await interaction.response.send_message(f"Welcome messages will be sent in {channel.mention}.", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Send a welcome message when a new member joins."""
        if self.welcome_channel_id is None:
            return  # Do nothing if no channel has been set

        channel = self.bot.get_channel(self.welcome_channel_id)
        if channel:
            # Get the member count
            member_count = member.guild.member_count

            # Create an embed message for the welcome
            embed = discord.Embed(
                title="Welcome to the server!",
                description=f"Welcome {member.mention}!\nYou are our **#{member_count}** member.\nThanks for joining!",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)  # Show the user's avatar in the embed
            embed.set_footer(text=f"Joined on {member.joined_at.strftime('%Y-%m-%d')}")

            # Send the embed to the welcome channel
            await channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(WelcomeSet(bot))
