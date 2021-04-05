from discord_slash.utils.manage_commands import create_option, create_choice
# from youtube_search import YoutubeSearch
from discord.ext.commands import Context
from discord_slash import SlashCommand
from discord.ext import commands
from discord.utils import get
from datetime import date
import youtube_dl.utils
import discord.utils
import youtube_dl
import funChest
import random
import time
import os

# ---------------------------------------------- #
# ----------- BOT VARIABLES SECTION ------------ #
# ---------------------------------------------- #

# ------------- University section ------------- #

f = open("tokenBot.txt", encoding='utf8')
TOKEN = f.read().strip()

# Command Prefix
COMMAND_PREFIX = "!"

# Uptime variables, when using time in a funtion, don't use this variables
today = str(date.today())
oraUp = time.strftime("%H", time.localtime())
minutiUp = time.strftime("%M", time.localtime())

# Files directories
file_ricevimento = 'ricevimentoDocenti.txt'
file_lezione = 'lezioniLockdown2.txt'
file_calendario = 'calendario.png'
file_docenti = 'sitiDocenti.txt'
file_help = 'help.txt'

# Other variables
colore = 0x822434
random.seed()

# -------------- Music Bot Section -------------- #

# Queue variables
list_queue = []
list_titles = []
nowPlaying = [""]
url_list = []

# Packages variables
youtube_dl.utils.std_headers['Cookie'] = ''
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'}]}
FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
ytlink = "https://www.youtube.com/watch?v="

# Volume variable
global_volume = [0.5]

# ---------------------------------------------- #
# ----------- BOT STARTUP SECTION -------------- #
# ---------------------------------------------- #


# bot = discord.Client()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)
slash = SlashCommand(bot, sync_commands=True)


# ----------------------------------------------- #
# ------------ BOT.COMMANDS SECTION ------------- #
# ----------------------------------------------- #


@bot.command(aliases=["Restartbot"])
async def restartbot(ctx: Context):
    message = "I'm self-rebooting (will check for updates during reboot)"
    title = "Reboot"
    await ctx.send(embed=discord.Embed(title=title, description=message, color=colore))
    os._exit(os.EX_OK)


@slash.slash(name="help", description="Mostra tutti gli slash commands presenti sul server")
async def help(ctx: Context):
    f = open(file_help, encoding='utf8')
    helpStr = f.read()
    titolo = "Unibot 3.0 Help"
    await ctx.send(embed=discord.Embed(title=titolo, description=helpStr, color=colore))


@slash.slash(name="ora", description="Mostra l'ora attuale")
async def ora(ctx: Context):
    ora = int(time.strftime("%H", time.localtime()))
    minuti = time.strftime("%M")
    orario = 'Sono le ore ' + str(ora) + ":" + minuti
    await ctx.send(embed=discord.Embed(title="Ora", description=orario, color=colore))


@slash.slash(name="uptime", description="Mostra l'ora dell'ultimo avvio del bot")
async def uptime(ctx: Context):
    string = 'Sono online dalle ore ' + str(int(oraUp)) + ":" + minutiUp + ' del giorno ' + today
    await ctx.send(embed=discord.Embed(title="Uptime", description=string, color=colore))


@slash.slash(name="roll", description="Rolla un dado virtuale",
             options=
             [
                 create_option
                     (
                     name="dado",
                     description="Inserisci un link o un titolo di un video di youtube",
                     option_type=3,
                     required=False
                 ),
             ])
