import os

#Descobrir se o ambiente em que o código está sendo executado é de desenvolvimento ou produção
#Para isso, utiliza o método getenv para descobrir se DEBUG é verdadeiro, caso contrário retorna falso
DEBUG = os.getenv("DEBUG", False)

#Se estiver no ambiente de desenvolvimento importa os arquivos de desenvolvimento
if DEBUG:
    print("We are in Debug")
    #Importar o arquivo do tipo ".env" que contém o token do bot para o ambiente de desenvolvimento
    from pathlib import Path
    from dotenv import load_dotenv
    env_path = Path(".") / ".env.debug"
    load_dotenv(dotenv_path=env_path)
    #Importar o script de configurações específicas de desenvolvimento
    from settings_files.development import *

#Se estiver no ambiente de produção importa os arquivos de produção
else:
    print("We are in Production")
    # Importar o arquivo do tipo ".env" que contém o token do bot para o ambiente de produção
    from pathlib import Path
    from dotenv import load_dotenv
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    # Importar o script de configurações específicas de produção
    from settings_files.production import *