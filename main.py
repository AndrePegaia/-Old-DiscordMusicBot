import os

from discord.ext import commands

# importar todas configurações do script settings
from settings import *

# definir bot com comandos de prefixo "="
bot = commands.Bot(command_prefix="=")

# receber mensagem local ao inicializar o bot corretamente
@bot.event
async def on_ready():
    # Ao inicializar exibe no prompt um texto e o nome de usuário do bot no discord
    print('Logged on as {0}!'.format(bot.user))

# carregar todos os cogs (conjuntos de comandos) da pasta "cogs"
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

# inicializar bot através de token encontrado em arquivo .env a parte
# para isso utiliza as configurações do script settings
bot.run(DISCORD_BOT_TOKEN)