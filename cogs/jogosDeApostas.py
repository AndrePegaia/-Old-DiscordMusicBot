from discord.ext import commands
import random

class jogosDeApostas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Número aleatório de 1 a 100', description='Gera um número aleatório de 1 a 100')
    async def random(self, ctx):
        n = random.randrange(1, 101)
        await ctx.send(n)

    @commands.command(aliases=['dado'], brief='Joga um dado da quantidade de lados especificada', description='Gera um número aleatório de 1 a n, onde n é a quantidade especificada pelo argumento')
    async def dice(self, ctx, *args):
        if not args:
            n = random.randrange(1, 6)
            await ctx.send(n)
        elif len(args) == 1:
            if args[0].isnumeric() and args[0] != "0":
                nLados = int(args[0])
                n = random.randrange(1, nLados)
                await ctx.send(n)
            else:
                await ctx.send('Insira um número de lados válido')
        else:
            await ctx.send('Insira um único argumento a frente do comando')

    @commands.command(aliases=['moeda'], brief='Joga cara ou coroa', description='Gera um número aleatório de 0 a 1 e define o resultado como cara ou coroa')
    async def coin(self, ctx):
        n = random.randint(0, 1)
        await ctx.send("Cara" if n==1 else "Coroa")

def setup(bot):
    bot.add_cog(jogosDeApostas(bot))
