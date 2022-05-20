import logging

import aiohttp
import aiosqlite
import arrow
import disnake
from disnake.ext import commands

from config import BotConfig, load_config

logging.basicConfig(level=logging.INFO)


class SomeBot(commands.AutoShardedBot):
    def __init__(self, config: BotConfig):
        super().__init__(
            case_insensitive=True,
            help_command=None,
            intents=disnake.Intents.all(),
            command_prefix=config.COMMAND_PREFIX,
        )

        self.config = config

        self.logger = logging.getLogger("bot")

        # these all have to be created later in an async context, see the start method
        self.db: aiosqlite.Connection = None
        self.http_client: aiohttp.ClientSession = None

        self.cog_list = [
            "core.events",
            "commands.owner",
        ]

    async def start(self, *args, **kwargs) -> None:
        async with aiohttp.ClientSession(raise_for_status=True) as self.http_client, aiosqlite.connect(self.config.DATABASE_NAME) as self.db:         
            # load all the cogs
            for cog in self.cog_list:
                self.load_extension(f"cogs.{cog}")
            
            await super().start(*args, **kwargs)

    def run(self) -> None:
        super().run(self.config.DISCORD_BOT_TOKEN)

    def default_embed(self) -> disnake.Embed:
        embed = disnake.Embed(color=disnake.Color.purple())

        embed.timestamp = arrow.utcnow().datetime

        embed.set_footer(text="SomeBot", icon_url=self.user.avatar.url)

        return embed


if __name__ == "__main__":
    SomeBot(load_config()).run()
