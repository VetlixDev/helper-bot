import nextcord
from nextcord.ext import commands, tasks
from difflib import get_close_matches

PREFIX = 'h!'

intents=nextcord.Intents.all()
client = commands.Bot(command_prefix = PREFIX,intents=intents)

@client.event
async def on_ready():
	print('Bot is Online')
	
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
      cmd = ctx.invoked_with
      cmds = [cmd.name for cmd in client.commands]
      matches = get_close_matches(cmd, cmds)
      if len(matches) > 0:
          embed = nextcord.Embed(title="Invalid Command!", description=f'Command `{str(PREFIX)}{cmd}` not found, maybe you meant `{str(PREFIX)}{matches[0]}`?')
          await ctx.send(embed=embed)
      else:
        embed = nextcord.Embed(title="Invalid Command!", description=f"Please type `{str(PREFIX)}help` to see all commands")
        await ctx.send(embed=embed)
      return
    if isinstance(error,commands.CommandOnCooldown):
      m, s = divmod(error.retry_after, 60)
      h, m = divmod(m, 60)
      if int(h) == 0 and int(m) == 0:
          em = nextcord.Embed(title="**Command on cooldown**", description=f'You must wait `{int(s)}` seconds to use this command!')
          await ctx.send(embed=em)
      elif int(h) == 0 and int(m) != 0:
          em = nextcord.Embed(title="**Command on cooldown**", description=f' You must wait `{int(m)}` minutes and `{int(s)}` seconds to use this command!')
          await ctx.send(embed=em)
      else:
          em = nextcord.Embed(title="**Command on cooldown**", description=f' You must wait `{int(h)}` hours, `{int(m)}` minutes and `{int(s)}` seconds to use this command!')
          await ctx.send(embed=em)
      return
    if isinstance(error, commands.DisabledCommand):
      em = nextcord.Embed(title='Command Disabled', description='It seems the command you are trying to use has been disabled')
      await ctx.send(embed=em)
      return
    if isinstance(error, commands.MissingPermissions):
      missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
      if len(missing) > 2:
          fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
      else:
          fmt = ' and '.join(missing)
      _message = 'You require the `{}` permission to use this command.'.format(fmt)
      em=nextcord.Embed(title='Invalid Permissions', description=_message)
      await ctx.send(embed=em)
      return
    if isinstance(error, commands.BotMissingPermissions):
      missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
      if len(missing) > 2:
          fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
      else:
          fmt = ' and '.join(missing)
      _message = 'I require the `{}` permission to use this command.'.format(fmt)
      em=nextcord.Embed(title='Invalid Permissions', description=_message)
      await ctx.send(embed=em)
      return
    if isinstance(error, commands.BadArgument):
      return
    print(error)

client.run("TOKEN")
