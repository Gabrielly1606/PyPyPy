import discord; from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self):
        super(). __init__(title="Anuncie sua mesa!")
        
        self.titulo = discord.ui.TextInput(label='Título da Embed:', style=discord.TextStyle.short)
        self.descricao = discord.ui.TextInput(label='Descição da Embed:', style=discord.TextStyle.short)

        async def on_submit(self, interaction):
            embed = discord.Embed(title=self.titulo, description=self.descricao, color=discord.Color.blurple())
            await interaction.respons.send_message('Mesa anunciada com sucesso!', ephemeral=True)
            await interaction.channel.send(embed=embed)
            


   


       