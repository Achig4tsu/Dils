import discord
from discord.ui import View, Button

class InteractiveEmbed(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.embeds = [discord.Embed(title="Page 1", description="Description of Page 1"),
                       discord.Embed(title="Page 2", description="Description of Page 2")]
        self.page_index = 0  # Keep track of current page index
        self.setup_hub()

    def setup_hub(self):
        self.clear_items()
        self.add_item(Button(label="Page 1", style=discord.ButtonStyle.blurple, custom_id="page1"))
        self.add_item(Button(label="Page 2", style=discord.ButtonStyle.blurple, custom_id="page2"))
        self.add_item(Button(label="Settings", style=discord.ButtonStyle.green, custom_id="settings"))

    def setup_settings(self):
        self.clear_items()
        self.add_item(Button(label="Back to Hub", style=discord.ButtonStyle.red, custom_id="back"))
        # Add more buttons for different settings/options

    async def interaction_handler(self, interaction: discord.Interaction):
        if interaction.data['custom_id'] == "page1":
            self.page_index = 0
        elif interaction.data['custom_id'] == "page2":
            self.page_index = 1
        elif interaction.data['custom_id'] == "settings":
            self.setup_settings()
            await interaction.response.edit_message(view=self)
            return
        elif interaction.data['custom_id'] == "back":
            self.setup_hub()
            await interaction.response.edit_message(view=self)
            return

        await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.embeds[self.page_index], view=self)

    async def send_embed(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.embeds[self.page_index], view=self)

    @discord.ui.button(label="Page 1", style=discord.ButtonStyle.blurple, custom_id="page1")
    async def page1_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.interaction_handler(interaction)

    @discord.ui.button(label="Page 2", style=discord.ButtonStyle.blurple, custom_id="page2")
    async def page2_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.interaction_handler(interaction)

    @discord.ui.button(label="Settings", style=discord.ButtonStyle.green, custom_id="settings")
    async def settings_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.interaction_handler(interaction)
