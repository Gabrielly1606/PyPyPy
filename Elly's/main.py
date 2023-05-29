import discord
from Dropdown import Dropdown
from DropdownView import DropdownView
from CreateTicket import CreateTicket
from CreateEmbed import  MyCog
import discord as d
from discord import app_commands
from discord.ext import commands
import interactions
import json
import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps

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
<<<<<<< HEAD
=======
#id_do_servidor = 481659634701303838
>>>>>>> 51608d7e934d68d3ed97ed403bcd1390a0fb488b
id_cargo_atendente = 1089374159060082759



class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="ajuda",label="Ajuda", emoji="👋"),
            discord.SelectOption(value="atendimento",label="Atendimento", emoji="📨"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "ajuda":
            await interaction.response.send_message("Se você precisar de ajuda",ephemeral=True)
        elif self.values[0] == "atendimento":
            await interaction.response.send_message("Clique abaixo para criar um ticket",ephemeral=True,view=CreateTicket())

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(Dropdown())

class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value=None

    @discord.ui.button(label="Abrir Ticket",style=discord.ButtonStyle.blurple,emoji="➕")
    async def confirm(self,interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(ephemeral=True,content=f"Você já tem um atendimento em andamento!")
                    return

        async for thread in interaction.channel.archived_threads(private=True):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.edit_original_response(content=f"Você já tem um atendimento em andamento!",view=None)
                    return
        
        if ticket != None:
            await ticket.edit(archived=False,locked=False)
            await ticket.edit(name=f"{interaction.user.name} ({interaction.user.id})",auto_archive_duration=10080,invitable=False)
        else:
            ticket = await interaction.channel.create_thread(name=f"{interaction.user.name} ({interaction.user.id})",auto_archive_duration=10080)#,type=discord.ChannelType.public_thread)
            await ticket.edit(invitable=False)

        await interaction.response.send_message(ephemeral=True,content=f"Criei um ticket para você! {ticket.mention}")
        await ticket.send(f"📩  **|** {interaction.user.mention} ticket criado! Envie todas as informações possíveis sobre seu caso e aguarde até que um atendente responda.\n\nApós a sua questão ser sanada, você pode usar `/fecharticket` para encerrar o atendimento!")

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

class deletechannel(discord.Client):
    async def deletechannel(ctx, channel: d.TextChannel):
        mbed = d.Embed(
            title = 'Sucesso',
            description = 'Chat deletado com sucesso',
        )
        if ctx.author.guild_permission.manage_channels:
            await ctx.send(embed=mbed)
            await channel.delete()

async def on_member_join(member):
    channel = client.get_channel(1090105200267772025)
    await channel.send(file=discord.File('Jabi.png'))
    
    url = requests.get(member.avatar_url)
    avatar = Image.open(BytesIO(url.content))
    avatar = avatar.resize((120, 120))
    bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
    mascara = Image.new('L', bigavatar, 0)
    recortar = ImageDraw.Draw(mascara)
    recortar.ellipse((0, 0) + bigavatar, fill=255)
    mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
    avatar.putalpha(mascara)

    saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 0.5))
    saida.save('jabi.png')
    img = Image.open('bemvindotest.png')

    fonte = ImageFont.truetype('TheWildBreathOfZelda-15Lv.ttf', 45)
    escrever = ImageDraw.Draw(img)
    escrever.text(xy=(210, 180), text=member.name, fill=(0, 0, 0), font=fonte)
    img.paste(avatar, (70, 130), avatar)
    img.save('Jabi.png')



aclient = client()
tree = app_commands.CommandTree(aclient)
bot = interactions.Client(token=token_bot)

@tree.command(guild= discord.Object(id=id_do_servidor), name = "deletechannel", description='Chat deletado com sucesso')
@commands.has_permissions(manage_guild=True)
async def deletechannel(interaction: discord.Integration):
    view=MyCog()
    await interaction.response.send_message("deletechannel",view=view)
    await interaction.channel.edit(archived=True,locked=True)

