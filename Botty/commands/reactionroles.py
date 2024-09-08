import discord
from discord.ext import commands
from discord import app_commands

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_roles = {}  # Dictionary to store reaction roles

    @app_commands.command(name="reactionrole", description="Set up a reaction role in an embed")
    @app_commands.describe(role="The role to assign when a reaction is added", emoji="The emoji to react with", message="The message to display in the embed")
    async def reaction_role(self, interaction: discord.Interaction, role: discord.Role, emoji: str, message: str):
        """Set up a reaction role with a specific emoji."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        # Create an embed with the provided message
        embed = discord.Embed(
            title="Reaction Role",
            description=message,
            color=discord.Color.blue()
        )
        embed.set_footer(text="React to this message with the specified emoji to get the role.")

        # Send the embed and add the reaction
        msg = await interaction.channel.send(embed=embed)
        await msg.add_reaction(emoji)

        # Save the message ID, role, and emoji for future reference
        self.reaction_roles[msg.id] = {'role': role, 'emoji': emoji}

        await interaction.response.send_message(f"Reaction role set! React with {emoji} to get the {role.name} role.", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Assign the role when the user reacts with the specified emoji."""
        if payload.message_id in self.reaction_roles:
            guild = self.bot.get_guild(payload.guild_id)
            role_info = self.reaction_roles[payload.message_id]
            role = role_info['role']

            if str(payload.emoji) == role_info['emoji']:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Remove the role when the user removes the reaction."""
        if payload.message_id in self.reaction_roles:
            guild = self.bot.get_guild(payload.guild_id)
            role_info = self.reaction_roles[payload.message_id]
            role = role_info['role']

            if str(payload.emoji) == role_info['emoji']:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.remove_roles(role)

async def setup(bot: commands.Bot):
    await bot.add_cog(ReactionRole(bot))
