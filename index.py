from telethon import TelegramClient, events
import configparser # CONFIGS
import os


config = configparser.ConfigParser()
config.read('credentials.conf')

api_id = config.get('creds', 'api_id')
api_hash = config.get('creds', 'api_hash')
channel_username = config.get('creds', 'channel_username')

descargas = 'descargado'

session_name = str(api_id)

client = TelegramClient(session_name, api_id, api_hash)


async def main():

    await client.start()

    # AUTENTICACION
    if not await client.is_user_authorized():
        print("Usuario no autorizado. Necesita iniciar sesión.")
        await client.send_code_request(config.get('creds', 'telefono'))
        code = input('Introduce el código que te llegó por SMS: ')
        await client.sign_in(config.get('creds', 'telefono'), code)


    async for message in client.iter_messages(channel_username, limit=2): # limit para los ultimos mensajes
        if message.media:  # Filtrar por contenido
            file_path = os.path.join(descargas, f"{message.id}.media")
            saved_path = await client.download_media(message.media, file=file_path)
            print(f"Archivo descargado en: {saved_path}")
            break 


# Ejecutar el cliente
with client:
    client.loop.run_until_complete(main())