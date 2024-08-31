import discord
from discord.ext import commands
from discord import app_commands
import random

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.answers = [
            "Yes.",
            "No.",
            "Maybe.",
            "I'm not sure.",
            "Definitely.",
            "Absolutely not.",
            "Ask again later.",
            "It is certain.",
            "I wouldn't count on it.",
            "Yes, but be cautious.",
            "No, but things could change.",
            "Most likely."
        ]

    @app_commands.command(name="8ball", description="Ask the magic 8-ball a yes/no question.")
    @app_commands.describe(question="The question you want to ask the magic 8-ball.")
    async def eightball(self, interaction: discord.Interaction, question: str):
        if not question:
            await interaction.response.send_message("You need to ask a question!")
            return

        answer = random.choice(self.answers)
        await interaction.response.send_message(f"**Question:** {question}\n**Answer:** {answer}")

async def setup(bot):
    await bot.add_cog(EightBall(bot))
