import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, Select, Modal, TextInput

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ticketsetup', description='Sets up the ticket system in a specified channel with a given staff role.')
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_setup(self, interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role):
        """Sets up the ticket system and sends the dropdown menu in the specified channel."""
        # Store channel and role in the bot's internal memory or a database/file if needed
        self.ticket_channel_id = channel.id
        self.staff_role_id = role.id

        # Create dropdown menu for ticket issues
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
                issue = self.values[0]
                await interaction.response.send_message("Creating ticket...", ephemeral=True)
                
                ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.id}', category=interaction.channel.category)
                await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
                await ticket_channel.set_permissions(role, view_channel=True)
                await ticket_channel.set_permissions(interaction.user, view_channel=True)

                embed = discord.Embed(
                    title="New Ticket",
                    description=f"**Issue:** {issue}\n**User:** {interaction.user.mention}",
                    color=discord.Color.blue()
                )
                await ticket_channel.send(embed=embed, view=TicketActions())
                await interaction.user.send(f"Your ticket has been created: {ticket_channel.mention}")

        view = View()
        view.add_item(TicketDropdown())
        await channel.send("Please select your issue:", view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data['custom_id'] == 'claim_ticket':
            if not any(role.id == self.staff_role_id for role in interaction.user.roles):
                await interaction.response.send_message("You do not have permission to claim tickets.", ephemeral=True)
                return
            await interaction.response.send_message("Ticket claimed!", ephemeral=True)
            # Handle claim logic here

        elif interaction.data['custom_id'] == 'close_ticket':
            if not any(role.id == self.staff_role_id for role in interaction.user.roles):
                await interaction.response.send_message("You do not have permission to close tickets.", ephemeral=True)
                return
            ticket_channel = interaction.channel
            await ticket_channel.delete()
            await interaction.user.send("Your ticket has been closed!")

        elif interaction.data['custom_id'] == 'close_ticket_reason':
            if not any(role.id == self.staff_role_id for role in interaction.user.roles):
                await interaction.response.send_message("You do not have permission to close tickets.", ephemeral=True)
                return
            await interaction.response.send_message("Please provide a reason for closing the ticket.", ephemeral=True)

            class ReasonModal(Modal):
                def __init__(self):
                    super().__init__(title="Close Ticket Reason")
                    self.add_item(TextInput(label="Reason", placeholder="Enter the reason here..."))

                async def callback(self, interaction: discord.Interaction):
                    reason = self.children[0].value
                    await interaction.response.send_message(f"Ticket closed with reason: {reason}", ephemeral=True)
                    await interaction.user.send(f"Your ticket has been closed with the following reason: {reason}")

            await interaction.response.send_modal(ReasonModal())

class TicketActions(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="Claim", style=discord.ButtonStyle.green, custom_id="claim_ticket"))
        self.add_item(Button(label="Close", style=discord.ButtonStyle.red, custom_id="close_ticket"))
        self.add_item(Button(label="Close with Reason", style=discord.ButtonStyle.grey, custom_id="close_ticket_reason"))

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
