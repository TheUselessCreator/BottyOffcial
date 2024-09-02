import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='extrahelp', description="Get extra help with Botty commands")
    async def extrahelp(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Botty Extra Help",
            description="Explore all the extra commands Botty offers. If you need assistance, join the support server.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)

        # First row - Moderation and Fun Commands (side by side)
        embed.add_field(
            name="🛠️ **Moderation Commands**", 
            value="""
            🔨 `/kick` - Kick a user
            🛑 `/ban` - Ban a user
            🤐 `/mute` - Mute a user
            🔓 `/unmute` - Unmute a user
            ⚠️ `/warn` - Warn a user
            🔒 `/lockdown_channel` - Lockdown a specific channel
            🔒 `/lockdown_server` - Lockdown the entire server
            🐢 `/slowmode` - Set slowmode for a channel
            ⏸️ `/pauseinvites` - Pause all invites
            ▶️ `/unpauseinvites` - Unpause invites
            """, 
            inline=True  # Inline for side by side
        )

        embed.add_field(
            name="🎮 **Fun Commands**", 
            value="""
            🎱 `/8ball` - Ask the magic 8ball a question
            🪙 `/coinflip` - Flip a coin
            😂 `/joke` - Get a random joke
            🖼️ `/meme` - Fetch a random meme
            🎲 `/guess` - Play a guessing game
            ✊ `/rps` - Rock, Paper, Scissors game
            🎲 `/roll` - Roll a dice
            🍀 `/luck` - Test your luck
            """, 
            inline=True  # Inline for side by side
        )

        # Second row - Utility and Info Commands (side by side)
        embed.add_field(
            name="📚 **Utility Commands**", 
            value="""
            🏓 `/ping` - Check the bot's ping
            🏠 `/serverinfo` - Get information about the server
            👤 `/whois` - Get information about a user
            🔗 `/invite` - Get the bot's invite link
            📊 `/status` - Check the bot's status
            🌦️ `/weather` - Get the current weather
            ⏰ `/time` - Get the current time
            🌍 `/translate` - Translate text
            📝 `/define` - Define a word
            """, 
            inline=True  # Inline for side by side
        )

        embed.add_field(
            name="💻 **Info Commands**", 
            value="""
            ℹ️ `/about` - Information about Botty
            👤 `/avatar` - Get a user's avatar
            💻 `/github` - Bot's GitHub link
            🌐 `/website` - Visit the bot's website
            📚 `/fact` - Get a random fact
            ⏰ `/remind` - Set a reminder
            ✉️ `/share` - Share something with the server
            """, 
            inline=False  # Inline for side by side
        )

        # Third row - AI and Interaction Commands (centered since it's one section)
        embed.add_field(
            name="🤖 **AI & Interaction Commands**", 
            value="""
            🤖 `/ai` - Ask Botty an AI-based question
            🧠 `/teach-ai` - Teach Botty something new
            ❓ `/question` - Ask a question
            💬 `/interact` - Interact with Botty
            """, 
            inline=False  # No inline, this will be full width
        )

        # Set an image or footer if needed
        embed.set_image(url="https://your-image-url.com/image.gif")
        embed.set_footer(text="Need more help? Join the support server below!")

        # Add buttons with a view
        view = discord.ui.View()
        support_button = discord.ui.Button(
            label="Support Server",
            url="https://your-support-server-link.com",
            style=discord.ButtonStyle.link
        )
        view.add_item(support_button)

        invite_button = discord.ui.Button(
            label="Invite Botty",
            url="https://your-bot-invite-link.com",
            style=discord.ButtonStyle.link
        )
        view.add_item(invite_button)

        vote_button = discord.ui.Button(
            label="Vote for Botty",
            url="https://your-bot-vote-link.com",
            style=discord.ButtonStyle.link
        )
        view.add_item(vote_button)

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
