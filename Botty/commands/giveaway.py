import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import secrets
import string
import asyncio

USER_ID = os.getenv('USER_ID')  # Load the host's user ID from the .env file

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_giveaways = {}  # Store active giveaways by ID

    def generate_random_string(self, length: int = 12):
        """Generates a random alphanumeric string for the giveaway ID and management key."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    @app_commands.command(name='create_giveaway', description='Create a new giveaway')
    async def create_giveaway(self, interaction: discord.Interaction, duration: int, winners: int):
        """Creates a new giveaway with a duration (in minutes) and a number of winners."""
        
        if str(interaction.user.id) != USER_ID:
            await interaction.response.send_message("You don't have permission to create a giveaway.", ephemeral=True)
            return

        # Generate a random giveaway ID and a management key
        giveaway_id = self.generate_random_string(12)
        management_key = self.generate_random_string(12)
        
        # Store the giveaway details
        self.active_giveaways[giveaway_id] = {
            'host': interaction.user,
            'duration': duration,
            'winners': winners,
            'participants': [],
            'channel': interaction.channel
        }

        # Send a DM to the host with the management key
        try:
            await interaction.user.send(f"Your management key for giveaway ID {giveaway_id} is: {management_key}")
        except discord.Forbidden:
            await interaction.response.send_message("Could not send you a DM with the management key. Please enable DMs from server members.", ephemeral=True)
            return

        # Create an embed for the giveaway
        embed = discord.Embed(
            title="**Giveaway**",
            description=(
                f"**Hosted by:** {interaction.user.mention}\n"
                f"**Duration:** {duration} minutes\n"
                f"**Winners:** {winners}\n"
                f"**Giveaway ID:** {giveaway_id}"
            ),
            color=discord.Color.green()
        )

        # View for the buttons
        view = self.GiveawayView(self, giveaway_id)

        # Send the giveaway embed with buttons
        await interaction.response.send_message(embed=embed, view=view)

        # Start the timer for the giveaway
        await self.end_giveaway_after_delay(giveaway_id, duration)

    async def end_giveaway_after_delay(self, giveaway_id: str, duration: int):
        """Waits for the specified duration (in minutes) and ends the giveaway."""
        await asyncio.sleep(duration * 60)  # Convert minutes to seconds

        giveaway = self.active_giveaways.get(giveaway_id)
        if giveaway:
            channel = giveaway['channel']
            winners_count = giveaway['winners']
            participants = giveaway['participants']

            # Select the winners randomly
            if participants:
                winners = secrets.SystemRandom().sample(participants, min(winners_count, len(participants)))
            else:
                winners = []

            # Create an embed to announce the winners
            embed = discord.Embed(
                title="**Giveaway Ended!**",
                description=f"**Hosted by:** {giveaway['host'].mention}\n"
                            f"**Giveaway ID:** {giveaway_id}",
                color=discord.Color.red()
            )

            if winners:
                winner_mentions = ', '.join([winner.mention for winner in winners])
                embed.add_field(name="Winners", value=winner_mentions, inline=False)
            else:
                embed.add_field(name="Winners", value="No participants.", inline=False)

            await channel.send(embed=embed)

            # Remove the giveaway from active giveaways
            del self.active_giveaways[giveaway_id]

    class GiveawayView(discord.ui.View):
        def __init__(self, cog, giveaway_id):
            super().__init__(timeout=None)
            self.cog = cog
            self.giveaway_id = giveaway_id

        @discord.ui.button(label="Join Giveaway", style=discord.ButtonStyle.green)
        async def join_giveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
            """Handles the join giveaway button press."""
            giveaway = self.cog.active_giveaways[self.giveaway_id]
            if interaction.user not in giveaway['participants']:
                giveaway['participants'].append(interaction.user)
                await interaction.response.send_message(f"{interaction.user.mention} joined the giveaway!", ephemeral=True)
            else:
                await interaction.response.send_message("You're already in the giveaway.", ephemeral=True)

        @discord.ui.button(label="Leave Giveaway", style=discord.ButtonStyle.red)
        async def leave_giveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
            """Handles the leave giveaway button press."""
            giveaway = self.cog.active_giveaways[self.giveaway_id]
            if interaction.user in giveaway['participants']:
                giveaway['participants'].remove(interaction.user)
                await interaction.response.send_message(f"{interaction.user.mention} left the giveaway.", ephemeral=True)
            else:
                await interaction.response.send_message("You are not in the giveaway.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))
