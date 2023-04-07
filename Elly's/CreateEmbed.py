import discord; from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
class Modal(discord.ui.Modal):
    def __init__(self):
        super(). __initt__(title="Anuncie sua mesa!")
        
        titulo = discord.ui.TextInput(label='Título da Embed:', style=discord.TextStyle.short)
        descrição = discord.ui.TextInput(label='Descição da Embed:', style=discord.TextStyle.short)

        async def on_submit(self, interaction):
            embed = discord.Embed(title=self.titulo, description=self.descrição, color=discord.Color.blurple())
            await interaction.respons.send_message('Mesa anunciada com sucesso!', ephemeral=True)
            await interaction.channel.send(embed=embed)

class CreateEmbed(commands.Cog):
     def __init__(self, bot):
        self.bot = bot


   


       