import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class Question(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "https://opentdb.com/api.php?amount=1&type=multiple"

    @app_commands.command(name='question', description='Get a trivia challenge question.')
    async def question(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        question = data['results'][0]['question']
                        correct_answer = data['results'][0]['correct_answer']
                        incorrect_answers = data['results'][0]['incorrect_answers']
                        answers = incorrect_answers + [correct_answer]
                        answers.sort()  # Shuffle answers
                        embed = discord.Embed(title="Trivia Question", description=question, color=discord.Color.blue())
                        for i, answer in enumerate(answers, start=1):
                            embed.add_field(name=f"Option {i}", value=answer, inline=False)
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message("Failed to fetch the question. Please try again later.")
            except Exception as e:
                await interaction.response.send_message(f"An error occurred: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Question(bot))
