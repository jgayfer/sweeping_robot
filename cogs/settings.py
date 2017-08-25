import asyncio

from discord.ext import commands
import discord

from db.dbase import DBase
from cogs.utils.messages import MessageManager


class Settings:

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, new_prefix):
        """
        Change the server's command prefix (admin only)

        Ex. '!setprefix $'
        """
        manager = MessageManager(self.bot, ctx.author, ctx.channel, [ctx.message])

        if len(new_prefix) > 5:
            await manager.say("Prefix must be less than 6 characters.")
            return await manager.clear()

        with DBase() as db:
            db.set_prefix(ctx.guild.id, new_prefix)
            await manager.say("Command prefix has been changed to " + new_prefix)
            return await manager.clear()


    @setprefix.error
    async def setprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            manager = MessageManager(self.bot, ctx.author, ctx.channel, [ctx.message])
            await manager.say("Oops! You didn't provide a new prefix.")
            await manager.clear()


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def togglecleanup(self, ctx):
        """
        Toggle command message cleanup on/off (admin only)

        When enabled, command message spam will be deleted a few seconds
        after a command has been invoked. This feature is designed to
        keep bot related spam to a minimum. Only non important messages will
        be deleted if this is enabled; messages like the help message or the
        roster, for example, will not be removed.
        """
        manager = MessageManager(self.bot, ctx.author, ctx.channel, [ctx.message])

        with DBase() as db:
            db.toggle_cleanup(ctx.guild.id)
            cleanup = db.get_cleanup(ctx.guild.id)
            status = 'enabled' if cleanup else 'disabled'

            await manager.say("Command message cleanup is now *{}*".format(status))
            return await manager.clear()