async def roll(ctx: Context, *dado):
    errore = 'I dati inseriti sono errati, utilizzare la formula "!roll LANCIdFACCE", per esempio 1d20 per un lancio di un dado a 20 facce.\n\
                                                           Il massimo di facce e lanci è 200, i valori negativi non vengono accettati.\n'
    istruzioni = 'Utilizzare la formula "!roll LANCIdFACCE", per esempio 1d20 per un lancio di un dado a 20 facce.\n' \
                 'Il massimo di facce e lanci è 200, i valori negativi non vengono accettati.\n'
    stringok = False
    try:
        stringa = dado[0]
        stringok = True
        listaDadoRoll = stringa.split('d')
        if int(listaDadoRoll[0]) > 200 or int(listaDadoRoll[1]) > 200 or int(listaDadoRoll[0]) <= 0 or int(
                listaDadoRoll[1]) <= 0:
            await ctx.send(embed=discord.Embed(title="Istruzioni", description=istruzioni, color=colore))
        else:
            resultStrDadi = ''
            rollSomma = 0
            for tiri in range(int(listaDadoRoll[0])):
                rollTemp = random.randint(0, int(listaDadoRoll[1]) - 1)
                resultStrDadi = resultStrDadi + ' ' + str(rollTemp + 1)
                rollSomma += rollTemp + 1
            if int(listaDadoRoll[0]) == 1:
                await ctx.send(
                    embed=discord.Embed(title="Il risultato del lancio è:", description=str(rollSomma), color=colore))
            else:
                await ctx.send(embed=discord.Embed(title="Il risultato del lancio è:",
                                                   description=resultStrDadi + ' ' + '\n' + 'La somma è ' + str(
                                                       rollSomma),
                                                   color=0x822434))
    except:
        if stringok:
            await ctx.send(embed=discord.Embed(title="Errore", description=errore, color=colore))
        else:
            await ctx.send(embed=discord.Embed(title="Istruzioni", description=istruzioni, color=colore))


@slash.slash(name="lezione", description="Mostra il link della lezione attuale")
async def lezione(ctx: Context):
    day = date.today().weekday()
    month = int(time.strftime("%m", time.localtime()))
    day_month = int(time.strftime("%d", time.localtime()))
    hour = int(time.strftime("%H", time.localtime()))
    minuts = int(time.strftime("%M", time.localtime()))
    now = (day, hour, minuts, day_month, month)

    lezione = funChest.lezione(file_lezione, now)
    await ctx.send(embed=discord.Embed(title="Lezione:", description=lezione, color=colore))


@slash.slash(name="calendario", description="Mostra un immagine del calendario settimanale")
async def calendario(ctx: Context):
    await ctx.send(embed=discord.Embed(title="Calendario", color=colore))
    await ctx.send(file=discord.File(file_calendario))


@slash.slash(name="docenti", description="Mostra tutti i link delle pagine ufficiali dei docenti del canale")
async def docenti(ctx: Context):
    f = open(file_docenti, encoding='utf8')
    link_docenti = f.read()
    titolo = "Siti ufficiali dei docenti, anno 2020/2021, canale 2:"
    await ctx.send(embed=discord.Embed(title=titolo, description=link_docenti, color=colore))


@slash.slash(name="ricevimento", description="Mostra tutti i link di eventuali ricevimenti online dei docenti")
async def ricevimenti(ctx: Context):
    f = open(file_ricevimento, encoding='utf8')
    link_ricevimenti = f.read()
    await ctx.send(embed=discord.Embed(title="Ricevimento:", description=link_ricevimenti, color=colore))


@slash.slash(name="fatti", description="Fatti curiosi che il bot vuole dirti!")
async def fatti(ctx: Context):
    with open('curiosity.txt', encoding='utf-8') as fatti:
        listaFatti = fatti.readlines()
    factValue = random.randint(0, len(listaFatti))
    listaFatti[factValue] = listaFatti[factValue].rstrip()
    await ctx.send(embed=discord.Embed(title="Fatto Curioso", description=listaFatti[factValue], color=colore))


@slash.slash(name="F", description="F")
async def f(ctx: Context):
    await ctx.send(embed=discord.Embed(
        description='**FFFFFFFFFFFFFFFF**\n**F**\n**F**\n**F**\n**FFFFFFFFF**\n**F**\n**F**\n**F**\n**F**\n**F**',
        color=colore))


@slash.slash(name="role",
             description="Aggiungi al tuo profilo un ruolo del server",
             options=[
                 create_option(
                     name="Ruolo",
                     description="Scegli il ruolo da abilitare:",
                     option_type=3,
                     required=True,
                     choices=[
                         create_choice(
                             name="Abituale: Permette l'accesso alla sezione abituale",
                             value="Abituale"
                         ),
                         create_choice(
                             name="View-All: Permette l'accesso a tutti i canali delle materie passate",
                             value="View-All")
                     ]
                 )
             ])
