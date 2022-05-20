import os
from disnake.ext import commands

from util.errors import format_exception
from util.code import execute_code

from bot import SomeBot


class OwnerCommands(commands.Cog):
    def __init__(self, bot: SomeBot):
        self.bot = bot

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context):
        os.system("git pull")

        for cog in self.bot.cog_list:
            self.bot.reload_extension(f"cogs.{cog}")

        await ctx.message.add_reaction("✔️")

    @commands.command(name="eval")
    @commands.is_owner()
    async def eval_code(self, ctx: commands.Context, *, stuff: str):
        stuff = stuff.strip(" `\n")

        if stuff.startswith("py"):
            stuff = stuff[2:]

        try:
            result = await execute_code(stuff, {"bot": self.bot, "ctx": ctx})

            await ctx.reply(f"```\n{str(result).replace('```', '｀｀｀')[:2000-9]}```")
        except Exception as e:
            await ctx.reply(f"```py\n{format_exception(e).replace('```', '｀｀｀')[:2000-9]}```")


def setup(bot: SomeBot):
    bot.add_cog(OwnerCommands(bot))
