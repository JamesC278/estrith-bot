import discord, asyncio, random
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_sent = f""

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if (self.bot.user.mentioned_in(message)
            and message.mention_everyone is False):
            if "I've got my eyes" in self.last_sent:
                text = "Time to do my rounds, I suppose."
                self.last_sent = text
                await message.channel.send(text)
            else:
                text = (f"Hey {message.author.mention}! I've got my eyes on "
                    f"you. You better not try any funny business around here.")
                self.last_sent = text
                await message.channel.send(text)
            await message.add_reaction('👀')

    # Commands
    @commands.command(name="invite", aliases=["inv"])
    async def permanent_invite_command(self, ctx):
        """Invite me to your server"""
        await ctx.send(("__**You can use the following link to invite me to "
            f"your server:**__\n<https://discordapp.com/api/oauth2/authorize?"
            f"client_id=705016151842750535&permissions=6144&scope=bot>"))

    @commands.command(name="hello")
    async def send_hello(self, ctx):
        """Get a lovely reply from me"""
        quote = random.choice(self.bot.messages)
        while quote in self.bot.recent:
            quote = random.choice(self.messages)
        self.bot.recent.pop(0)
        self.bot.recent.append(quote)
        await ctx.send(quote)

    @commands.command(name="uptime", aliases=["up"])
    async def uptime_command(self, ctx):
        """Shows the total uptime of the bot"""
        await ctx.send((f"<:online:705690474882793473> I've been hating my "
            f"life for: {await ctx.bot.uptime()}"))

    @commands.command(name="mintime", aliases=["set_min"], hidden=True)
    async def set_lower_boundary(
        self,
        ctx,
        hours: int
    ):
        if await ctx.bot.is_owner(ctx.author):
            self.bot.min_time = hours * 3600
            await ctx.send(f"{self.bot.min_time} seconds minimum")

    @commands.command(name="maxtime", aliases=["set_max"], hidden=True)
    async def set_upper_boundary(
        self,
        ctx,
        hours: int
    ):
        if await ctx.bot.is_owner(ctx.author):
            self.bot.max_time = hours * 3600
            await ctx.send(f"{self.bot.max_time} seconds maximum")

def setup(bot):
    bot.add_cog(Core(bot))
