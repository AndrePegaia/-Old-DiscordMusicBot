import os

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
FFMPEG_DIR = os.path.join(ROOT_DIR, 'ffmpeg')


# Define a variável do token do bot como a variável do arquivo .env, caso contrário retorna falso
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", False)