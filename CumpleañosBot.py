import os

from discord.ext import tasks
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import time

bot = commands.Bot("!")
load_dotenv()

target_channel_id = os.getenv("CHANNEL_ID")

@tasks.loop(minutes=30.0)
async def birthday_check():
    now = datetime.now()
    #Checa todos los dias a las 8
    if now.hour != 8:
        print(f"[{now}]: not 8, skipping check")
        return

    message_channel = bot.get_channel(int(target_channel_id))
    print(f"[{now}]: Got channel {message_channel}")

    #Abre el bday text que usa el formato: dd-MonthName Name
    bday_file = open("./birthdays.txt")
    today = time.strftime("%d-%B")

    for bday in bday_file:
        if today in bday:
            #Si hay cumpleaños, lo manda al discord
            print(bday)
            name = bday.split(" ")[1]
            await message_channel.send(f"@everyone Hoy es cumpleaños de: {name}")


@birthday_check.before_loop
async def before():
    await bot.wait_until_ready()
    print("Iniciando")

birthday_check.start()
#runs bot
bot.run(os.getenv("TOKEN"))
