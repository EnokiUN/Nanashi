import discord
from discord.ext import commands, tasks
from vars import *
from views import *
from engine import *

intents = discord.Intents.all()
client = commands.Bot(command_prefix="-", case_insensitive=True, intents=intents)

@client.event
async def on_ready():
    change_status.start()
    print(f"logged in as {client.user}, time to get some work done")
    
@tasks.loop(minutes=10)
async def change_status():
    await client.change_presence(activity=discord.Streaming(name=f"{len(client.guilds)} servers!", url=TWITCH_URL))
        
@client.slash_command(guild_ids=GUILD_IDS, description="A test command that's functionality changes every while..... for testing purposes.")
async def test(ctx, atk: discord.Option(int, "the amount of attack you have", required=False, default=20)):
    goblin = Enemy("goblin", {"hp": 100, "mp": 20, "atk": 10, "def": 5}) 
    player = Player(ctx.author, {"hp": 100, "mp": 20, "atk": atk, "def": 5})
    view = BattleView(ctx=ctx, player=player, enemy=goblin)
    await ctx.respond("a goblin approaches, what do you do?", view=view) 
    
@client.slash_command(guild_ids=GUILD_IDS, description="Looking to invite me  or join my support server? this is the command you're looking for then!")
async def invite(ctx):
    embed = discord.Embed(title="My invite links", description=f"Want to invite me to your own server?\nYes please!\n\nAdding me to your servers would be very appreciated and it's very simple, just click on the buttons below and you'll be redirected to my invite page.\n\nCurrently in **{len(client.guilds)}** servers", url=INVITE_LINK, colour=EMBED_HEX)
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label='Invite me!', url=INVITE_LINK, style=discord.ButtonStyle.url))
    view.add_item(discord.ui.Button(label="Support server!", url=SUPPORT_SERVER_LINK, style=discord.ButtonStyle.url))
    await ctx.respond(embed=embed, view=view)
    
for i in COGS:
    client.load_extension(i)
client.run(TOKEN)