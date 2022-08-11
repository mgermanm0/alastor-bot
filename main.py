from turtle import title
from dotenv import load_dotenv
load_dotenv()

import os
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
from constants import Constants
from music.ytdl import YTDLUtils
from music.musicplayer import MusicPlayer

musicplayer = MusicPlayer()
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
        await ctx.reply("¡Hey! Primero debes de conectarte a un canal de voz")
        return
    await voice.channel.connect()
    await ctx.guild.change_voice_state(channel=voice.channel, self_mute=False, self_deaf=True)
    print("conectado")
    await ctx.reply("¡Dentro!")


def queueHandler(voice, textchannel):
    nextsong = musicplayer.pop(voice.channel.id)
    if nextsong is not None:
        audio = FFmpegPCMAudio(nextsong['formats'][0]['url'], **Constants.FFMPEG_OPTS)
        voice.play(audio)
        embedmsg = discord.Embed(title="Reproduciendo...", url=nextsong['webpage_url'], description=nextsong['title'])
        embedmsg.add_field(name="URL de la canción", value=nextsong['webpage_url'])
        embedmsg.set_thumbnail(url=nextsong['thumbnails'][-1]['url'])
        textchannel.send(embed=embedmsg)
        
@bot.command()
async def play(ctx, *args): 
    song = ' '.join(args)
    
    if ctx.voice_client is None:
        await ctx.reply("No estoy en un canal de voz. Usa `>connect` para entrar en el canal que estés conectado.")
        return
    
    video = YTDLUtils.search(song)
    voice = get(bot.voice_clients, guild=ctx.guild)
    musicplayer.push(voice.channel.id, video)
    
    title="Reproduciendo..."
    if voice.is_playing():
        title="Añadida a cola..."
    else:
        song = musicplayer.pop(voice.channel.id)['formats'][0]['url']
        audio = FFmpegPCMAudio(song, **Constants.FFMPEG_OPTS)
        voice.play(audio, after=lambda e: queueHandler(voice, ctx.channel))
    
    embedmsg = discord.Embed(title=title, url=video['webpage_url'], description=video['title'])
    embedmsg.add_field(name="URL de la canción", value=video['webpage_url'])
    embedmsg.set_thumbnail(url=video['thumbnails'][-1]['url'])
    await ctx.reply(embed=embedmsg)
    
@bot.command()
async def pause(ctx):
    if ctx.voice_client is None:
        await ctx.reply("No estoy en un canal de voz. Usa `>connect` para entrar en el canal que estés conectado y reproducir así música.")
        return
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.pause()
    await ctx.reply("Pausado")

@bot.command()
async def resume(ctx):
    if ctx.voice_client is None:
        await ctx.reply("No estoy en un canal de voz. Usa `>connect` para entrar en el canal que estés conectado y reproducir así música.")
        return
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.resume()
    await ctx.reply("Renaudando reproducción")

@bot.command()
async def queue(ctx):
    if ctx.voice_client is None:
        await ctx.reply("No estoy en un canal de voz. Usa `>connect` para entrar en el canal que estés conectado y reproducir así música.")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    embed = musicplayer.getQueue(voice.channel.id)
    await ctx.reply(embed=embed)

bot.run(os.getenv('TOKEN'))