@tree.command(guild= discord.Object(id=id_do_servidor), name = "criarmesa", description='gera uma mesa')
@commands.has_permissions(manage_guild=True)
async def criarmesa(interaction: discord.Integration):
    view=MyCog()
    await interaction.response.send_message("gerar aventura",view=view)

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'setup', description='Setup')
@commands.has_permissions(manage_guild=True)
async def setup(interaction: discord.Interaction):
    await interaction.response.send_message("Mensagem do painel",view=DropdownView()) 

@tree.command(guild = discord.Object(id=id_do_servidor), name="fecharticket",description='Feche um atendimento atual.')
async def _fecharticket(interaction: discord.Interaction):
    mod = interaction.guild.get_role(id_cargo_atendente)
    if str(interaction.user.id) in interaction.channel.name or mod in interaction.user.roles:
        await interaction.response.send_message(f"O ticket foi arquivado por {interaction.user.mention}, obrigado por entrar em contato!")
        await interaction.channel.edit(archived=True,locked=True)
    else:
        await interaction.response.send_message("Isso não pode ser feito aqui...")
        
@tree.command(guild = discord.Object(id=id_do_servidor), name="perfil",
              description='Olhar o perfil.')
async def _getProfille(interaction: discord.Interaction):
    url = "http://127.0.0.1:5000/api/users/" + str(interaction.user.id)
    response = requests.get(url)
    response.json()
    await interaction.response.send_message(response.json())
    
@tree.command(guild = discord.Object(id=id_do_servidor), name="todosperfil",
              description='Olhar o perfil de todos.')
async def _getProfille(interaction: discord.Interaction):
    url = "http://127.0.0.1:5000/api/users"
    response = requests.get(url)
    response.json()
    await interaction.response.send_message(response.json())

@tree.command(guild = discord.Object(id=id_do_servidor), name="criarperfil",
              description='cria um perfil.')
async def _create_user(interaction: discord.Interaction):
    url = "http://127.0.0.1:5000/api/users"
    data = {"name": interaction.user.name, "exp": 100}
    response = requests.post(url, json=data)
    response.json()
    await interaction.response.send_message(response.json())
    
@tree.command(guild = discord.Object(id=id_do_servidor), name="addexp",
              description='Adiciona exp.')
async def _add_exp(interaction: discord.Interaction):
    url = "http://127.0.0.1:5000/api/users/" + str(interaction.user.id)
    data = {"name": interaction.user.name, "exp": 100}
    response = requests.put(url, json=data)
    response.json()
    await interaction.response.send_message(response.json())

@tree.command(guild = discord.Object(id=id_do_servidor), name="destino",
              description='Veja seu destino.')
async def _getProfille(interaction: discord.Interaction):
    url = "http://127.0.0.1:5000/api/destiny"
    response = requests.get(url)
    json_response = response.json()
    text = json_response["text"]
    await interaction.response.send_message(text)
    
@tree.command(name="mapa",
              description='MapaRPG.',
              guild = discord.Object(id=id_do_servidor),
              extras=dict(params={}))
async def _getProfille(interaction: discord.Interaction, params):
    url = "http://127.0.0.1:5000/api/map"
    params = {'player1': 'a', 'x1': 100, 'y1': 200,
              'player2': 'b', 'x2': 400, 'y2': 100,
              'player3': 'c', 'x3': 50, 'y3': 100,
              'player4': 'tenta', 'x4': 100, 'y4': 100,}  # Example of parameters
    request_params = {**params}
    url = url + "?" + request_params
    response = requests.get(url)
    #response = requests.get(url, params=params)
    image_bytes = response.content
    dFile = discord.File(open('F:\\Development\\visual code\\Python\\discord\\Talya\\PyPyPy\\api\\temp.png', 'rb'))
    await interaction.response.send_file(image_bytes, filename='mapa.png')
    #await ctx.channel.send(File=dFile)
    #await ctx.response.send_message(file=dFile)
    #await interaction.response.send_file(image_bytes, filename='mapa.png')
        
aclient.run(token_bot)