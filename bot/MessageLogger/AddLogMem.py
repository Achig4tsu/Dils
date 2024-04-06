import discord
from discord.ext import commands
import json
from datetime import datetime

intents = discord.Intents.default()
intents.members = True  
intents.message_content = True
intents.integrations = True
intents.guilds = True 
intents.guild_messages = True
intents.guild_reactions = True
intents.voice_states = True

# Initialiser le bot
bot = commands.Bot(command_prefix='!', intents=intents)


# Créer la structure de base du fichier JSON s'il n'existe pas
def create_user_list_json(filename):
    user_list = []
    with open(filename, 'w') as file:
        json.dump(user_list, file, indent=4)

# Charger la liste des utilisateurs à partir du fichier JSON
def load_user_list_from_json(filename):
    try:
        with open(filename, 'r') as file:
            user_list = json.load(file)
    except FileNotFoundError:
        create_user_list_json(filename)
        user_list = []
    return user_list

# Sauvegarder la liste des utilisateurs dans le fichier JSON
def save_user_list_to_json(filename, user_list):
    with open(filename, 'w') as file:
        json.dump(user_list, file, indent=4)

# Charger le token du bot Discord à partir d'un fichier
def load_token_from_file(filename):
    with open(filename, 'r') as file:
        token = file.read().strip()
    return token

# Envoyer les messages des utilisateurs dans un canal spécifique
async def send_messages_to_channel(client, user_list, channel_id):
    channel_admin = client.get_channel(channel_id)
    if channel_admin is None:
        print("Channel not found!")
        return
    
    for user_info in user_list:
        user_id = int(user_info['id'])
        messages = user_info.get('messages', [])
        user = client.get_user(user_id)
        if user is None:
            print(f"User with ID {user_id} not found!")
            continue
        
        for message_info in messages:
            guild_id = message_info.get('guild_id')
            channel_id = message_info.get('channel_id')
            content = message_info.get('content')
            timestamp = message_info.get('timestamp')
            
            if timestamp:
                timestamp = datetime.fromisoformat(timestamp)
            else:
                timestamp = datetime.now()
            
            guild = client.get_guild(guild_id)
            channel = guild.get_channel(channel_id)
            
            if channel is None:
                print(f"Channel with ID {channel_id} not found in guild with ID {guild_id}!")
                continue
            
            embed = discord.Embed(title="Message Log", color=0x00ff00)
            embed.add_field(name="User", value=user.name, inline=False)
            embed.add_field(name="Guild", value=guild.name, inline=False)
            embed.add_field(name="Channel", value=channel.name, inline=False)
            embed.add_field(name="Timestamp", value=timestamp, inline=False)
            embed.add_field(name="Message", value=content, inline=False)
            
            await channel_admin.send(embed=embed)

# Commande pour les modérateurs permettant d'ajouter un utilisateur à surveiller
@bot.command()
@commands.has_permissions(manage_messages=True)  # Seuls les modérateurs peuvent utiliser cette commande
async def add_user(ctx, user_id: int):
    user_list = load_user_list_from_json('logs.json')
    if not any(user_info['id'] == str(user_id) for user_info in user_list):
        user_list.append({'id': str(user_id)})
        save_user_list_to_json('logs.json', user_list)
        await ctx.send(f"User with ID {user_id} added to watchlist.")
    else:
        await ctx.send(f"User with ID {user_id} is already in watchlist.")

# Commande pour les modérateurs permettant de supprimer un utilisateur de la liste de surveillance
@bot.command()
@commands.has_permissions(manage_messages=True)  # Seuls les modérateurs peuvent utiliser cette commande
async def remove_user(ctx, user_id: int):
    user_list = load_user_list_from_json('logs.json')
    user_found = False
    for user_info in user_list:
        if user_info['id'] == str(user_id):
            user_list.remove(user_info)
            save_user_list_to_json('logs.json', user_list)
            await ctx.send(f"User with ID {user_id} removed from watchlist.")
            user_found = True
            break
    if not user_found:
        await ctx.send(f"User with ID {user_id} is not in watchlist.")

# Événement déclenché lorsqu'un message est envoyé sur un serveur
@bot.event
async def on_message(message):
    if not message.author.bot:  # Ignore les messages provenant des bots
        user_list = load_user_list_from_json('logs.json')
        for user_info in user_list:
            if user_info['id'] == str(message.author.id):
                user_info.setdefault('messages', []).append({
                    'guild_id': message.guild.id,
                    'channel_id': message.channel.id,
                    'content': message.content,
                    'timestamp': message.created_at.isoformat()
                })
                save_user_list_to_json('logs.json', user_list)
                break
    await bot.process_commands(message)  # Nécessaire pour exécuter les autres commandes du bot

# Événement de connexion
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # Charger la liste des utilisateurs à partir du fichier JSON
    user_list = load_user_list_from_json('logs.json')

    # Envoyer les messages des utilisateurs dans le canal spécifié
    await send_messages_to_channel(bot, user_list, 1220772981895069766)  # Remplacer l'ID du canal par l'ID du canal spécifique

# Charger et démarrer le bot avec le token
token = load_token_from_file('token.txt')
bot.run(token)
