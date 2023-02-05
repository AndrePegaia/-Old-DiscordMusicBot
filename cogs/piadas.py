import discord
from discord.ext import commands
import json
import os
import random
from settings import *

async def get_momma_jokes():
    with open(os.path.join(DATA_DIR, "momJokes.json"), encoding="utf8") as joke_file:
        jokes = json.load(joke_file)
    random_category = random.choice(list(jokes.keys()))
    insult = random.choice(list(jokes[random_category]))
    return insult

class piadas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['piada','joke','piadaMãe'], brief="Piadas de mães", description="Retorna uma piada aleatória de mãe")
    async def momJoke(self, ctx, member: discord.Member = None):
        insult = await get_momma_jokes()
        if member is not None:
            await ctx.send(f"That's for you {member.name} \n{insult}")
        else:
            await ctx.send(insult)


def setup(bot):
    bot.add_cog(piadas(bot))