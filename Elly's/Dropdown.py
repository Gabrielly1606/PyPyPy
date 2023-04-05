import discord
import CreateTicket
import DropdownView
import Dropdown

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
