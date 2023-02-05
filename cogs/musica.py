import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
from settings import *
from youtube_search import YoutubeSearch
import asyncio

listaServidores = {}
songQueue = []
loop = False
songIndex = 0
songInfo = {}

def pararSom(ctx):
    try:
        ctx.voice_client.stop()
    except:
        pass

#utiliza a library youtube_search para procurar o primeiro vídeo correspondente aos argumentos de pesquisa
#retorna todas as informações sobre o vídeo (url, título, views, etc)
async def searchSong(args):
    ytb_search = ' '.join(args)
    results = YoutubeSearch(ytb_search, max_results=1).to_dict()
    songInfo = results[0]
    return songInfo


#formata o embed que será exibido para o vídeo solicitado, tendo como base as informações do mesmo
async def videoEmbed(songInfo, self, ctx):
    embed = discord.Embed(title="Tocando agora:", color=0xF7FE2E)
    embed.add_field(name="Nome:", value=f"[{songInfo['title']}](https://www.youtube.com{songInfo['url_suffix']})", inline=True)
    embed.add_field(name="Duraçao:", value="`[0:00 /{}]`".format(songInfo['duration']), inline=True)
    embed.add_field(name="Solicitado por:", value=ctx.message.author.mention, inline=False)
    #embed.add_field(name="Visualizações:", value="`{}`".format(songInfo['views']), inline=True)
    thumbnailURL = songInfo['thumbnails']
    embed.set_thumbnail(url=f"{thumbnailURL[0]}.jpeg")
    return embed


async def queueSong(self, ctx, songInfo):
    try:
        embed = await videoEmbed(songInfo, self, ctx)
        await ctx.send(embed=embed)
        songQueue.append(songInfo)
    except:
        return await ctx.send("Vídeo não encontrado! Tente novamente!")


async def startSong(self, ctx, songIndex, songInfo):
    vc = ctx.voice_client
    YDL_OPTIONS = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    url = f"https://www.youtube.com{songInfo['url_suffix']}"

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(executable=os.path.join(FFMPEG_DIR, "ffmpeg.exe"), source=url2, **FFMPEG_OPTIONS)
        vc.play(source, after = lambda e: asyncio.run(nextSong(self, ctx, songIndex, songInfo)))


async def nextSong(self, ctx, songIndex, songInfo):
    # Quando terminar a música, se não estiver em loop, remove a música da lista
    if loop == False:
        songQueue.pop(0)
        # Se ainda houverem músicas na playlist, toca a próxima
        if len(songQueue) > 0:
            songInfo = songQueue[0]
            await startSong(self, ctx, songIndex, songInfo)
        # Se não houverem músicas na playlist, se disconecta do canal de voz
        else:
            pass
    # Se estiver em loop, toca a próxima música. Se chegar no final, volta do início
    else:
        songIndex += 1
        if songIndex >= len(songQueue):
            songIndex=0
            songInfo = songQueue[songIndex]
            await startSong(self, ctx, songIndex, songInfo)
        else:
            songInfo = songQueue[songIndex]
            await startSong(self, ctx, songIndex, songInfo)


async def playSong(self, ctx, args):
    songInfo = await searchSong(args)
    await queueSong(self, ctx, songInfo)

    #Verificar se já está tocando algo, se não estiver, tocar o primeiro item da lista.
    if ctx.voice_client.is_playing() == False:
        songIndex = 0
        await startSong(self, ctx, songIndex, songInfo)


class musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #conecta o bot ao canal de voz e solicita que o vídeo seja tocado, enviando os argumentos digitados
    @commands.command(brief="Tocar música", description="Se conecta ao canal de voz do usuário e toca a música desejada")
    async def play(self, ctx, *args):
        if ctx.message.author.voice == None:
            await ctx.send("Você não está conectado a um canal de voz! Conecte-se antes de tentar novamente!")
        else:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
                await playSong(self, ctx, args)
            else:
                voice = await channel.connect()
                await ctx.send("Me conectei a um canal de voz!")
                await playSong(self, ctx, args)

    #pausa o som do bot
    @commands.command(brief="Pausar música", description="Pausa a música do bot")
    async def pause(self, ctx):
        if ctx.voice_client.is_paused() == False:
            ctx.voice_client.pause()
            await ctx.send(":pause_button:  Suas músicas foram pausadas!  :pause_button:")
        else:
            ctx.voice_client.resume()
            await ctx.send(":play_pause:  Suas músicas foram retomadas!  :play_pause:")

    #retoma o som do bot
    @commands.command(brief="Despausar música", description="Despausa a música do bot")
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send(":play_pause:  Suas músicas foram retomadas!  :play_pause:")

    #desconecta o bot do canal de voz
    @commands.command(brief="Parar música e desconectar bot", description="Para a música e desconecta o bot do canal de voz")
    async def stop(self, ctx):
        ctx.voice_client.stop()
        channel = ctx.message.guild.voice_client
        if channel is not None:
            await channel.disconnect()
            await ctx.send("Me desconectei do canal de voz!")
        else:
            await ctx.send("O bot não está conectado a um canal de voz!")

    @commands.command(brief="Aciona o loop", description="Coloca a lista de reprodução em loop")
    async def loop(self, ctx):
        global loop
        if loop == False:
            loop = True
            await ctx.send("Comando de loop ativado!")
        else:
            loop = False
            await ctx.send("Comando de loop desativado!")

    @commands.command(brief="Skip", description="Skip a lista de reprodução")
    async def skip(self, ctx):
        global songIndex
        global songQueue
        global loop

        if loop == False:
            if len(songQueue) == 0:
                await ctx.send("Sua lista de reprodução está vazia!!")
                pararSom(ctx)
            else:
                pararSom(ctx)
                await nextSong(self, ctx, songIndex, songInfo)
        else:
            await ctx.send("Não é possível usar esse comando em modo de loop!!")

def setup(bot):
    bot.add_cog(musica(bot))
