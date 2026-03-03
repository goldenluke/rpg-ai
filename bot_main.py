import os
import discord
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# ==========================================================
# CONFIG
# ==========================================================

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
API_BASE = os.getenv("API_BASE_URL")

ROOMS = {}  # Estado multiplayer por canal


# ==========================================================
# BOT BASE
# ==========================================================

class RPG_Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        print("🔄 Sincronizando comandos...")
        synced = await self.tree.sync()
        print(f"✅ {len(synced)} comandos sincronizados.")


bot = RPG_Bot()


# ==========================================================
# UTILIDADES
# ==========================================================

def get_room(channel_id):
    if channel_id not in ROOMS:
        ROOMS[channel_id] = {
            "players": {},
            "turn_order": [],
            "current_turn": None,
            "guild": None
        }
    return ROOMS[channel_id]


def advance_turn(room):
    if not room["turn_order"]:
        return

    idx = room["turn_order"].index(room["current_turn"])
    next_idx = (idx + 1) % len(room["turn_order"])
    room["current_turn"] = room["turn_order"][next_idx]


# ==========================================================
# READY
# ==========================================================

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"🤖 Bot Online: {bot.user}")
    print("=" * 40)


# ==========================================================
# CRIAR PERSONAGEM
# ==========================================================

@bot.tree.command(name="criar", description="Criar personagem na sala atual")
@app_commands.describe(nome="Nome do personagem", classe="guerreiro, mago ou ladino")
async def criar(interaction: discord.Interaction, nome: str, classe: str):

    await interaction.response.defer(thinking=True)

    channel_id = interaction.channel.id
    room = get_room(channel_id)

    response = requests.post(
        f"{API_BASE}/criar-sessao",
        json={
            "nome": nome,
            "classe": classe,
            "room_id": str(channel_id),
            "user_id": str(interaction.user.id)
        }
    )

    data = response.json()
    session_id = data["session_id"]

    room["players"][interaction.user.id] = session_id

    if interaction.user.id not in room["turn_order"]:
        room["turn_order"].append(interaction.user.id)

    if room["current_turn"] is None:
        room["current_turn"] = interaction.user.id

    embed = discord.Embed(
        title=f"🧙 {nome} entrou na aventura!",
        color=discord.Color.green()
    )

    embed.add_field(name="Classe", value=classe)
    embed.add_field(name="HP", value=data["personagem"]["hp"])
    embed.add_field(name="Mana", value=data["personagem"]["mana"])

    await interaction.followup.send(embed=embed)


# ==========================================================
# NARRAR
# ==========================================================

@bot.tree.command(name="narrar", description="Enviar narrativa para o motor QWAN")
@app_commands.describe(texto="Descreva sua ação")
async def narrar(interaction: discord.Interaction, texto: str):

    await interaction.response.defer(thinking=True)

    channel_id = interaction.channel.id

    response = requests.post(
        f"{API_BASE}/analisar-cena",
        json={
            "textos": [texto],
            "room_id": str(channel_id),
            "user_id": str(interaction.user.id)
        }
    )

    data = response.json()

    embed = discord.Embed(
        title="📖 Narrativa",
        description=data["narrativa"],
        color=discord.Color.blue()
    )

    await interaction.followup.send(embed=embed)


# ==========================================================
# AÇÃO (COM TURNO REAL)
# ==========================================================

@bot.tree.command(name="acao", description="Executar ação no seu turno")
@app_commands.describe(tipo="Atacar, Magia ou Defender")
async def acao(interaction: discord.Interaction, tipo: str):

    await interaction.response.defer(thinking=True)

    channel_id = interaction.channel.id
    user_id = interaction.user.id

    room = get_room(channel_id)

    if user_id not in room["players"]:
        await interaction.followup.send("⚠️ Você precisa criar um personagem primeiro.")
        return

    if room["current_turn"] != user_id:
        await interaction.followup.send(
            f"⏳ Não é seu turno! É o turno de <@{room['current_turn']}>."
        )
        return

    session_id = room["players"][user_id]

    response = requests.post(
        f"{API_BASE}/combate",
        json={
            "session_id": session_id,
            "acao": tipo,
            "room_id": str(channel_id),
            "user_id": str(user_id)
        }
    )

    data = response.json()

    embed = discord.Embed(
        title=f"⚔️ {interaction.user.display_name} usou {tipo}",
        description=data["narrativa"],
        color=discord.Color.red()
    )

    embed.add_field(name="HP", value=data["hp"])
    embed.add_field(name="Mana", value=data["mana"])
    embed.add_field(name="XP", value=data["xp"])
    embed.add_field(name="HP Inimigo", value=data["hp_inimigo"])

    await interaction.followup.send(embed=embed)

    # Avança turno
    advance_turn(room)

    if room["current_turn"]:
        await interaction.channel.send(
            f"🔄 Próximo turno: <@{room['current_turn']}>"
        )


# ==========================================================
# STATUS
# ==========================================================

@bot.tree.command(name="status", description="Ver status da sala")
async def status(interaction: discord.Interaction):

    channel_id = interaction.channel.id
    room = get_room(channel_id)

    embed = discord.Embed(
        title="📊 Status da Sala",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="Jogadores",
        value="\n".join([f"<@{u}>" for u in room["players"].keys()]) or "Nenhum",
        inline=False
    )

    embed.add_field(
        name="Turno Atual",
        value=f"<@{room['current_turn']}>" if room["current_turn"] else "Nenhum"
    )

    await interaction.response.send_message(embed=embed)


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":

    if not TOKEN:
        print("❌ DISCORD_TOKEN não encontrado.")
    else:
        bot.run(TOKEN)
