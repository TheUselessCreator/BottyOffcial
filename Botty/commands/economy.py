import discord
from discord.ext import commands
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # In-memory storage for user balances
        self.balances = {}

    # Helper function to get a user's balance
    def get_balance(self, user_id):
        return self.balances.get(user_id, 0)

    # Helper function to update a user's balance
    def update_balance(self, user_id, amount):
        if user_id in self.balances:
            self.balances[user_id] += amount
        else:
            self.balances[user_id] = amount

    @commands.command(name='beg')
    async def beg(self, ctx):
        """Chance to receive money by begging."""
        amount = random.randint(1, 100)  # Random amount between 1 and 100
        self.update_balance(ctx.author.id, amount)
        await ctx.send(f"{ctx.author.mention} begged and received ${amount}!")

    @commands.command(name='work')
    async def work(self, ctx):
        """Earn money by working."""
        amount = random.randint(50, 200)  # Random amount between 50 and 200
        self.update_balance(ctx.author.id, amount)
        await ctx.send(f"{ctx.author.mention} worked hard and earned ${amount}!")

    @commands.command(name='steal')
    async def steal(self, ctx, member: discord.Member):
        """Attempt to steal money from another user."""
        if member == ctx.author:
            await ctx.send("You can't steal from yourself!")
            return

        if member.id not in self.balances:
            await ctx.send(f"{member.mention} has no money to steal!")
            return

        amount = random.randint(1, 50)  # Random amount between 1 and 50
        if self.get_balance(member.id) < amount:
            amount = self.get_balance(member.id)  # Steal all money if less than the requested amount
        
        self.update_balance(ctx.author.id, amount)
        self.update_balance(member.id, -amount)
        await ctx.send(f"{ctx.author.mention} attempted to steal and succeeded, stealing ${amount} from {member.mention}!")

    @commands.command(name='check')
    async def check_balance(self, ctx):
        """Check your current balance."""
        balance = self.get_balance(ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, your current balance is ${balance}.")

    @commands.command(name='donate')
    async def donate(self, ctx, member: discord.Member, amount: int):
        """Donate money to another user."""
        if amount <= 0:
            await ctx.send("You must donate a positive amount.")
            return
        
        if self.get_balance(ctx.author.id) < amount:
            await ctx.send("You don't have enough money to donate.")
            return
        
        self.update_balance(ctx.author.id, -amount)
        self.update_balance(member.id, amount)
        await ctx.send(f"{ctx.author.mention} donated ${amount} to {member.mention}!")

async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
