from discord.ext import commands

class convite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Convite para o servidor', description='Gera um convite para entrar no servidor e o envia como mensagem')
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age="0")
        await ctx.send(link)

def setup(bot):
    bot.add_cog(convite(bot))
