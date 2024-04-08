import discord
from discord.ui import Button, View

class InteractiveEmbed(View):
    def __init__(self, embeds):
        super().__init__()
        self.page = 0
        self.embeds = embeds

        self.add_item(Button(label="<", style=discord.ButtonStyle.green, custom_id="prev_button"))
        self.add_item(Button(label=">", style=discord.ButtonStyle.green, custom_id="next_button"))

    async def update_embed(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.embeds[self.page], view=self)

    async def send_embed(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.embeds[self.page], view=self)

    @discord.ui.button(label="<", style=discord.ButtonStyle.green, custom_id="prev_button")
    async def prev_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.page > 0:
            self.page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.green, custom_id="next_button")
    async def next_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.page < len(self.embeds) - 1:
            self.page += 1
            await self.update_embed(interaction)