async def role(ctx: Context, Ruolo: str):
    try:
        rle = get(ctx.guild.roles, name=Ruolo)
        await ctx.author.add_roles(rle, reason="Richiesto dall'utente")
        ruolo = "Adesso hai il ruolo **" + Ruolo + "** e l'accesso alla sezione **Abituali** nel server!\n" + ctx.author.mention + "!"
        await ctx.send(embed=discord.Embed(title="Ruolo assegnato", description=ruolo, color=colore))
    except:
        await ctx.send(embed=discord.Embed(title="Errore", description='Il ruolo richiesto non è presente sul server',
                                           color=colore))


@slash.slash(name="remove",
             description="Comando per disabilitare un tuo ruolo",
             options=[
                 create_option(
                     name="Ruolo",
                     description="Scegli il ruolo da disabilitare:",
                     option_type=3,
                     required=True,
                     choices=[
                         create_choice(
                             name="Abituale",
                             value="Abituale"
                         ),
                         create_choice(
                             name="View-All",
                             value="View-All"
                         )])])
async def remove(ctx: Context, Ruolo: str):
    try:
        rle = get(ctx.guild.roles, name=Ruolo)
        await ctx.author.remove_roles(rle, reason="Richiesto dall'utente")
        ruolo = "Hai rimosso il ruolo **" + Ruolo + "**\n" + ctx.author.mention
        await ctx.send(embed=discord.Embed(title="Ruolo rimosso", description=ruolo, color=colore))
    except:
        await ctx.send(embed=discord.Embed(title="Errore", description='Il ruolo richiesto non è presente sul server',
                                           color=colore))


# ---------------------------------------------- #
# ------------ MUSIC BOT SECTION --------------- #
# ---------------------------------------------- #


@slash.slash(name="play", description="Riproduce un brano da youtube",
             options=
             [
                 create_option(
                        name="Titolo",
                        description="Inserisci un link o un titolo di un video di youtube",
                        option_type=3,
                        required=True
                     ),
             ])
async def play(ctx, url: str):
    # We first search for the user that wrote the message
    user = ctx.author
    # Than we get our query/url (you can use both!)
    if user.voice is None:
        # If the user doesn't stay in any voice channel, we send him a message
        await ctx.send(embed=discord.Embed(title="Utente non trovato",
                                           description="Prima unisciti ad un canale, dopo fai entrare il bot!",
                                           color=colore))
        return
    # Then we try to connect to his channel
    voice_channel = user.voice.channel
    try:
        await voice_channel.connect()
    except:
        # If you have channels that the bot cannot see on your server, you have to manage that code here
        pass
    # We take the "bot voice" instance
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    # Then we search the video on yt
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except:
            try:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
            except:
                await ctx.send(embed=discord.Embed(title="Errore nel reperimento del brano",
                                                   description="Non siamo riusciti a reperire il brano richiesto \n"
                                                               "Prova a formulare la tua richiesta nella forma: \n"
                                                               "'Artista - Titolo Brano'\n",
                                                   color=colore))
                return

    # If we are listening to a song, we add the new song to the queue
    if voice.is_playing() or voice.is_paused():
        list_queue.append(info)
        url_list.append(ytlink + info['id'])
        list_titles.append(info['title'])
        await ctx.send(embed=discord.Embed(title="Brano messo in coda",
                                           description="Il brano **" + info['title'] +
                                                       "** è stato messo in coda",
                                           color=colore))
        return

    await ctx.send(embed=discord.Embed(title="Elaborazione brano",
                                       description="Stiamo elaborando il brano **" + info['title'] + "**\n"
                                                   "Attendere qualche istante...",
                                       color=colore))

    # If all goes as planned while searching the song on youtube, we finally start to play the song
    try:
        voice.play(discord.FFmpegPCMAudio(info['formats'][0]['url'], **FFMPEG_OPTS), after=lambda e: queue(ctx))
        voice.source = discord.PCMVolumeTransformer(voice.source, volume=global_volume[0])
    except:
        await ctx.send(embed=discord.Embed(title="Errore",
                                           description="Ci si è inceppato il disco...",
                                           color=colore))
        return
    nowPlaying[0] = ytlink + info['id']


# ---QUEUE FUNCTIONS--- #


