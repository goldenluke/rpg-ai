import os
import discord
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente (.env)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL")

# 2. Classe customizada para gerenciar a sincronização do menu '/'
class RPG_Bot(commands.Bot):
    def __init__(self):
        # Intents necessários para o funcionamento pleno
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        """Este método roda antes do bot ligar e registra os comandos no Discord"""
        print("🔄 Sincronizando menu de comandos '/'...")
        try:
            # Sincroniza os comandos com os servidores do Discord
            synced = await self.tree.sync()
            print(f"✅ Sincronizado: {len(synced)} comandos registrados no menu.")
        except Exception as e:
            print(f"❌ Erro ao sincronizar: {e}")

# Instancia o bot
bot = RPG_Bot()

@bot.event
async def on_ready():
    print("\n" + "="*30)
    print(f"✅ SISTEMA OPERACIONAL!")
    print(f"🤖 Bot: {bot.user.name}")
    print(f"📡 Status: Online no menu '/'")
    print("="*30 + "\n")

# --- COMANDOS DO MENU VISUAL (SLASH COMMANDS) ---

@bot.tree.command(name="oi", description="Verifica se o bot está ouvindo o canal")
async def oi(interaction: discord.Interaction):
    """Comando simples de resposta rápida"""
    await interaction.response.send_message(
        f"🌊 Olá {interaction.user.mention}! Estou pronto para processar sua narrativa."
    )

@bot.tree.command(name="narrar", description="Analisa a cena de RPG e retorna a regra do Django Ninja")
@app_commands.describe(texto="Descreva o que está acontecendo (Ex: Katara ergueu as mãos)")
async def narrar(interaction: discord.Interaction, texto: str):
    """Envia a descrição para a API RAG Lite e exibe o resultado"""

    # Indica ao Discord que o bot está 'pensando' (evita erro de timeout em 3s)
    await interaction.response.defer(thinking=True)

    try:
        # Chamada para o backend Django Ninja
        payload = {"texto": texto}
        response = requests.post(API_URL, json=payload, timeout=15)

        if response.status_code == 200:
            dados = response.json()
            regra_nome = dados.get("regra_detectada", "Protocolo Geral")
            detalhes = dados.get("detalhes", "O mestre deve arbitrar a cena.")

            # Formata a resposta em um Embed elegante
            embed = discord.Embed(
                title=f"🧠 Análise de Contexto: {regra_nome}",
                description=detalhes,
                color=discord.Color.from_rgb(114, 137, 218) # Azul clássico Discord
            )
            embed.add_field(name="Narrativa analisada", value=f"*{texto[:200]}...*", inline=False)
            embed.set_footer(text="Motor: Django Ninja + RAG Lite")

            # Envia o resultado final
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"⚠️ Erro no Cérebro (Status {response.status_code}). O Django está ligado?")

    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        await interaction.followup.send("❌ Não consegui conectar ao servidor de regras do RPG.")

# 4. Execução do Bot
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERRO: DISCORD_TOKEN não encontrado. Verifique seu arquivo .env")
    else:
        bot.run(TOKEN)
