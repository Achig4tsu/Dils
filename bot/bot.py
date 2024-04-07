import discord
from discord.ext import commands

from .SetupServer.ServerSetup import InteractiveEmbed

class MyBot():
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  
        intents.message_content = True
        intents.integrations = True
        intents.guilds = True 
        intents.guild_messages = True
        intents.guild_reactions = True
        intents.voice_states = True

        
        self.client = commands.Bot(command_prefix="", intents=intents)


    def setup(self) :
        client = self.client
        
        
        @client.tree.command(name="setup", description="🤖 - Mise en place du Bot.")
        async def setup(interaction: discord.Interaction):
            await InteractiveEmbed().send_embed(interaction)
        
        @client.tree.command(name="ban", description="🤖 - Mise en place du Bot.")
        async def setup(interaction: discord.Interaction):
            await InteractiveEmbed().send_embed(interaction)
            
        @client.tree.command(name="unban", description="🤖 - Mise en place du Bot.")
        async def setup(interaction: discord.Interaction):
            await InteractiveEmbed().send_embed(interaction)
        
            

        @client.event
        async def on_ready():
            print ("----------------")
            print ("|  D  I  L  S  |")
            print ("----------------")
            print ()
            
            print ("Version : 1.0")
            print (client.user.name)
                        
            await client.tree.sync()
            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity(name="Watching everyone..."))
    
    def run(self) :
        self.setup()
        t = open("./token.txt", 'r').read()
        self.client.run(t)
        
    
        
        

if __name__ == "__main__" :
    pass
       
        
