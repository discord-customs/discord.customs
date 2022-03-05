import discord
from typing import *
from .command import Command


class SlashResponse:
    def __init__(
        self,
        content: Optional[str] = None,
        tts: bool = False,
        embeds: Optional[List[discord.Embed]] = None,
        embed: Optional[discord.Embed] = None,
        allowed_mentions: Optional[discord.AllowedMentions] = None,
        ephemeral: Optional[bool] = False,
        delete_after: Optional[int] = None,
    ) -> None:
        self.content = content
        self.tts = tts
        self.embeds = embeds
        self.embed = embed
        self.allowed_mentions = allowed_mentions
        self.ephemeral = ephemeral
        self.delete_after = delete_after
        if self.embeds and self.embed:
            raise RuntimeError("Cannot have `embeds` and `embed` set at the same time.")

    def to_dict(self):
        embeds = []
        data = {"tts": self.tts}
        if self.embeds:
            for embed in self.embeds:
                embeds.append(embed.to_dict())
            data["embeds"] = embeds
        if self.ephemeral is True:
            data["flags"] = 64
        if self.embed:
            embeds.append(self.embed.to_dict())
            data["embeds"] = embeds
        if self.allowed_mentions:
            data["allowed_mentions"] = self.allowed_mentions.to_dict()
        if self.content:
            data["content"] = self.content
        return data


class SlashType:
    default = slash = 1
    user = 2
    message = 3


class SlashOptionType:
    string = 3
    boolean = 5
    user = 6
    channel = 7
    role = 8
    mentionable = 9
    float = 10


class SlashChoice:
    def __init__(self, name: str, value: Any) -> None:
        self.name = name
        self.value = value


class SlashOption:
    def __init__(
        self,
        type: SlashOptionType,
        name: str,
        description: str,
        required: bool = False,
        choices: List[SlashChoice] = None,
    ) -> None:
        self.type = type
        self.name = name
        self.required = required
        self.choices = choices
        self.description = description


class SlashOptionValue:
    def __init__(self, name: str, value: Any) -> None:
        self.name = name
        self.value = value


class SlashCommand(Command):
    def __init__(
        self,
        name: str = None,
        callback: Coroutine = None,
        description: str = None,
        args=None,
        feature=None,
        options: List[SlashOption] = None,
    ):
        """Initiation of the class

        Args:
            name (str, optional): _description_. Defaults to None.
            callback (Coroutine, optional): _description_. Defaults to None.
            description (str, optional): _description_. Defaults to None.
            args (List, optional): _description_. Defaults to None.
            feature (Feature, optional): _description_. Defaults to None.
        """
        super().__init__(name, callback, description, args, feature)
        self.responder: discord.webhook.async_.AsyncWebhookAdapter = discord.webhook.async_.async_context.get()
        self.data: dict = {"type": 4}
        self.options = options

    async def __call__(self, ctx, *args, **kwargs):
        return await self.callback(ctx, *args, **kwargs)

    async def respond(self, ctx, response: SlashResponse):
        self.responded = True
        interaction: discord.Interaction = ctx.interaction
        self.data["data"] = response.to_dict()
        route = discord.http.Route("POST", f"/interactions/{interaction.id}/{interaction.token}/callback")
        await ctx.bot.http.request(route, headers={"Content-Type": "application/json"}, json=self.data)
        return await self.get_original_response(ctx)

    async def get_original_response(self, ctx):
        interaction: discord.Interaction = ctx.interaction
        route = discord.http.Route(
            "GET",
            f"/webhooks/{(await ctx.bot.application_info()).id}/{interaction.token}/messages/@original",
        )
        resp = await ctx.bot.http.request(route, headers={"Content-Type": "application/json"})
        return discord.Message(
            state=ctx.bot._connection,
            channel=(await ctx.bot.fetch_channel(resp["channel_id"])),
            data=resp,
        )

    async def edit_original_response(self, ctx, response: SlashResponse):
        data = response.to_dict()
        interaction: discord.Interaction = ctx.interaction
        route = discord.http.Route(
            "PATCH",
            f"/webhooks/{(await ctx.bot.application_info()).id}/{interaction.token}/messages/@original",
        )
        resp = await ctx.bot.http.request(route, headers={"Content-Type": "application/json"}, json=data)
        return discord.Message(
            state=ctx.bot._connection,
            channel=(await ctx.bot.fetch_channel(resp["channel_id"])),
            data=resp,
        )

    async def delete_original_response(self, ctx):
        interaction: discord.Interaction = ctx.interaction
        route = discord.http.Route(
            "DELETE",
            f"/webhooks/{(await ctx.bot.application_info()).id}/{interaction.token}/messages/@original",
        )
        resp = await ctx.bot.http.request(route, headers={"Content-Type": "application/json"})


class SlashContext:
    def __init__(
        self,
        bot: discord.Client = None,
        interaction: discord.Interaction = None,
        command: SlashCommand = None,
    ):
        self.channel = interaction.channel
        self.guild = interaction.guild
        self.author = interaction.user
        self.message = interaction.message
        self.bot = bot
        self.interaction = interaction
        self.command = command

    async def __call__(self):
        return await self.command(self)

    async def respond(self, response: SlashResponse):
        return await self.command.respond(self, response)
