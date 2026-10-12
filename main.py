import discord
from discord import app_commands
import os
import random
import asyncio
from flask import Flask
from threading import Thread

# --- server per Render ---
app = Flask('')
@app.route('/')
def home():
    return "Maximo e' ON TOP!"
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIG FLAG ---
FLAGS = {
    "🇮🇹": "italia italy", "🇫🇷": "francia france", "🇩🇪": "germania germany",
    "🇪🇸": "spagna spain", "🇬🇧": "inghilterra uk england", "🇺🇸": "usa america",
    "🇯🇵": "giappone japan", "🇧🇷": "brasile brazil", "🇦🇷": "argentina",
    "🇵🇹": "portogallo portugal", "🇲🇽": "messico mexico", "🇨🇦": "canada",
    "🇦🇺": "australia", "🇬🇷": "grecia greece", "🇹🇷": "turchia turkey",
    "🇸🇪": "svezia sweden", "🇳🇴": "norvegia norway", "🇵🇱": "polonia poland",
    "🇷🇴": "romania", "🇺🇦": "ucraina ukraine", "🇨🇭": "svizzera switzerland",
    "🇳🇱": "olanda netherlands", "🇧🇪": "belgio belgium", "🇮🇳": "india",
    "🇰🇷": "corea south korea", "🇨🇳": "cina china", "🇪🇬": "egitto egypt"
}

active_games = {}

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Maximo ON TOP come {client.user}")

# /say
@tree.command(name="say", description="Fai parlare Maximo")
async def say(interaction: discord.Interaction, messaggio: str):
    await interaction.response.send_message("Inviato!", ephemeral=True)
    await interaction.channel.send(messaggio)

# /flag
@tree.command(name="flag", description="Indovina la bandiera")
@app_commands.describe(difficolta="Scegli difficolta: facile, medio, difficile")
async def flag(interaction: discord.Interaction, difficolta: str = "facile"):
    flag_emoji, answers = random.choice(list(FLAGS.items()))

    embed = discord.Embed(title="🌍 INDOVINA LA BANDIERA!", description=f"# {flag_emoji}\n\n**Difficoltà: {difficolta}**\nScrivi il nome del paese in chat!", color=0xFF0000)
    await interaction.response.send_message(embed=embed)

    active_games[interaction.channel.id] = answers.split()

    def check(m):
        return m.channel.id == interaction.channel.id and not m.author.bot

    try:
        while True:
            msg = await client.wait_for('message', timeout=60.0, check=check)
            guess = msg.content.lower().strip()
            if guess in active_games[interaction.channel.id]:
                await msg.channel.send(f"🎉 {msg.author.mention} ha indovinato! Era **{answers.split()[0].upper()}** {flag_emoji}")
                del active_games[interaction.channel.id]
                break
    except asyncio.TimeoutError:
        if interaction.channel.id in active_games:
            del active_games[interaction.channel.id]
            await interaction.channel.send(f"⏰ Tempo scaduto! Era {flag_emoji} -> {answers.split()[0]}")

# /start
@tree.command(name="start", description="SOLO ADMIN - Annuncia Maximo ovunque")
async def start(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Solo gli amministratori possono farlo!", ephemeral=True)
        return

    await interaction.response.send_message("Invio in corso...", ephemeral=True)
    testo = "# MAXIMO ON TOP #\nhttps://discord.gg/EAhmen5yu"

    count = 0
    for channel in interaction.guild.text_channels:
        try:
            await channel.send(testo)
            count += 1
            await asyncio.sleep(0.5)
        except:
            pass
    await interaction.followup.send(f"Fatto! Inviato in {count} canali.", ephemeral=True)

keep_alive()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("ERRORE CRITICO: TOKEN non trovato nelle Environment Variables di Render!")
else:
    client.run(TOKEN)
