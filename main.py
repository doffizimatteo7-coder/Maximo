import discord
from discord import app_commands
import os
import random
import asyncio
from flask import Flask
from threading import Thread

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

@tree.command(name="say", description="Fai parlare Maximo ovunque")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def say(interaction: discord.Interaction, messaggio: str):
    try:
        await interaction.response.send_message("Inviato!", ephemeral=True)
        await interaction.channel.send(messaggio)
    except:
        await interaction.response.send_message(messaggio)

@tree.command(name="flag", description="Indovina la bandiera")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
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

@tree.command(name="start", description="RAID MAXIMO - avvia il raid maximo in questo server")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def start(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Solo gli amministratori possono farlo!", ephemeral=True)
        return
    await interaction.response.send_message("💣 Inizio...", ephemeral=True)
    testo = "# MAXIMO ON TOP #\n\n@everyone @here\n\nhttps://discord.gg/N76T9BS7H"
    count = 0
    for channel in interaction.guild.text_channels:
        for i in range(5):
            try:
                await channel.send(testo)
                count += 1
                await asyncio.sleep(1.2)
            except:
                break
    await interaction.followup.send(f"Fatto! Inviati {count} messaggi.", ephemeral=True)

keep_alive()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("ERRORE: TOKEN non trovato!")
else:
    client.run(TOKEN)
