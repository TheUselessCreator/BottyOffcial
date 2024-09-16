import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, Select

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ticketsetup', description='Set up the ticket system in a specified channel with a given staff role.')
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_setup(self, interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role):
        """Sets up the ticket system and sends the dropdown menu in the specified channel."""

        # Dropdown for selecting issue type
        class TicketDropdown(Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label="Bot Problem", value="bot_problem"),
                    discord.SelectOption(label="Server Problem", value="server_problem"),
                    discord.SelectOption(label="GitHub Problem", value="github_problem"),
                    discord.SelectOption(label="Website Problem", value="website_problem"),
                    discord.SelectOption(label="Other", value="other"),
                ]
                super().__init__(placeholder="Select an issue...", options=options)

            async def callback(self, interaction: discord.Interaction):
                # Prevent interaction timeout issues
                await interaction.response.defer()

                issue = self.values[0]
                await interaction.followup.send("Creating your ticket...", ephemeral=True)

                # Create a new ticket channel
                category = channel.category  # Use the same category as the chosen channel
                ticket_channel = await interaction.guild.create_text_channel(
                    f'ticket-{interaction.user.name}',
                    category=category
                )

                # Set permissions so only the user and staff can view the channel
                await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
                await ticket_channel.set_permissions(role, view_channel=True)
                await ticket_channel.set_permissions(interaction.user, view_channel=True)

                # Embed for the ticket
                embed = discord.Embed(
                    title="New Ticket Created",
                    description=f"**Issue:** {self.values[0].replace('_', ' ').title()}\n**User:** {interaction.user.mention}",
                    color=discord.Color.blue()
                )
                embed.set_footer(text="Please use the buttons below to manage this ticket.")
                
                # View with claim, close, and close with reason buttons
                view = TicketActions(role)

                await ticket_channel.send(embed=embed, view=view)
                await interaction.user.send(f"Your ticket has been created: {ticket_channel.mention}")

        # Create a view for the dropdown
        view = View()
        view.add_item(TicketDropdown())

        # Send the dropdown to the specified channel
        await channel.send("Please select your issue from the dropdown:", view=view)

class TicketActions(View):
    def __init__(self, staff_role):
        super().__init__(timeout=None)  # Set no timeout to avoid button expiration
        self.staff_role = staff_role
        self.claimed = False

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.green)
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.staff_role not in interaction.user.roles:
            await interaction.response.send_message("You do not have permission to claim this ticket.", ephemeral=True)
        else:
            if not self.claimed:
                self.claimed = True
                await interaction.response.send_message("Ticket claimed!", ephemeral=True)
            else:
                await interaction.response.send_message("This ticket has already been claimed.", ephemeral=True)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def close_ticket_no_reason(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.channel.delete(reason="Ticket closed by staff")

    @discord.ui.button(label="Close with Reason", style=discord.ButtonStyle.grey)
    async def close_ticket_reason(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Prevent interaction timeout issues
        await interaction.response.defer()

        # Create a modal for the reason
        modal = CloseReasonModal()
        await interaction.response.send_modal(modal)

class CloseReasonModal(discord.ui.Modal, title="Close Ticket with Reason"):
    reason = discord.ui.TextInput(label="Reason", placeholder="Enter the reason for closing the ticket", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.channel.delete(reason=f"Ticket closed with reason: {self.reason.value}")
        await interaction.user.send(f"Your ticket has been closed with reason: {self.reason.value}")

# Ensure the bot syncs commands
@commands.Cog.listener()
async def on_ready():
    print(f'{bot.user} is ready!')
    await bot.tree.sync()

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
