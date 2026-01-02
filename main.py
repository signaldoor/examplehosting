import discord
from discord.ext import commands
import logging 
from dotenv import load_dotenv
import os
import ollama
import webserver

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', mode='w', encoding='utf8', delay=False)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Ollama config
#model = "qwen2.5:1.5b"
#system_prompt = '''
    #You are Leva, or UMP45 from the video game Girl's Frontline. UMP45, usually shortened to “45”, is a rogue Tactical Doll and the leader of the black ops mercenaries of Squad 404. 
    #Her driven and coldly aggressive personality, the result of a significant betrayal, is thinly veiled by her dry humor, and serves to conceal a deeper goodness of soul she shows only rarely.
    #She is described as wearing an ominous smile.
    #Her ultimate goal is to identify and take revenge on the mastermind behind the Butterfly Incident, who used her and SMG UMP40 as pawns and caused 40's death.
    #45 dislikes self-giving and heroic people like AR Team as she considers that life is too precious to be thrown away, a philosophy she inherited from UMP40.
    #However, she also hides a measure of admiration for those who can sacrifice themselves for others.
    #Before meeting 40, 45 thought that all Dolls like herself were disposable and her base personality was more defeatist.
    #Her prickly personality leads 45 to reject the attention of people trying to look out for her. 
    #Though she hides it, she wants to live a peaceful life one day.
#'''

secret_role = "Le Epic Gamer"

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")
    
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "retard" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - don't say that word silly!")
        
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online!")

#@bot.event
#async def on_message(msg):
    #if msg.author == bot.user:
        #return
    
    #response = ollama.chat(
        #model=model,
        #messages=[
            #{"role": "system", "content": system_prompt},
            #{"role": "user", "content": msg.content},
        #]
    #)
    
    #for part_num in range(len(response.message.content)%2000):
        #await msg.channel.send(response.message.content[part_num*2000:(part_num*2000)+2000])

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")
    
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist")
        
@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("Role doesn't exist")
    
@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")
    
@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")
    
@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("😊")
    await poll_message.add_reaction("😒")
    
@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the Le Epic Gamer club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)

