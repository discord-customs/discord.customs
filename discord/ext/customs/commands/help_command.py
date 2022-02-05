import discord, typing

class Trash(discord.ui.Button):
    def __init__(self, ctx, help):
        self.context = ctx
        self.help = help

        super().__init__(label="Trash", row=1, emoji="🗑️")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            "_Original message deleted_", embed=None
        )


class Dropdown(discord.ui.Select):
    def __init__(self, ctx, help):
        self.context = ctx
        self.help = help
        options = [
            discord.SelectOption(
                label="Home", description="The main menu.", value="Home"
            ),
        ]
        super().__init__(
            placeholder="Where do you wanna go",
            min_values=1,
            custom_id="Dropdowns",
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        embedd = discord.Embed(
            title="Help",
            description="```\n[] -> optional\n<> -> required```",
        )
        if self.values[0] == "Home":
            await interaction.response.edit_message(embed=embedd)


class DropdownView(discord.ui.View):
    def __init__(self, ctx, help):
        super().__init__(timeout=50.0)
        self.context = ctx
        self.value = "Id"
        self.h = help
        self.add_item(Dropdown(ctx, help))

    @discord.ui.button(label="Trash", style=discord.ButtonStyle.red, emoji="🗑️")
    async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.value = "Stopped"
        # Make sure to update the message with our updated selves
        await self.message.edit(view=self, content="STOPPED")
        self.clear_items()
        self.timeout = None
        await interaction.message.delete()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id in [
            self.context.author.id
		]:
            return True
        await interaction.response.send_message(
            "This command wasnt ran by you, sorry!", ephemeral=True
        )
        return False

    async def on_timeout(self):
        await self.message.edit("This help menu has expired", view=None, embed=None)
        self.remove_item(Dropdown(self.context, self.h))


class DefaultHelp:
	def __init__(self, ctx) -> None:
		self.context = ctx
		
	async def send_bot_help(self):
		view : DropdownView = DropdownView(ctx=self.context, help=self)
		embedd = discord.Embed(
            title="Help",
            description="```\n[] -> optional\n<> -> required```",
        )
		view.message = await self.context.send(embed=embedd, view=view)
