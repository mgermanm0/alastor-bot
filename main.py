# This example requires the 'members' privileged intents

import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import requests
bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print('Sesión iniciada')
    print(bot.user)
    print('------')

@bot.command()
async def connect(ctx):
    voice = ctx.author.voice
    if not voice:
        await ctx.reply("Subnormal conectate a un canal de voz xd")
        return
    vc = await voice.channel.connect()
    await ctx.guild.change_voice_state(channel=voice.channel, self_mute=False, self_deaf=True)
    print("conectado")
    await ctx.reply("oleeee ya estoy")
    
def search(query):
    with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
        try: 
            requests.get(query)
        except: # Ocurre un error
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        else: # No ocurre ningún error
            info = ydl.extract_info(query, download=False)
            
    return (info, info['formats'][0]['url'])

@bot.command()
async def play(ctx, *args):
    song = ' '.join(args)
    if ctx.voice_client is None:
        await ctx.reply("no crees que para cantar primero debes de meterme en un canal de voz? xd")
        
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    video, src = search(song)
    voice = get(bot.voice_clients, guild=ctx.guild)

    audio = FFmpegPCMAudio(src ,**FFMPEG_OPTS)
    voice.play(audio)
    await ctx.reply("Reproduciendo esto: " + video['title'] + "\n" + video['webpage_url'])
    
bot.run('TU TOKEN AQUI')