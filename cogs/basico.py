from discord.ext import commands


class Basicos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        await ctx.send(':rotating_light: :rotating_light:  Erro detectado!!  :rotating_light: :rotating_light:')
        await ctx.send("Por favor cheque como utilizar o comando corretamente digitando =help. Em caso de dúvida, entre em contato com o administrador.")

    @commands.command(brief='Nome de usuário no jogo', description='Recebe e interpreta um username especificado pelo usuário')
    async def username(self, ctx, *args):
        ## se não houverem argumentos, ou seja, o usuário digitar apenas "=username", retorna uma mensagem de erro
        if len(args) == 0:
            await ctx.send('Algo deu errado! Tente novamente!')
        ## se houver um ou mais argumentos, concatena eles com espaços (' '.join(args))
        else:
            username = ' '.join(args)
            await ctx.send('Seu nick é "{}"'.format(username))

    @commands.command(aliases=['clear','limpar'], brief='Apaga mensagens recentes', description='Deleta a quantidade de mensagens especificada')
    async def clean(self, ctx, arg):
        ## O comando "purge()" é utlizado para deletar as mensagens e possui um limite igual ao argumento fornecido mais um
        await ctx.channel.purge(limit=int(arg) + 1)

def setup(bot):
    bot.add_cog(Basicos(bot))
