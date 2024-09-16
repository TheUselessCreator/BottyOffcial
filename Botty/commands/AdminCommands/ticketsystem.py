import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, Modal, TextInput

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_channel_id = None
        self.staff_role_id = None

    @app_commands.command(name='ticketsetup', description='Sets up the ticket system in a specified channel with a given staff role.')
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_setup(self, interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role):
        """Sets up the ticket system and sends the dropdown menu in the specified channel."""
        self.ticket_channel_id = channel.id
        self.staff_role_id = role.id

        class TicketDropdown(discord.ui.Select):
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
                
                # Create a new ticket channel
                ticket_channel = await interaction.guild.create_text_channel(
                    f'ticket-{interaction.user.id}', 
                    category=interaction.channel.category
                )
                await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
                await ticket_channel.set_permissions(role, view_channel=True)
                await ticket_channel.set_permissions(interaction.user, view_channel=True)

                # Send embed with buttons to the ticket channel
                embed = discord.Embed(
                    title="New Ticket",
                    description=f"**Issue:** {issue}\n**User:** {interaction.user.mention}",
                    color=discord.Color.blue()
                )
                embed.set_footer(text="Please use the buttons below to manage this ticket.")

                staff_role = interaction.guild.get_role(self.staff_role_id)
                if staff_role:
                    embed.add_field(name="Staff Required", value=f"Ping: {staff_role.mention}")

                await ticket_channel.send(embed=embed, view=TicketActions())
                await interaction.user.send(f"Your ticket has been created: {ticket_channel.mention}")

        # Send dropdown menu in the specified channel
        view = View()
        view.add_item(TicketDropdown())
        await channel.send("Please select your issue:", view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
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
                await interaction.response.send_message("Please provide a reason for closing the ticket.", ephemeral=True)

                class ReasonModal(Modal):
                    def __init__(self):
                        super().__init__(title="Close Ticket Reason")
                        self.add_item(TextInput(label="Reason", placeholder="Enter the reason here..."))

                    async def callback(self, interaction: discord.Interaction):
                        reason = self.children[0].value
                        await interaction.response.send_message(f"Ticket closed with reason: {reason}", ephemeral=True)
                        await interaction.user.send(f"Your ticket has been closed with the following reason: {reason}")
                        await interaction.channel.delete()

                await interaction.response.send_modal(ReasonModal())

            elif interaction.data['custom_id'] == 'close_ticket_no_reason':
                if not any(role.id == self.staff_role_id for role in interaction.user.roles):
                    await interaction.response.send_message("You do not have permission to close tickets.", ephemeral=True)
                    return
                await interaction.response.send_message("Your ticket has been closed!", ephemeral=True)
                await interaction.user.send("Your ticket has been closed!")
                await interaction.channel.delete()

class TicketActions(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="Claim", style=discord.ButtonStyle.green, custom_id="claim_ticket"))
        self.add_item(Button(label="Close", style=discord.ButtonStyle.red, custom_id="close_ticket_no_reason"))
        self.add_item(Button(label="Close with Reason", style=discord.ButtonStyle.grey, custom_id="close_ticket"))

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
