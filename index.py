#!/usr/bin/python3

from telethon import TelegramClient
import configparser # CONFIGS
import os
from tqdm import tqdm # Barra de Progreso
import time

config = configparser.ConfigParser()
config_leer = config.read('credentials.conf')

if config_leer:
    try:
        api_id = config.get('creds', 'api_id')
        api_hash = config.get('creds', 'api_hash')
    except (configparser.NoSectionError, configparser.NoOptionError):
        print("\n[-] Error: La sección o las opciones no existen en el archivo 'credentials.conf'.\n")
else:
    print("\n[-] credentials.conf doesn't exists....\n")
    time.sleep(1)
    print("\n If you don't know to how to obtain your api_id & api_hash pls obtain more info here: Log in to your Telegram core: https://my.telegram.org. Go to 'API development tools' and fill out the form. You will get basic addresses as well as the api_id and api_hash parameters required for user authorization.")
    api_id_request = input("\nWhich your api_id?: ")
    api_hash_request = input("Which your api_hash?: ")
    telephone_request = input("Which phone number do you have on you account (Necessary for the SMS Code) (Ex. Country Code + Number -> +34644382914): ")
    syntax = f"""[creds]
api_id = {api_id_request}
api_hash = {api_hash_request}
telefono = {telephone_request}
    """

    api_id = api_id_request
    api_hash = api_hash_request

    try:
        with open('credentials.conf', 'w') as credenciales:
            credenciales.write(syntax)
    except:
        print("[-] Some error ocurred on the creation of the configuration files.")
        exit(0)


channel_username = input("From which channel do you want to obtain the media? (Ex. elhackerdotnet): ")

descargas = 'downloads'

session_name = str(api_id)

client = TelegramClient(session_name, api_id, api_hash)

limite_descargas = int(input("How many new messages do you want to download? (Ex. 10): "))

async def barra_de_progreso(current, total):
    """Callback para mostrar la barra de progreso."""
    bar.update(current - bar.n)


async def download_media_with_progress(message):
    full_path = os.path.join(descargas, channel_username)

    if not os.path.exists(descargas):
        os.makedirs(descargas)
    
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    if message.document:
        file_name = message.file.name or f"{message.id}"
        file_ext = os.path.splitext(file_name)[1]  # Obtener la extension del archivo
        file_path = os.path.join(full_path, f"{message.id}{file_ext}")
    else:
        file_path = os.path.join(descargas, f"{message.id}.media")

    # Crear barra de progreso
    global bar
    bar = tqdm(total=message.file.size if message.file else 100, unit="B", unit_scale=True)

    saved_path = await client.download_media(message.media, file=file_path, progress_callback=barra_de_progreso)

    bar.close()

    print(f"Archivo descargado en: {saved_path}")

async def main():

    await client.start()
    async for message in client.iter_messages(channel_username, limit=limite_descargas):
            if message.media:
                await download_media_with_progress(message)


# Ejecutar el cliente
with client:
    client.loop.run_until_complete(main())


""" EN CASO DE QUERER QUE EL PROGRAMA SE EJECUTE EN TIEMPO REAL.
while True:
    async for message in client.iter_messages(channel_username, limit=limite_descargas):
        if message.date > tate and message.media:
            await download_media_with_progress(message)
    await asyncio.sleep(60) # Esperar 60 segundos para ver si hay algo nuevo
"""