def queue(ctx):
    # This is where our queue gets underway
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if len(list_queue) != 0:
        try:
            voice.play(discord.FFmpegPCMAudio(list_queue[0]['formats'][0]['url'], **FFMPEG_OPTS),
                       after=lambda e: queue(ctx))
            voice.source = discord.PCMVolumeTransformer(voice.source, volume=global_volume[0])
            nowPlaying[0] = url_list[0]
        except:
            print("Errore nella riproduzione della coda")
            return
        del list_queue[0]
        del list_titles[0]
        del url_list[0]


def svuota_coda():
    list_titles.clear()
    list_queue.clear()
    url_list.clear()


@slash.slash(name="clear", description="Rimuove tutti i brani nella coda")
async def clear(ctx):
    if await permessi(ctx):
        svuota_coda()
        await ctx.send(embed=discord.Embed(title="Coda Svuotata",
                                           description="Nella coda ora non è presente nessun brano",
                                           color=colore))


@slash.slash(name="queue", description="Mostra la coda")
async def coda(ctx):
    contatore = 0
    stringa = ""
    if await permessi(ctx):
        if len(list_queue) == 0:
            await ctx.send(embed=discord.Embed(title="Coda vuota",
                                               description="Nella coda non è presente nessun brano",
                                               color=colore))
        else:
            for elemento in list_titles:
                contatore += 1
                stringa += str(contatore) + "- " + elemento + "\n"
            await ctx.send(embed=discord.Embed(title="Coda",
                                               description=stringa,
                                               color=colore))


