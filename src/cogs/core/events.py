import arrow
import disnake
from disnake.ext import commands

from bot import SomeBot
from util.errors import format_exception


class Events(commands.Cog):
    def __init__(self, bot: SomeBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info("Bot is connected and ready!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            retry_after_in = (
                arrow.now().shift(seconds=error.retry_after).humanize(only_distance=True)
            )
            await ctx.reply(f"Cool down! You can use this command again in {retry_after_in}")
        elif isinstance(error, commands.NotOwner):
            await ctx.reply("This command is only available to the bot owners!")
        else:
            error_formatted = format_exception(error)

            self.bot.logger.error(error_formatted)

            debug_info = (
                f"```\n{ctx.author} ({ctx.author.id}): {ctx.message.content}"[:200]
                + f"``````py\n{error_formatted.replace('```', '｀｀｀')}"[: 2000 - 209]
                + "```"
            )

            await ctx.send(debug_info)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            retry_after_in = (
                arrow.now().shift(seconds=error.retry_after).humanize(only_distance=True)
            )
            await inter.send(f"Cool down! You can use this command again in {retry_after_in}")
        elif isinstance(error, commands.NotOwner):
            await inter.send("This command is only available to the bot owners!")
        else:
            error_formatted = format_exception(error)

            self.bot.logger.error(error_formatted)

            debug_info = (
                f"```\n{inter.author} ({inter.author.id}): {inter.application_command.name}"[:200]
                + f"``````py\n{error_formatted.replace('```', '｀｀｀')}"[: 2000 - 209]
                + "```"
            )

            await inter.send(debug_info)


def setup(bot: SomeBot):
    bot.add_cog(Events(bot))
