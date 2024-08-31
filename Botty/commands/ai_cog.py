import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import difflib
import sympy as sp  # Import sympy for math evaluation

# Load environment variables from .env file
load_dotenv()

class AIResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.qa_pairs = {}
        self.load_qa_pairs()

    def load_qa_pairs(self):
        """Load question-answer pairs from the questions.txt file."""
        try:
            with open('./assets/questions.txt', 'r') as file:
                for line in file:
                    if '=' in line:
                        question, answer = line.strip().split('=', 1)
                        self.qa_pairs[question.strip().lower()] = answer.strip()
            print(f"Loaded {len(self.qa_pairs)} QA pairs.")
        except FileNotFoundError:
            print("questions.txt file not found. Please make sure it exists.")
        except Exception as e:
            print(f"An error occurred while loading QA pairs: {e}")

    def find_best_match(self, user_question):
        """Find the closest matching question from the QA pairs."""
        question_list = list(self.qa_pairs.keys())
        matches = difflib.get_close_matches(user_question, question_list, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        return None

    def is_math_expression(self, expression):
        """Check if the expression is a valid math expression."""
        try:
            # Try to parse the expression
            parsed_expr = sp.sympify(expression, evaluate=False)
            # Check if it evaluates to a number
            return parsed_expr.is_real
        except:
            return False

    @app_commands.command(name='ai', description='Ask the AI a question')
    async def ai(self, interaction: discord.Interaction, question: str):
        """Respond to a question asked to the AI."""
        question = question.strip().lower()

        # Try to find the closest matching question
        best_match = self.find_best_match(question)
        if best_match:
            answer = self.qa_pairs[best_match]
        else:
            answer = "I don't know the answer to that question."

        await interaction.response.send_message(answer)

    @app_commands.command(name='teach-ai', description='Teach the AI a new question-answer pair')
    async def teach_ai(self, interaction: discord.Interaction, question: str, answer: str):
        """Add a new question-answer pair to the AI's knowledge."""
        question = question.strip()
        answer = answer.strip()

        if not question or not answer:
            await interaction.response.send_message("Both question and answer must be provided.")
            return

        # Check if the question already exists
        if question.lower() in self.qa_pairs:
            await interaction.response.send_message("This question is already known.")
            return

        # Check if the answer is a valid math expression
        if self.is_math_expression(answer):
            try:
                with open('./assets/questions.txt', 'a') as file:
                    file.write(f"{question} = {answer}\n")
                # Update the in-memory QA pairs
                self.qa_pairs[question.lower()] = answer
                await interaction.response.send_message("AI has been taught a new question-answer pair.")
            except Exception as e:
                await interaction.response.send_message("An error occurred while teaching the AI.")
                print(f"An error occurred while saving the QA pair: {e}")
        else:
            await interaction.response.send_message("The answer is not a valid math expression.")

async def setup(bot: commands.Bot):
    await bot.add_cog(AIResponder(bot))
