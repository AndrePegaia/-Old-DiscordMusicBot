from discord.ext import commands
import aiohttp
import discord

class imagens(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat//meow") as r:
                    data = await r.json()
                    embed = discord.Embed(title="Gatinhos Fofinhos")
                    embed.set_image(url=data['file'])
                    embed.set_footer(text="random.cat")
                    await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()
                    if data['url'].endswith(".mp4"):
                        embed = discord.Embed(title="Cachorros Fofinhos", description=data['url'])
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title="Cachorros Fofinhos")
                        embed.set_image(url=data['url'])
                        embed.set_footer(text="random.dog")
                        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(imagens(bot))