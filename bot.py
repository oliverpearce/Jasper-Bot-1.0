# =============================================================
# This project was created on 4/3/2020, last edited 9/22/2021
# Created by Oliver Pearce AKA Silver Tateyama
# Using Discord.py 1.7.3 (rewrite) and Python 3.8.1 on Mac
# =============================================================

import discord
from discord.ext import commands, tasks
import platform
import random
import json
from itertools import cycle
import os
import music

def main():

    intents = discord.Intents.default()
    intents.members = True

    client = commands.Bot(command_prefix = "~", owner_id = 314922756628152322, intents=intents)
    status = cycle(['Corona bad >:c', '~helper', '~info'])
    TOKEN = os.environ.get("BOT_TOKEN")

    cogs = [music]

    for i in range(len(cogs)):
        cogs[i].setup(client)

    # =============================================================
    # BASIC SET-UP STUFF
    # =============================================================

    @client.event
    async def on_ready():
        '''
        on_ready - prints message when bot is ready
        '''
        #await client.change_presence(activity=discord.Game(name='Corona bad >:c'))
        change_status.start()
        print("bot is online and ready :O")

    @tasks.loop(seconds = 30)
    async def change_status():
        await client.change_presence(activity=discord.Game(next(status)))

    @client.event
    async def on_member_join(member):
        '''
        member_joins - prints when a member joins the server
        '''
        print(f'{member} has joined a server. This bot is so cool!!')

    @client.event
    async def on_member_remove(member):
        '''
        member_leaves - prints when a member leaves the server
        '''
        print(f'{member} has left a server. cy@')

    # =============================================================
    # TEXT CHANNEL STUFF - COMMANDS
    # =============================================================

    @client.command()
    async def ping(ctx):
        '''
        ~ping - writes message on discord when prompted
        '''
        embed = discord.Embed(
            title = (f'Pong! {round(client.latency * 1000)}ms :partying_face:'),
            colour = discord.Colour.blurple()
        )
        await ctx.send(embed=embed)
        await update_data('ping')

    @client.command()
    async def info(ctx):
        '''
        ~info - writes an embed on discord as a help message
        '''
        embed = discord.Embed(
            title = 'Welcome to Jasper Bot 1.0!',
            description = 'This bot is just for messing around and made entirely by Silver. \nNamed after my S.O. :D',
            colour = discord.Colour.blue()
        )

        embed.set_footer(text='invite link: https://tinyurl.com/jasper-bot')
       # embed.set_image(url='https://cdn.discordapp.com/avatars/314922756628152322/d18c19c2c70c1991e0ebbea5ee5d029b.png')
        embed.set_thumbnail(url='https://i1.sndcdn.com/artworks-000215600087-h47tpo-t500x500.jpg')
        embed.set_author(name='Silver Tateyama',
        icon_url='https://i.imgur.com/vZeGPHq.jpg')
        #https://cdn.discordapp.com/aavatars/314922756628152322/d18c19c2c70c1991e0ebbea5ee5d029b.png
        embed.add_field(name='Need help?', value="Use the ~helper command to learn more!", inline=False)

        await ctx.send(embed=embed)
        await update_data('info')

    @client.command()
    async def echo(ctx, *, message=None):
        '''
        ~echo - echoes a user message
        '''
        message = message or "Please enter message to be echoed."
        await ctx.message.delete()
        await ctx.send(message)
        await update_data('echo')

    @client.command(name='hi')
    async def _hi(ctx):
        '''
        ~hi - says hi to the user in an embed
        '''
        embed = discord.Embed(
            title = (f'Hi {ctx.author.name}! :stuck_out_tongue_closed_eyes: '),
            colour = discord.Colour.dark_magenta()
        )

        await ctx.send(embed=embed)
        await update_data('hi')

    @client.command()
    async def stats(ctx):
        '''
        ~stats - Sends an embed with the bot's stats
        '''
        await update_data('stats')

        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(client.guilds)
        memberCount = len(set(client.get_all_members())) # set removes duplicates
        # used to be ctx.guild.members

        with open('stats.json', 'r') as f:
            stats = json.load(f)

            embed = discord.Embed(
                title = ':gear: Look at these spicy stats',
                description = (f"I am in {serverCount} servers with a total of {memberCount} members. \nI'm running python version {pythonVersion} and discord.py {dpyVersion}. \nI have been issued {stats['total']} total commands."),
                colour = discord.Colour.red()
            )

        await ctx.send(embed=embed)

    @client.command()
    async def cmdstats(ctx):
        '''
        ~cmdstats - sends an embed with global command usage
        '''
        with open('stats.json', 'r') as f:
            stats = json.load(f)

            # bad way to check if owner id, find better way to do it later
            if ctx.message.author.id == client.owner_id:
                stat_string = f"""\n(~ping) - {stats['ping']}, \n(~hi) - {stats['hi']},\n(~info) - {stats['info']},\n(~echo) - {stats['echo']},\n(~stats) - {stats['stats']},\n(~joke) - {stats['joke']},\n(~profile) - {stats['profile']},\n(~helper) - {stats['helper']},\n(~join/leave) - {stats['join']+stats['leave']}, \n(~8ball) - {stats['8ball']}, \n(~play) - {stats['play']}, \n(~pause) - {stats['pause']}, \n(~resume) - {stats['resume']}, \n(~logout [basically failures]) - {stats['logout']} """
            else:
                stat_string = f"""\n(~ping) - {stats['ping']}, \n(~hi) - {stats['hi']},\n(~info) - {stats['info']},\n(~echo) - {stats['echo']},\n(~stats) - {stats['stats']},\n(~joke) - {stats['joke']},\n(~profile) - {stats['profile']},\n(~helper) - {stats['helper']},\n(~join/leave) - {stats['join']+stats['leave']}, \n(~8ball) - {stats['8ball']}, \n(~play) - {stats['play']}, \n(~pause) - {stats['pause']}, \n(~resume) - {stats['resume']} """

            embed = discord.Embed(
                title = ':scream: Look at these all these commands!',
                description = f"Total Commands - {stats['total']}," + stat_string,
                colour = discord.Colour.red()
            )

            await ctx.send(embed=embed)


    @client.command(aliases=['destroy', 'stop', 'quit', 'terminate', 'kill', 'murk', 'murder', 'stab'])
    @commands.is_owner()
    async def logout(ctx):
        '''
        ~logout/quit/destroy/stop/terminate/etc. - severs connections with discord
        '''
        embed = discord.Embed(
            title = (f"Hey {ctx.author.name}, I am logging off now. :wave:"),
            colour = discord.Colour.dark_red()
        )

        await ctx.send(embed=embed)
        # await client.logout()
        await client.close()
        await update_data('logout')
        print('bot has successfully logged out')

    @logout.error
    async def logout_error(ctx, error):
        '''
        n/a - when logout has an error, this function runs
        '''
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"Hey {ctx.author.mention}, you don't have access to this command. Sorry!")
        else:
            raise error

    @client.command()
    async def joke(ctx):
        '''
        ~joke - sends a random "joke" in an embed
        '''
        with open('jokes.json', 'r') as f:
            jokes = json.load(f)

        #print(jokes)
        idx = random.randint(1, 50)
        idx = str(idx)

        embed = discord.Embed(
          title=(f'{jokes[idx]}'),
          colour = discord.Colour.greyple()
        )

        await ctx.send(embed=embed)
        await update_data('joke')

    @client.command()
    async def profile(ctx, member: discord.Member = None):
        '''
        ~profile - lists the user's information (checking how to use)
        '''
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        roles.pop(0)

        embed = discord.Embed(
          colour = member.color,
          timestamp=ctx.message.created_at
        )

        if member == ctx.author:
            embed.set_thumbnail(url=(f'{ctx.author.avatar_url}'))
            embed.set_author(name=(f"{ctx.author.name}'s profile (AKA {ctx.author.display_name})"))
        else:
            embed.set_thumbnail(url=(f'{member.avatar_url}'))
            embed.set_author(name=(f"{member.name}'s profile (AKA {member.display_name})"))
        embed.set_footer(text=(f'Requested by {ctx.author}'), icon_url=ctx.author.avatar_url)

        embed.add_field(name='ID:', value=member.id, inline=True)
        embed.add_field(name='Server name:', value=member.display_name, inline=True)
        embed.add_field(name=(f'Roles: ({len(roles)})'), value=' '.join([role.mention for role in roles]), inline=False)
        embed.add_field(name='Top Role:', value=member.top_role.mention, inline=True)
        embed.add_field(name='Bot?', value=member.bot, inline=True)

        await ctx.send(embed=embed)
        await update_data('profile')

    @client.command(aliases=['8ball'])
    async def magic8(ctx):
        ans = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Signs point to yes', 'Reply hazy', 'Try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Dont count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']

        rand = random.choice(ans)

        embed = discord.Embed(
          colour = discord.Colour.blurple(),
          title = f"""**:8ball:** says: ```{rand}.```""",
          #description = f'Question posed: {ctx}'
        )

        await ctx.send(embed=embed) 
        await update_data('8ball')

    async def update_data(cmd):
        '''
        update_data - updates stats.json file when command is used
        '''
        #print(f'updating data for cmd: {cmd}...')
        with open("stats.json", "r") as f:
            stats = json.load(f)

            stats[cmd] += 1
            stats['total'] += 1

            with open("stats.json", "w") as f:
                json.dump(stats, f)

            #print(f'data has been updated for cmd {cmd}!')

    @client.command()
    async def helper(ctx):
        '''
        ~helper - sends an embed with commands for the bot
        '''
        embed = discord.Embed(
            title = 'Commands',
            colour = discord.Colour.orange()
        )

        embed.set_author(name='Jasper Bot 1.0',
        icon_url='https://i1.sndcdn.com/artworks-000215600087-h47tpo-t500x500.jpg')

        #embed.set_author(name='Helper for your wildest dreams :)')
        embed.add_field(name='\u200b', value='-------------------', inline=False)
        embed.add_field(name='_*TEXT COMMANDS*_   :keyboard:', value='\u200b', inline=False)
        embed.add_field(name='~ping', value="Returns 'Pong POG! + ping", inline = False)
        embed.add_field(name='~hi', value="Says hi to user when prompted", inline = False)
        embed.add_field(name='~echo', value="Echoes message provided by user", inline = False)
        embed.add_field(name='~stats', value="Displays bot's overall statistics", inline = False)
        embed.add_field(name='~cmdstats', value="Displays bot's global command usage", inline = False)
        embed.add_field(name='~joke', value="Displays a random message", inline = False)
        embed.add_field(name='~profile', value="Displays basic user information", inline = False)

        embed.add_field(name='\u200b', value='-------------------', inline=False)
        embed.add_field(name='_*AUDIO COMMANDS*_   :loud_sound:', value='\u200b', inline=False)
        embed.add_field(name='~join', value='Joins the voice channel of user', inline=False)
        embed.add_field(name='~disconnect', value='Disconnects bot from voice channel of user', inline=False)
        embed.add_field(name='~play', value='Plays a song from only a youtube link', inline=False)
        embed.add_field(name='~pause', value='Pauses the music currently playing', inline=False)
        embed.add_field(name='~resume', value='Resumed music after being paused', inline=False)

        await ctx.send(embed=embed)
        await update_data('helper')

    # =============================================================
    # VOICE CHANNEL STUFF - COMMANDS
    # =============================================================

    # MOVED TO MUSIC.PY

    client.run(TOKEN)

if __name__ == '__main__':
    main()
