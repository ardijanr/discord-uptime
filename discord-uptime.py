from ping3 import ping
from discord.ext import commands
import discord
import asyncio
import json

bot = commands.Bot(command_prefix='>', description='Bot to monitor uptime of services')
currently_down = []

with open('servers.json') as f:
    servers = json.load(f)

with open('config.json') as f:
    config = json.load(f)


@bot.event
async def on_ready():
    print('Logged in as {0}'.format(bot.user))


async def monitor_uptime():
    await bot.wait_until_ready()
    channel = bot.get_channel(config['notification_channel'])

    while not bot.is_closed():
        for i in servers:
            if ping(i["address"]) is None:
                if not i["address"] in currently_down:
                    currently_down.append(i["address"])
                embed = discord.Embed(
                    title='**{0} is down!**'.format(i['name']),
                    description='Error pinging {0} <@&{1}>'.format(i['address'], config['role_to_mention']),
                    color=discord.Color.red()
                )
                await channel.send(embed=embed)
            else:
                if i["address"] in currently_down:
                    embed = discord.Embed(
                        title='**{0} is now up!**'.format(i['name']),
                        description='Successfully pinged {0} <@&{1}>'.format(i['address'], config['role_to_mention']),
                        color=discord.Color.green()
                    )
                    await channel.send(embed=embed)
                    currently_down.remove(i["address"])
                else:
                    if config['always_notify'] is True:
                        await channel.send('Received response from {0} in: '.format(i['address']) + str(
                            int(ping(i['address'], unit='ms'))) + 'ms')
        await asyncio.sleep(config['secs_between_ping'])


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.CommandNotFound, commands.BadArgument, commands.MissingRequiredArgument)):
        return await ctx.send(error)
    else:
        return


@bot.command(brief="Pings an address - status <address> [pings]")
async def status(ctx, address: str, pings: int = 1):
    """
    :param ctx:
    :param address: Address to ping
    :param pings: Number of pings
    :return: Delay in milliseconds
    """
    for i in range(pings):
        await ctx.send(f"Received response from {address} in: {str(int(ping(address, unit='ms')))}ms.")
        await asyncio.sleep(1)

bot.loop.create_task(monitor_uptime())
bot.run(config['token'])
