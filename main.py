import discord
from discord.ext import commands
import asyncio

# Configurazione dei permessi per il bot
intents = discord.Intents.default()
intents.members = True
intents.messages = True

# Inizializzazione del bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connesso come {bot.user}')

@bot.slash_command(name='start', description='Inizia la raid creando canali e messaggi.')
async def start_command(interaction: discord.Interaction):
    member = interaction.user
    
    # Controllo permesso AMMINISTRATIVO
    if not member.guild_permissions.administrator:
        await interaction.response.send_message("Solo gli Amministratori possono usare questo comando!", ephemeral=True)
        return

    await interaction.response.defer()

    for i in range(10):
        # Crea il canale
        channel = await interaction.guild.create_text_channel(name="maximo on top")
        
        # Invia il messaggio 5 volte
        message_content = "# MAXIMO ON TOP# https://discord.gg/Bkz4WHPvkT"
        for _ in range(5):
            await channel.send(message_content)
            await asyncio.sleep(0.1) # Breve pausa per evitare rate limit immediato

    await interaction.edit_original_response(content="Raid avviata: 10 canali creati e messaggi inviati.")

# Avvio del bot (il token viene inserito al momento dell'esecuzione o via variabile d'ambiente)
bot.run()
