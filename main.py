import discord
import os
import json
from datetime import datetime
from itertools import cycle
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', help_command=None,intents=intents)
client.launch_time = datetime.utcnow()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

with open('./config.json') as f:
    config = json.load(f)

token = config.get('token')

@client.event
async def on_ready():
    print("I'm ready lol.")


@tasks.loop(minutes=2)
async def changer():
    await client.wait_until_ready()
    await client.change_presence(activity=discord.Game(name=next(client.status)))


status1 = f"Best bot ww! | .help"
status2 = f"Doggo Pictures! | .help"
status3 = f"Crypto Stats! | .help"
status4 = f"Memes! | .help"
status4 = f"Dadjokes! 😒 | .help"
client.status = cycle([status1, status2, status3, status4])
changer.start()

@client.command()
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    uptimeembed = discord.Embed(title = "")
    uptimeembed.add_field(name = "Uptime:", value = f"{days}d, {hours}h, {minutes}m, {seconds}s since last restart.")
    await ctx.send(embed=uptimeembed)

@client.group(invoke_without_command=True)
async def help(ctx):
    helpembed = discord.Embed(title='Help', description='Made with <3 by Supelion.', color=discord.Color.blue())

    helpembed.add_field(name='<:crypto:844234812331524117> Crypto', value='``.btc ; .eth; .doge; .bat; .ada``', inline=False)
    
    helpembed.add_field(name='<:misc:844235406877917234> Utility', value='``.about; .support; .ping; .invite; .id; .stats; .remind; .uptime``', inline=False)
    
    helpembed.add_field(name='<a:813111549941252126:844446604043878410> Fun', value='``.meme; .dadjoke; .coinflip; .8b; .avatar; .bored; .doggo``', inline=False)
    
    helpembed.set_thumbnail(url='https://media.discordapp.net/attachments/835071270117834773/844229169863983154/logo.PNG')
    
    helpembed.set_footer(text="Utility Bot | Supelion#4275")

    await ctx.send(embed=helpembed)


client.run(f"{token}")