@slash.slash(name="nowPlaying", description="Mostra il brano attualmente in riproduzione")
async def np(ctx):
    if await permessi(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing() and not voice.is_paused():
            await ctx.send(embed=discord.Embed(title="Silenzio....",
                                               description="Il silenzio regna su di noi...",
                                               color=colore))
        else:
            await ctx.send(nowPlaying[0])


@slash.slash(name="delete", description="Rimuove un brano dalla coda",
             options=
             [
                 create_option(
                     name="Indice",
                     description="Indice del brano da rimuovere (puoi reperire gli indici con il comando queue)",
                     option_type=4,
                     required=True
                 ),
             ])
async def delet(ctx, indi: int):
    if await(permessi(ctx)):
        indice = indi - 1
        if indice < len(list_queue):
            await ctx.send(embed=discord.Embed(title="Brano Skippato",
                                               description="Il brano **" + list_titles[indice] + "** "
                                                                                                 "è stato eliminato dalla coda",
                                               color=colore))
            del list_queue[indice]
            del list_titles[indice]
            del url_list[indice]
        else:
            await ctx.send(embed=discord.Embed(title="Indice inesistente",
                                               description="Non esiste nessun brano con tale indice nella coda",
                                               color=colore))


# ---END OF QUEUE FUNCTIONS--- #


@slash.slash(name="volume", description="Mostra a che livello è il volume e permette di modificarlo",
             options=[
                 create_option(
                     name="Volume",
                     description="Inserisci un valore da 0 a 100",
                     option_type=4,
                     required=False
                 )
             ])
async def volume(ctx, *Volume: int):
    if await permessi(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        try:
            volume = Volume[0]
        except:
            await ctx.send(embed=discord.Embed(title="Volume",
                                               description="Il volume al momento è a " + str(global_volume[0] * 100),
                                               color=colore))
            return
        try:
            new_volume = float(volume)
        except:
            await ctx.send(embed=discord.Embed(title="Errore",
                                               description="Per favore inserire un valore da 0 a 100",
                                               color=colore))
            return
        if 0 <= new_volume <= 100:
            try:
                voice.source.volume = new_volume / 100
                global_volume[0] = new_volume / 100
            except:
                await ctx.send(embed=discord.Embed(title="Errore",
                                                   description="Prima di impostare il volume, riproduci qualcosa!",
                                                   color=colore))
                return
            await ctx.send(embed=discord.Embed(title="Volume modificato",
                                               description="Il nuovo volume è impostato a " + str(new_volume),
                                               color=colore))
        else:
            await ctx.send(embed=discord.Embed(title="Errore",
                                               description="Per favore inserire un valore da 0 a 100",
                                               color=colore))


@slash.slash(name="skip", description="Salta al brano successivo")
async def skip(ctx):
    if await permessi(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_connected() and voice.is_playing():
            if len(list_queue) == 0:
                await ctx.send(embed=discord.Embed(title="Riproduzione terminata",
                                                   description="I brani in coda sono terminati, aggiungine altri!",
                                                   color=colore))
            else:
                await ctx.send(embed=discord.Embed(title="Brano Skippato",
                                                   description="Sto elaborando il nuovo brano **" + list_titles[
                                                       0] + "**\n"
                                                            "Dammi un secondo...",
                                                   color=colore))
            voice.stop()
        else:
            await ctx.send(embed=discord.Embed(title="Errore",
                                               description="Non c'è nulla in riproduzione al momento",
                                               color=colore))


@slash.slash(name="disconnect", description="Disconnette il bot musicale dalla chat vocale")
async def disconnect(ctx):
    if await permessi(ctx):
        svuota_coda()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
            await ctx.send(embed=discord.Embed(title="Ciao ciao",
                                               description="Il bot è stato disconnesso dalla chat vocale",
                                               color=colore))
        else:
            await ctx.send(embed=discord.Embed(title="Errore",
                                               description="Il bot non è connesso a nessuna chat vocale",
                                               color=colore))


@slash.slash(name="pause", description="Mette in pausa il brano in riproduzione")
async def pause(ctx):
    if await permessi(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send(embed=discord.Embed(title="Pausa",
                                               description="Brano messo in pausa",
                                               color=colore))
        else:
            await ctx.send(embed=discord.Embed(title="Errore",
                                               description="Non c'è nulla in riproduzione al momento",
                                               color=colore))


@slash.slash(name="resume", description="Riprende la riproduzione del brano")
async def resume(ctx):
    if await permessi(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send(embed=discord.Embed(title="Brano ripreso",
                                               description="Il brano è stato ripreso",
                                               color=colore))
        elif not voice.is_playing():
            await ctx.send(embed=discord.Embed(title="Errore",
                                               description="Non c'è nulla in riproduzione al momento",
                                               color=colore))
        else:
            await ctx.send(embed=discord.Embed(title="Errore",
                                               description="Il brano non è in pausa",
                                               color=colore))


@slash.slash(name="stop", description="Interrompe la riproduzione e elimina la coda")
async def stop(ctx):
    if await permessi(ctx):
        svuota_coda()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.send(embed=discord.Embed(title="Stop",
                                               description="Brano interrotto",
                                               color=colore))
            voice.stop()
        else:
            await ctx.send(embed=discord.Embed(title="Errore",
                                               description="Non c'è nulla in riproduzione al momento",
                                               color=colore))


async def permessi(ctx):
    user = ctx.author
    if user.voice is None:
        await ctx.send(embed=discord.Embed(title="Errore",
                                           description="Per usare il bot musicale, connettiti ad un canale vocale",
                                           color=colore))
        return False
    else:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice is None:
            await ctx.send(embed=discord.Embed(title="Errore",
                                               description="Per usare questo comando devi prima chiamare il bot "
                                                           "con il comando !play",
                                               color=colore))
            return False
    return True


# ---------------------------------------------- #
# ------------ BOT.EVENT SECTION --------------- #
# ---------------------------------------------- #


@bot.event
async def on_ready():
    print('Bot server started as nickname {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'shootdawnbotter':
        myid = '<@131058082003288064>'
        testo = ' %s Il bot è stato terminato ' % myid
        await message.channel.send(embed=discord.Embed(title="Bot Terminato", description=testo, color=colore))
        await bot.close()

    if message.content == "f" or message.content == "F":
        await message.channel.send(embed=discord.Embed(
            description='**FFFFFFFFFFFFFFFF**\n**F**\n**F**\n**F**\n**FFFFFFFFF**\n**F**\n**F**\n**F**\n**F**\n**F**',
            color=colore))

    if '*' in message.content:
        stringa = message.content.replace('*', 'Ə') + ' #GenderNeutrale'
        await message.channel.send(embed=discord.Embed(title="#GenderNeutrale", description=stringa, color=colore))

    if message.channel.id == 816773641572057119:
        descrizione = ""
        channel = bot.get_channel(776145787566161980)
        titolo = message.content.split("\n")
        for elemento in titolo[1:]:
            descrizione += elemento + "\n"
        await channel.send(embed=discord.Embed(title=titolo[0], description=descrizione, color=colore))
    await bot.process_commands(message)


bot.run(TOKEN)
