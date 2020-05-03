import datetime, time, discord, asyncio, json, os, random
from itertools import cycle
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRole, MissingAnyRole

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
token = open("data/token/token.txt", "r").readline()

description = """
I hate my life.
"""

class MyClient(commands.Bot):
    def __init__(self):
        # Initialise bot
        super().__init__(
            command_prefix="+",
            case_insensitive=True,
            owner_id=154622682078380032,
            description=description
        )
        self.add_command(self.load_command)
        self.add_command(self.unload_command)
        self.add_command(self.reload_command)
        # Set up attributes
        self.commands_used = 0
        self.start_time = time.time()
        self.recent = [0 for x in range(7)]
        self.messages = ["Yet another round with nothing interesting happening.", "Soon we'll be home eating red meat and combing innards from our hair.", "Time to do my rounds, I suppose.", "If that smuggler is sneaking about again, I'll have his head on a rusty pike.", "Hey you! I've got my eyes on you. You better not try any funny business around here.", "Oh look! Some rocks! Oh, and some more rocks! It can't get more exciting than this.", "I've got the eyes of a hawk, the ears of a wolf, the speed of a kyatt and an awful day job.", "If I never see another floating eyeball in a hundred years, it'll be too soon."]
        self.bg_task = self.loop.create_task(self.background_loop())
        # Load cogs
        for file in os.listdir("./cogs"):
            try:
                if file.endswith(".py"):
                    self.load_extension(f"cogs.{file[:-3]}")
                    print(f"Loaded: {file}.")
            except Exception as e:
                print(f"Failed to load extension {file}.")

    async def on_ready(self):
        print(f"Online.\nUsername: {self.user.name}\nID: {self.user.id}\n{'-'*27}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for rusty pikes"))

    async def background_loop(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await asyncio.sleep(random.randint(3600, 86400))
            channel = self.get_channel(683818756522115084)
            quote = random.choice(self.messages)
            while quote in self.recent:
                quote = random.choice(self.messages)
            self.recent.pop(0)
            self.recent.append(quote)
            await channel.send(quote)

    async def on_command(self, ctx):
        """Count number of commands used"""
        self.commands_used += 1

    async def on_command_error(self, ctx, error):
        """Handle error on commands"""
        if await ctx.bot.is_owner(ctx.author) or ctx.channel.id in self.allowed_channels:
            if isinstance(error, CommandNotFound):
                await ctx.send("That command didn't work. Please try `+help` for all available commands.")
            raise error
        else:
            if isinstance(error, MissingRole) or isinstance(error, MissingAnyRole):
                await ctx.send("You do not have permission to use that command here.")
            raise error

    async def uptime(self):
        current_time = time.time()
        return str(datetime.timedelta(seconds=(int(round(current_time - self.start_time)))))

    # Commands
    @commands.command(name="load", hidden=True)
    async def load_command(self, *, module):
        """Loads a module."""
        if await self.bot.is_owner(self.author):
            try:
                self.bot.load_extension(f"cogs.{module}")
            except commands.ExtensionError as e:
                await self.send(f"{e.__class__.__name__}: {e}")
            else:
                await self.send(":ok_hand:")

    @commands.command(name="unload", hidden=True)
    async def unload_command(self, *, module):
        """Unloads a module."""
        if await self.bot.is_owner(self.author):
            try:
                self.bot.unload_extension(f"cogs.{module}")
            except commands.ExtensionError as e:
                await self.send(f"{e.__class__.__name__}: {e}")
            else:
                await self.send(":ok_hand:")

    @commands.command(name="reload", hidden=True)
    async def reload_command(self, *, module):
        """Reloads a module."""
        if await self.bot.is_owner(self.author):
            if module == "all":
                text = ""
                for file in os.listdir("./cogs"):
                    try:
                        if file.endswith(".py"):
                            self.bot.unload_extension(f"cogs.{file[:-3]}")
                            self.bot.load_extension(f"cogs.{file[:-3]}")
                            text += f"Loaded: {file}\n"
                    except Exception as e:
                        print(e)
                        text += f"Failed to load extension {file}\n"
                await self.send(text)
            else:
                try:
                    self.bot.unload_extension(f"cogs.{module}")
                    self.bot.load_extension(f"cogs.{module}")
                except commands.ExtensionError as e:
                    print(e)
                    await self.send(f"{e.__class__.__name__}: {e}")
                else:
                    await self.send(":ok_hand:")

if __name__ == "__main__":
    client = MyClient()
    client.run(token)
