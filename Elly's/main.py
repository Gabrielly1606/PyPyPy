import discord
import CreateTicket
from DropdownView import DropdownView
from discord import app_commands
from discord.ext import commands
import json
import os

filename = "config.json"

if not os.path.isfile(filename):
    print("File does not exist, creating file...")
    config = {"token_bot": "MeuTokken"}
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)
    token_bot = "MeuTokken"
else:
    with open(filename, "r") as f:
        config = json.load(f)
    token_bot = config["token_bot"]
    print(f"Retrieved token_bot value from {filename}: {token_bot}")
    
id_do_servidor = 1089260593954967553
id_cargo_atendente = 1089374159060082759

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False #Nós usamos isso para o bot não sincronizar os comandos mais de uma vez

    async def setup_hook(self) -> None:
        self.add_view(DropdownView())

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #Checar se os comandos slash foram sincronizados 
            await tree.sync(guild = discord.Object(id=id_do_servidor)) # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
            self.synced = True
        print(f"Entramos como {self.user}.") 

aclient = client()

tree = app_commands.CommandTree(aclient)

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'setup', description='Setup')
@commands.has_permissions(manage_guild=True)
async def setup(interaction: discord.Interaction):
    await interaction.response.send_message("Mensagem do painel",view=DropdownView()) 


@tree.command(guild = discord.Object(id=id_do_servidor), name="fecharticket",description='Feche um atendimento atual.')
async def _fecharticket(interaction: discord.Interaction):
    mod = interaction.guild.get_role(id_cargo_atendente)
    if str(interaction.user.id) in interaction.channel.name or mod in interaction.author.roles:
        await interaction.response.send_message(f"O ticket foi arquivado por {interaction.user.mention}, obrigado por entrar em contato!")
        await interaction.channel.edit(archived=True,locked=True)
    else:
        await interaction.response.send_message("Isso não pode ser feito aqui...")

aclient.run(token_bot)