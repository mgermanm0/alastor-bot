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
    vc = await voice.channel.connect()
    await ctx.guild.change_voice_state(channel=voice.channel, self_mute=False, self_deaf=True)
    print("conectado")
    await ctx.reply("¡Dentro!")


@bot.command()
async def play(ctx, *args):
    song = ' '.join(args)
    if ctx.voice_client is None:
        await ctx.reply("No estoy en un canal de voz. Usa `>connect` para entrar en el canal que estés conectado.")
        return
    
    video, src = YTDLUtils.search(song)
    voice = get(bot.voice_clients, guild=ctx.guild)

    audio = FFmpegPCMAudio(src ,**Constants.FFMPEG_OPTS)
    voice.play(audio)
    embedmsg = discord.Embed(title="Reproduciendo...", url=video['webpage_url'], description=video['title'])
    embedmsg.add_field(name="URL de la canción", value=video['webpage_url'])
    embedmsg.set_thumbnail(url=video['thumbnails'][-1]['url'])
    await ctx.reply(embed=embedmsg) 
    
bot.run(os.getenv('TOKEN'))