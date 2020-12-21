import os
import random
from time import sleep

import discord
from discord.ext import commands

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='--')

@bot.command()
async def join(ctx):
    try:
        channel = ctx.author.voice.channel
        return await channel.connect()
    except Exception as e:
        print("join", e)

@bot.command()
async def leave(ctx):
    try:
        for vc in bot.voice_clients:
            await vc.disconnect()
    except Exception as e:
        print("leave", e)

@bot.command()
async def dime(ctx, *arg):
    try:
        bot_voice = bot.voice_clients
        voice = bot_voice[0] if bot_voice else await join(ctx)
        if voice != None:
            audio = None
            available = {i: j for i, j in enumerate(os.listdir("assets"))}
            if arg:
                if arg[0].isnumeric() and int(arg[0]) < len(available):
                    audio = f"{available[int(arg[0])]}"
                if f"{arg[0]}.mp3" in available.values():
                    audio = f"{arg[0]}.mp3"
            else:
                audio = random.choice(available)

            if audio:
                voice.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=f"assets/{audio}"))
                while voice.is_playing():
                    sleep(.1)
            else:
                await ctx.send("No tengo ese registro mi bro :(")
        else:
            await ctx.send("Conectate a un canal sipo :)")
    except Exception as e:
        print("dime", e)

@bot.command()
async def joyitas(ctx):
    try:
        msg = "Tengo estas joyitas para ti:\n"
        available = os.listdir("assets")
        for i, name in enumerate(available):
            msg += f" {i}. {name[:-4]}\n"
        await ctx.send(msg)
    except Exception as e:
        print("joyitas", e)

@bot.command()
async def compañia(ctx, arg):
    try:
        if arg:
            arg = int(arg)
        else:
            arg = 6

        for _ in range(max(6, arg)):
            await dime(ctx)
    except Exception as e:
        print("compañia", e)


if __name__ == "__main__":
    
    bot.run(TOKEN)
