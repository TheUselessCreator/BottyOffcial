import discord
from discord.ext import commands
from discord import app_commands

class DropdownMenu(discord.ui.Select):
    def __init__(self):
        # Define the dropdown options for categories
        options = [
            discord.SelectOption(label="AdminCommands", description="Admin commands for managing the server"),
            discord.SelectOption(label="HelpfulCommands", description="Helpful commands to assist users"),
            discord.SelectOption(label="OwnerCommands", description="Commands exclusive to the server owner"),
            discord.SelectOption(label="AntiManagers", description="Commands for anti-management and moderation"),
            discord.SelectOption(label="CommunityCommands", description="Fun and interactive community commands"),
        ]
        super().__init__(placeholder="Select a Command Category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Define command sets for each category based on the user's selection
        command_sets = {
            "AdminCommands": [
                "add_remove_role", "announce", "ban", "clearmessages", "giveaway", "joinrole", "kick", "lockdown_channel",
                "lockdown_server", "logger", "mute", "new_nick", "pauseinvites", "share", "slowmode", "unban", "unmute", 
                "unpauseinvites", "warn"
            ],
            "HelpfulCommands": [
                "about", "help_command", "report", "serverinfo"
            ],
            "OwnerCommands": [
                "LS", "ownergive", "serverlist", "shutdown"
            ],
            "AntiManagers": [
                "anticaps", "antiemoji", "antiraidmanage", "linksmanager", "spammanage"
            ],
            "CommunityCommands": [
                "8ball", "Picross", "avatar", "coinflip", "define", "echo", "fact", "funfont", "github", "guess", "interact",
                "invite", "joke", "luck", "membercount", "meme", "ping", "question", "remind", "rolescount", "roll", "rps", 
                "time", "translate", "weather", "website", "whois"
            ]
        }

        # Respond with the commands for the selected category by editing the embed
        selected_category = self.values[0]
        commands_list = "\n".join([f"/{cmd}" for cmd in command_sets[selected_category]])

        # Create an updated embed with the selected category's commands
        embed = discord.Embed(title=f"{selected_category} Commands", description=f"**Available Commands:**\n{commands_list}", color=discord.Color.blue())
        embed.set_thumbnail(url=interaction.guild.me.display_avatar.url)  # Use bot's profile picture as thumbnail

        await interaction.message.edit(embed=embed)  # Edit the original message's embed

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropdownMenu())

class HelpCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Get a list of categorized commands.")
    async def help_command(self, interaction: discord.Interaction):
        # Create an initial embed with instructions
        embed = discord.Embed(title="Botty Extra Help", description="Choose a category to get started!", color=discord.Color.green())
        embed.set_thumbnail(url=interaction.guild.me.display_avatar.url)  # Use bot's profile picture as thumbnail

        # Send the initial embed with the dropdown menu
        await interaction.response.send_message(embed=embed, view=DropdownView())

async def setup(bot):
    await bot.add_cog(HelpCommandCog(bot))
