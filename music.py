import discord
from discord import client
from discord.ext import commands
import youtube_dl
import json

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):

        embed = discord.Embed(
            title = (f'Connecting to voice channel. Hi! :wave:'),
            colour = discord.Colour.dark_grey()
        )

        # user not in voice channel
        if ctx.author.voice is None: 
            await ctx.send("You are not connected to a voice channel.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        await ctx.send(embed=embed)
        await update_data('join')

    @commands.command(aliases=['leave'])
    async def disconnect(self, ctx):
        embed = discord.Embed(
            title = (f'Disconnecting from voice channel. See you next time! :wave:'),
            colour = discord.Colour.dark_red()
        )

        await ctx.voice_client.disconnect()
        await ctx.send(embed=embed)
        await update_data('leave')

    @commands.command(aliases=['p'])
    async def play(self, ctx, url, search: str):

        embed = discord.Embed(
            title = (f':musical_note: Now playing: ```{url}```'),
            colour = discord.Colour.dark_gold()
        )

        # copied join command, don't need to run join then play
        if ctx.author.voice is None:    
            await ctx.send("You are not connected to a voice channel.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format':'bestaudio', 'default_search': 'auto'}
        # 'quiet':True
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            print(search)
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            # source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

        await ctx.send(embed=embed)
        await update_data('play')

    @commands.command()
    async def pause(self, ctx):
        embed = discord.Embed(
            title = (f':pause_button: Pausing song now.'),
            colour = discord.Colour.dark_teal()
        )

        ctx.voice_client.pause()
        await ctx.send(embed=embed)

        await update_data('pause')

    @commands.command()
    async def resume(self, ctx):
        embed = discord.Embed(
            title = (f':play_pause: Resuming song now.'),
            colour = discord.Colour.dark_green()
        )

        ctx.voice_client.resume()
        await ctx.send(embed=embed)

        await update_data('resume')

def setup(client):
    client.add_cog(music(client))

async def update_data(cmd):
        '''
        update_data - updates stats.json file when command is used -> copied from bot.py
        '''
        #print(f'updating data for cmd: {cmd}...')
        with open("stats.json", "r") as f:
            stats = json.load(f)

            stats[cmd] += 1
            stats['total'] += 1

            with open("stats.json", "w") as f:
                json.dump(stats, f)

            #print(f'data has been updated for cmd {cmd}!')




