import guilded
from guilded import Embed
from guilded.ext import commands
import time
import random
from flask import Flask
from threading import Thread
from io import StringIO
import contextlib
import asyncio


app = Flask(__name__)
bot = commands.Bot(command_prefix='!')

@app.route('/')
def index():
    return "Bot test"

def run_flask():
    host = '0.0.0.0'
    port = 3000
    app.run(host=host, port=port)


@bot.event
async def on_ready():
    print(f"{bot.user} ready ({bot.user_id})")


@bot.event
async def deal_with_message(message):
    if message.type is not guilded.MessageType.default or message.author.bot or not message.server:
        return
    if 'lund' in message.content:
        await message.author.ban(reason=f'Said a really bad word in #{message.channel.name}')
        await message.delete()

    elif 'fuck' in message.content.lower() or 'sex' in message.content.lower():
      await message.reply('You can\'t say that!', private=True)
      await message.delete()
    elif 'http://' in message.content or 'https://' in message.content:
      if message.author.guild_permissions.manage_messages:
        return
      else:
        embed = Embed(title = "Link Warning ⚠",description=f"{message.author.mention} sent a link lol, better luck next time")
        embed.set_footer(text=f"Requested by {message.author.display_name}")
        await message.reply(embed=embed)
        await message.delete()

    elif '!ping' in message.content.lower():
      start_time = time.time()
      await message.reply('pong!')
      end_time = time.time()
      latency = (end_time - start_time) * 1000
      await message.reply(f'Reply speed: {latency:.2f} ms')
    elif '!help' in message.content.lower():
      await message.reply('Type !commands to check out the commands')
    elif '!info' in message.content.lower():
      embed = Embed(title = "**SECURITY INFORMATION**",description= '''**Bot Name** : **Security Bot**
      
**Founder** : **Stanny & Guru**

About Security: *Security provides you with a secure way to moderate your server with zero Guilded permissions required. Its limitable usage ensures that no one can take advantage of their privileges, all with the help of a single bot. Make sure your server stays safe, and control when and how users can access your server with Security.*

Support Server: [Security Support Server](https://www.guilded.gg/i/2DlJ3gj2)''')
      embed.set_footer(text=f"Requested by {message.author.display_name}")
      await message.reply(embed=embed)

    elif '!search' in message.content.lower():
      await message.reply('Search that easy thing in google')
    elif '!play rock' in message.content.lower():
      comp = random.choice(['Rock', 'Paper', 'Scissor'])
      if comp == 'Rock':
        await message.reply('''
        AI choice: Rock
        Its a Draw''')
      elif comp == 'Paper':
        await message.reply('''
        AI choice: Paper
        You Lost to me 🤭''')
      elif comp == 'Scissor':
        await message.reply('''
        AI choice: Scissor
        You Won 😎''')
    elif '!play paper' in message.content.lower():
      comp = random.choice(['Rock', 'Paper', 'Scissor'])
      if comp == 'Rock':
        await message.reply('''
        AI choice: Rock
        You Won 😎''')
      elif comp == 'Paper':
        await message.reply('''
        AI choice: Paper
        Its a Draw
        ''')
      elif comp == 'Scissor':
        await message.reply('''
        AI choice: Scissor
        You Lost to me 🤭''')
    elif '!play scissor' in message.content.lower():
      comp = random.choice(['Rock', 'Paper', 'Scissor'])
      if comp == 'Rock':
        await message.reply('''
        AI choice: Rock
        You Lost to me 🤭''')
      elif comp == 'Paper':
        await message.reply('''
        AI choice: Paper
        You Won 😎''')
      elif comp == 'Scissor':
        await message.reply('''
        AI choice: Scissor
        Its a Draw''')
      
    elif 'help' in message.content.lower():
          await message.reply('Cant help unless you specify the problem')
    elif '!kick' in message.content.lower():
      if message.author.guild_permissions.kick_members:
          member_to_kick = message.mentions[0] if message.mentions else None

          if member_to_kick:
              await member_to_kick.kick()
              embed = Embed(title = "User Kicked 😐",description=f"{member_to_kick.mention} has been kicked")
              await message.reply(embed=embed)
          else:
              embed = Embed(title = "Command Error ❌",description=f"Please mention a user to kick")
              await message.reply(embed=embed)
      else:
          embed = Embed(title = "Permission Error ❌",description=f"You don't have permission to kick members")
          await message.reply(embed=embed)

    elif '!ban' in message.content.lower():
        if message.author.guild_permissions.ban_members:
            member_to_ban = message.mentions[0] if message.mentions else None

            if member_to_ban:
                await member_to_ban.ban()
                embed = Embed(title = "User Banned 😈",description=f"{member_to_ban.display_name} has been banned")
                await message.reply(embed=embed)
            else:
                embed = Embed(title = "Command Error ❌",description=f"Please mention a user to ban")
                await message.reply(embed=embed)
        else:
            embed = Embed(title = "Permission Error ❌",description=f"You don't have permission to ban") 
            await message.reply(embed=embed)
    elif '!unban' in message.content.lower():
        if message.author.guild_permissions.ban_members:
            user_id_to_unban_str = message.content.split()[1] if len(message.content.split()) > 1 else None
            if user_id_to_unban_str:
              banned_users = await message.guild.bans()

              banned_user = None
              for ban_entry in banned_users:
                  if str(ban_entry.user.id) == user_id_to_unban_str:
                      banned_user = ban_entry
                      break

              if banned_user:
                  await message.guild.unban(banned_user.user)
                  embed = Embed(title = "User Unbanned 😊",description=f"User with ID {user_id_to_unban_str} has been unbanned")
                  await message.reply(embed=embed)
              else:
                  embed = Embed(title = "Assumption Error ❌",description=f"User with ID {user_id_to_unban_str} is not banned.") 
                  await message.reply(embed=embed)
            else:
                embed = Embed(title = "Command Error ❌",description=f"Please provide the user ID to unban")
                await message.reply(embed=embed)
    elif '!commands' in message.content.lower():
      embed = Embed(title = "**COMMANDS**",description= '''**!ping** - Check the bot's latency
**!info** - Get info about the bot
**!help** - Get help
**!commands** - Get the list of commands
**!search** - Search that easy thing in google
**!play rock** - Play rock paper scissor with the bot
**!play paper** - Play rock paper scissor with the bot
**!play scissor** - Play rock paper scissor with the bot
**!kick** - Kick a user
**!ban** - Ban a user
**!unban** - Unban a user
**!mute** - Mute a user
**!unmute** - Unmute a user
**!warn** - Warn a user
**!unwarn** - Remove warn of a user
**!warns** - Check the warns of a user
**!register** - Register yourself in our game
**!balance** - Check your balance
**!daily** - Get your daily reward
**google1** - Basically the First Result of Google''') 
      embed.set_footer(text=f"Requested by {message.author.display_name}")
      await message.reply(embed=embed)
      
    elif '!mute' in message.content.lower():
        if message.author.guild_permissions.manage_messages:
            member_to_mute = message.mentions[0] if message.mentions else None

            if member_to_mute:
                mute_role = guilded.utils.get(message.server.roles, name='Muted')
                if not mute_role:
                    mute_role = await message.server.create_role(name='Muted')
                await member_to_mute.add_roles(mute_role)
                embed = Embed(title = "User Muted 😶",description=f"{member_to_mute.mention} has been muted")
                await message.reply(embed=embed)
            else:
                embed = Embed(title = "Command Error ❌",description=f"Please mention a user to mute") 
                await message.reply(embed=embed)
        else:
            embed = Embed(title = "Permission Error ❌",description=f"You don't have permission to mute members")
            await message.reply(embed=embed)

    elif '!unmute' in message.content.lower():
        if message.author.guild_permissions.manage_messages:
            member_to_unmute = message.mentions[0] if message.mentions else None

            if member_to_unmute:
                mute_role = guilded.utils.get(message.server.roles, name='Muted')
                if mute_role:
                    await member_to_unmute.remove_roles(mute_role)
                    embed = Embed(title = "User Unmuted 😊",description=f"{member_to_unmute.mention} has been unmuted.") 
                    await message.reply(embed=embed)
                else:
                    embed = Embed(title = "Role Error ❌",description=f"The 'Muted' role doesn't exist.")
                    await message.reply(embed=embed)
            else:
                embed = Embed(title = "Command Error ❌",description=f"Please mention a user to unmute")
                await message.reply(embed=embed)
        else:
            embed = Embed(title = "Permission Error ❌",description=f"You don't have permission to unmute members")
            await message.reply(embed=embed)
    elif 'hacker' in message.content.lower():
      embed = Embed(title = "Hacker Alert ⚠️",description='''If you come to a group and claim yourself to be a hacker (and a powerful one at that) you are publicly declaring to everyone that you are not familiar with the world you claim to be part of. This is a standard rule that does not make exceptions, and idiots like me flaming you will not be a matter of "if" but of "when".''')
      await message.reply(embed=embed)
    elif 'lol' in message.content.lower():
      await message.reply('¯\_(ツ)_/¯')
    elif '!google1' in message.content.lower():
      await message.reply('basically the first result in Google ¯\_(ツ)_/¯')
    elif '!serverinfo' in message.content.lower():
     guild = message.guild
     total_members = guild.member_count
     owner_name = guild.owner.display_name  
     embed = guilded.Embed(title=f"{guild.name} Server Info")
     embed.add_field(name="Total Members", value=total_members, inline=False)
     embed.add_field(name="Server Owner", value=owner_name, inline=False)
     embed.set_footer(text=f"Requested by {message.author.display_name}")
     await message.reply(embed=embed)
    elif message.content.startswith('!userinfo'):
      mentioned_user = message.mentions[0] if message.mentions else message.author
      user_info_embed = guilded.Embed(title=f"User Info - {mentioned_user.display_name}")
      user_info_embed.add_field(name="User ID", value=mentioned_user.id, inline=False)
      if mentioned_user.joined_at:
          user_info_embed.add_field(name="Joined Server", value=mentioned_user.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC"), inline=False)
      else:
          user_info_embed.add_field(name="Joined Server", value="Join date not available", inline=False)

      user_info_embed.set_thumbnail(url=mentioned_user.avatar)

      user_info_embed.set_footer(text=f"Requested by {message.author.display_name}")
      await message.reply(embed=user_info_embed)
    elif '!offtopic' in message.content.lower():
      embed = Embed(title = "**Off Topic**",description= "Click here: [Offtopic](https://en.m.wikipedia.org/wiki/Off_topic)")
      await message.reply(embed=embed)
  
@bot.event
async def on_message(message):
    await deal_with_message(message)

@bot.event
async def on_message_update(before, after):
    await deal_with_message(after)

flask_thread = Thread(target=run_flask)
flask_thread.start()

  
bot.run('gapi_J1HimzuzCGK+YIGbuAp0txvr6lfpbZUSubbccs8hrL94ILMyDEwD5HU30t1yQ+3yC+WYVK1L3OXZVzseEVpasg==')
