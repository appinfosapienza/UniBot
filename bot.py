from youtube_search import YoutubeSearch
from discord.ext.commands import Context
from discord.ext import commands
from discord.utils import get
from datetime import date
import discord.utils
import youtube_dl
import funChest
import random
import time
import os

# ---------------------------------------------- #
# ----------- BOT VARIABLES SECTION ------------ #
# ---------------------------------------------- #

f = open("tokenBot.txt", encoding='utf8')

TOKEN = f.read().strip()  # BOT TOKEN, DO NOT SHARE
COMMAND_PREFIX = "!"

today = str(date.today())
oraUp = time.strftime("%H", time.localtime())
minutiUp = time.strftime("%M", time.localtime())
ruoli = {"abituale": "Abituale", "Abituale": "Abituale", "view-all": "View-All", "View-All": "View-All"}
file_lezione = 'lezioniLockdown.txt'
file_docenti = 'sitiDocenti.txt'
file_ricevimento = 'ricevimentoDocenti.txt'
file_calendario = 'calendario.png'
file_help = 'help.txt'
colore = 0x822434
global list_coda
list_coda = []
global ydl_opts
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
global list_titles
list_titles = []
global nowPlaying
nowPlaying = [""]
global volume
global_volume = [0.5]

random.seed() #Random initialization


# ---------------------------------------------- #
# ----------- BOT STARTUP SECTION -------------- #
# ---------------------------------------------- #


bot = discord.Client()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)


# ----------------------------------------------- #
# ------------ BOT.COMMANDS SECTION ------------- #
# ----------------------------------------------- #

@bot.command(aliases=["Restartbot"])
async def restartbot(ctx: Context):
    message = "I'm self-rebooting (will check for updates during reboot)"
    title = "Service"
    await ctx.channel.send(embed=discord.Embed(title = title, description=message, color=colore))
    os._exit(os.EX_OK)

@bot.command(aliases=["Help"])
async def help(ctx: Context):
    f = open(file_help, encoding='utf8')
    helpStr = f.read()
    titolo = "Unibot 2.0 Help"

    await ctx.channel.send(embed=discord.Embed(title = titolo, description=helpStr, color=colore))


@bot.command(aliases=['Hello'])
async def hello(ctx: Context):
    await ctx.channel.send(embed=discord.Embed(title="Ciao!", description="Come va?", color=colore))


@bot.command(aliases=['Ora'])
async def ora(ctx: Context):
    ora = int(time.strftime("%H", time.localtime()))
    minuti = time.strftime("%M")
    orario = 'Sono le ore ' + str(ora + 1) + ":" + minuti
    await ctx.channel.send(embed=discord.Embed(title="Ora", description=orario, color=colore))


@bot.command(aliases=['Uptime'])
async def uptime(ctx: Context):
    string = 'Sono online dalle ore ' + str(int(oraUp) + 1) + ":" + minutiUp + ' del giorno ' + today
    await ctx.channel.send(embed=discord.Embed(title="Uptime", description=string, color=colore))


@bot.command(aliases=['Roll'])
async def roll(ctx: Context, *args):
    errore = 'I dati inseriti sono errati, utilizzare la formula "!roll LANCIdFACCE", per esempio 1d20 per un lancio di un dado a 20 facce.\n\
                                                           Il massimo di facce e lanci è 200, i valori negativi non vengono accettati.\n'
    istruzioni = 'Utilizzare la formula "!roll LANCIdFACCE", per esempio 1d20 per un lancio di un dado a 20 facce.\n' \
                 'Il massimo di facce e lanci è 200, i valori negativi non vengono accettati.\n'
    try:
        stringok = False
        stringa = args[0]
        stringok = True
        listaDadoRoll = stringa.split('d')
        if int(listaDadoRoll[0]) > 200 or int(listaDadoRoll[1]) > 200 or int(listaDadoRoll[0]) <= 0 or int(
                listaDadoRoll[1]) <= 0:
            await ctx.channel.send(embed=discord.Embed(title="Istruzioni", description=istruzioni, color=colore))
        else:
            resultStrDadi = ''
            rollSomma = 0
            for tiri in range(int(listaDadoRoll[0])):
                rollTemp = random.randint(0, int(listaDadoRoll[1]) - 1)
                resultStrDadi = resultStrDadi + ' ' + str(rollTemp + 1)
                rollSomma += rollTemp + 1
            if int(listaDadoRoll[0]) == 1:
                await ctx.channel.send(
                    embed=discord.Embed(title="Il risultato del lancio è:", description=str(rollSomma), color=colore))
            else:
                await ctx.channel.send(embed=discord.Embed(title="Il risultato del lancio è:",
                                                           description=resultStrDadi + ' ' + '\n' + 'La somma è ' + str(rollSomma),
                                                           color=0x822434))
    except:
        if stringok:
            await ctx.channel.send(embed=discord.Embed(title="Errore", description=errore, color=colore))
        else:
            await ctx.channel.send(embed=discord.Embed(title="Istruzioni", description=istruzioni, color=colore))


@bot.command(aliases=["Lezione", "lezioni", "Lezioni"])
async def lezione(ctx : Context):
    day = date.today().weekday()  # Prende il giorno della settimana
    mese = int(time.strftime("%m", time.localtime()))
    giornoMese = int(time.strftime("%d", time.localtime()))  # Prende il giorno del mese
    ora = int(time.strftime("%H", time.localtime()))
    minuti = int(time.strftime("%M", time.localtime()))

    ora_attuale = (day, ora + 1, minuti, giornoMese, mese)
    lezione = funChest.lezione(file_lezione, ora_attuale)

    await ctx.channel.send(embed=discord.Embed(title="Lezione:", description=lezione, color=colore))


@bot.command(aliases=["Calendario"])
async def calendario(ctx: Context):
    await ctx.channel.send(file=discord.File(file_calendario))


@bot.command(aliases=["Docenti"])
async def docenti(ctx: Context):
    f = open(file_docenti, encoding='utf8')
    link_docenti = f.read()
    titolo = "Siti ufficiali dei docenti, anno 2020/2021, canale 2:"
    await ctx.channel.send(embed=discord.Embed(title=titolo, description= link_docenti, color=colore))


@bot.command(aliases=["Ricevimenti", "ricevimento", "Ricevimento"])
async def ricevimenti(ctx: Context):
    f = open(file_ricevimento, encoding='utf8')
    link_ricevimenti = f.read()
    await ctx.channel.send(embed=discord.Embed(title="Ricevimento:", description=link_ricevimenti, color=colore))


@bot.command(aliases=["Fatti"])
async def fatti(ctx: Context):
    listaFatti = []
    with open('curiosity.txt', encoding='utf-8') as fatti:
        listaFatti = fatti.readlines()
    factValue = random.randint(0, len(listaFatti))
    listaFatti[factValue] = listaFatti[factValue].rstrip()
    await ctx.channel.send(embed=discord.Embed(title="Fatto Curioso", description=listaFatti[factValue], color=colore))


@bot.command(aliases=['F'])
async def f(ctx: Context):
    await ctx.channel.send(embed=discord.Embed(description='**FFFFFFFFFFFFFFFF**\n**F**\n**F**\n**F**\n**FFFFFFFFF**\n**F**\n**F**\n**F**\n**F**\n**F**',
                                               color=colore))


@bot.command(pass_context=True, aliases=['Role'])
async def role(ctx: Context, *args):
    errore = 'Il ruolo richiesto non è presente sul server'
    istruzioni = "**Lista dei ruoli disponibili nel server**" \
                 "\nPer assegnarsi un ruolo usare il comando !role seguito dal nome del ruolo" \
                 "\n**Abituale**: Ruolo dedicato a coloro che sono molto attivi sul server e vogliono aiutare la sua crescita." \
                 "\n**View-All**: Ruolo necessario per visualizzare le chat e le discussioni dei semestri passati\n" \
                 "\nPer rimuovere un ruolo basta scrivere !remove seguito dal nome del ruolo che si vuole rimuovere"
    try:
        stringok = False
        stringa = args[0]
        stringok = True
        rle = get(ctx.message.guild.roles, name=ruoli[stringa])
        await ctx.message.author.add_roles(rle, reason="Richiesto dall'utente")
        ruolo = "Adesso hai il ruolo **"+ ruoli[stringa] +"** e l'accesso alla sezione **Abituali** nel server!\n" + ctx.author.mention + "!"
        await ctx.channel.send(embed=discord.Embed(title="Ruolo assegnato", description= ruolo, color=colore))
    except:
        if stringok:
            await ctx.channel.send(embed=discord.Embed(title="Errore", description=errore, color=colore))
        else:
            await ctx.channel.send(embed=discord.Embed(title="Lista Ruoli", description=istruzioni, color=colore))


@bot.command(aliases=['Remove'])
async def remove(ctx: Context, *args):
    errore = 'Il ruolo richiesto non è presente sul server'
    try:
        stringa = args[0]
        rle = get(ctx.message.guild.roles, name=ruoli[stringa])
        await ctx.message.author.remove_roles(rle, reason="Richiesto dall'utente")
        ruolo = "Hai rimosso il ruolo **"+ ruoli[stringa] +"**\n" + ctx.author.mention
        await ctx.channel.send(embed=discord.Embed(title="Ruolo rimosso", description= ruolo, color=colore))
    except:
        await ctx.channel.send(embed=discord.Embed(title="Errore", description=errore, color=colore))


# ---------------------------------------------- #
# ------------ MUSIC BOT SECTION --------------- #
# ---------------------------------------------- #


@bot.command()
async def play(ctx):
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    # Cerchiamo l'utente che ha richiesto il brano
    user = ctx.message.author
    url = str(ctx.message.content)
    url = url[5:]
    if user.voice == None:
        await ctx.send(embed=discord.Embed(title="Utente non trovato",
                                           description="Prima unisciti ad un canale, dopo fai entrare il bot!",
                                           color=colore))
        return
    # Ci tentiamo di connettere al canale dell'utente
    voice_channel = user.voice.channel
    try:
        await voice_channel.connect()
    except:
        pass
    if url != "":
        # Prendiamo l'istanza voice
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        # Ci ricaviamo il campo di ricerca dell'utente
        song_there = os.path.isfile("song.mp3")
        # Se non ci sono brani in ascolto, cancelliamo l'ultimo brano salvato se presente, altrimenti mettiamo in coda
        if not voice.is_playing() and not voice.is_paused():
            if song_there:
                os.remove("song.mp3")
        else:
            try:
                results = YoutubeSearch(url, max_results=1).to_dict()
            except:
                await ctx.send(embed=discord.Embed(title="Nessun risultato trovato",
                                                   description="Non siamo riusciti a trovare ciò che cercavi\n"
                                                   "Prova ad essere più preciso",
                                                   color=colore))
            list_coda.append(url)
            list_titles.append(results[0]['title'])
            await ctx.send(embed=discord.Embed(title="Brano messo in coda",
                                               description="Il brano **" + results[0]['title'] + "** è stato messo in coda",
                                               color=colore))
            return
        # Analizziamo il campo di ricerca e forniamo il giusto video
        results = YoutubeSearch(url, max_results=1).to_dict()
        if len(results) == 0:
            await ctx.send(embed=discord.Embed(title="Nessun risultato trovato",
                                               description="Non siamo riusciti a trovare ciò che cercavi\n"
                                               "Prova ad essere più preciso",
                                               color=colore))
            return
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            await ctx.send(embed=discord.Embed(title="Attendere...",
                                               description="Sto scaricando il brano **"+ results[0]['title'] +"**\n "
                                                           "Dammi un secondo...\n"
                                                           "**Non richiedere altre canzoni durante questo processo**",
                                               color=colore))
            try:
                url = "https://www.youtube.com" + results[0]['url_suffix']
                info = ydl.extract_info(url, download=False)
            except:
                await ctx.send(embed=discord.Embed(title="Errore",
                                                   description="Inserire un link valido\n"
                                                               "Se il link inserito è valido riprovare più tardi...",
                                                   color=colore))
                return
        # Se la ricerca è andata a buon fine, cambiamo il nome del file e lo mandiamo in esecuzione
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        try:
            voice.play(discord.FFmpegPCMAudio(info['formats'][0]['url'], **FFMPEG_OPTS), after=lambda e: queue(ctx))
            voice.source = discord.PCMVolumeTransformer(voice.source, volume=global_volume[0])
        except:
            await ctx.send(embed=discord.Embed(title="Errore",
                                               description="Ci si è inceppato il disco...",
                                               color=colore))
            return
        nowPlaying[0] = "https://www.youtube.com" + results[0]['url_suffix']
    else:
        await ctx.send(embed=discord.Embed(title="Connesso",
                                           description="Ora scegli un brano!",
                                           color=colore))


# ---GESTIONE DELLA CODA--- #


def queue(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    song_there = os.path.isfile("song.mp3")
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if song_there:
        os.remove("song.mp3")
    if len(list_coda) != 0:
        results = YoutubeSearch(list_coda[0], max_results=1).to_dict()
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = "https://www.youtube.com" + results[0]['url_suffix']
            info = ydl.extract_info(url, download=False)
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        try:
            voice.play(discord.FFmpegPCMAudio(info['formats'][0]['url'], **FFMPEG_OPTS), after=lambda e: queue(ctx))
            voice.source = discord.PCMVolumeTransformer(voice.source, volume=global_volume[0])
            nowPlaying[0] = "https://www.youtube.com" + results[0]['url_suffix']
        except:
            print("Errore nella riproduzione della coda")
            return
        del list_coda[0]
        del list_titles[0]

def svuota_coda():
    list_titles.clear()
    list_coda.clear()


@bot.command(aliases=["clr"])
async def clear(ctx):
    svuota_coda();
    await ctx.send(embed=discord.Embed(title="Coda Svuotata",
                                           description="Nella coda ora non è presente nessun brano",
                                           color=colore))


@bot.command(aliases=["queue"])
async def coda(ctx):
    if len(list_coda) == 0:
        await ctx.send(embed=discord.Embed(title="Coda vuota",
                                           description="Nella coda non è presente nessun brano",
                                           color=colore))
    else:
        stringa = "\n".join(list_titles)
        await ctx.send(embed=discord.Embed(title="Coda",
                                           description=stringa,
                                           color=colore))


@bot.command(aliases = ["NowPlaying"])
async def np(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice.is_playing() and not voice.is_paused():
        await ctx.send(embed=discord.Embed(title="Silenzio....",
                                           description="Il silenzio regna su di noi...",
                                           color=colore))
    else:
        await ctx.send(embed=discord.Embed(title="Ora in riproduzione",
                                       color=colore))
        await ctx.send(nowPlaying[0])


# ---FINE GESTIONE DELLA CODA--- #


@bot.command()
async def volume(ctx, *args):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        volume = args[0]
    except:
        await ctx.send(embed=discord.Embed(title="Volume",
                                           description="Il volume al momento è a " + str(voice.source.volume*100),
                                           color=colore))
        return
    new_volume = float(volume)
    if 0 <= new_volume <= 100:
        global_volume[0] = new_volume / 100
        voice.source.volume = global_volume[0]
        await ctx.send(embed=discord.Embed(title="Volume modificato",
                                           description="Il nuovo volume è impostato a " + str(new_volume),
                                           color=colore))
    else:
        await ctx.send(embed=discord.Embed(title="Errore",
                                           description="Per favore inserire un valore da 0 a 100",
                                           color=colore))


@bot.command(aliases=["next"])
async def skip(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected() and voice.is_playing():
        if len(list_coda) == 0:
            await ctx.send(embed=discord.Embed(title="Riproduzione terminata",
                                               description="I brani in coda sono terminati, aggiungine altri!",
                                               color=colore))
        else:
            await ctx.send(embed=discord.Embed(title="Brano Skippato",
                                               description="Sto scaricando il nuovo brano **" + list_titles[0] + "**\n"
                                                           "Dammi un secondo...\n"
                                                           "**Non richiedere altre canzoni durante questo processo**",
                                               color=colore))
        voice.stop()
    else:
        await ctx.send(embed=discord.Embed(title="Errore",
                                           description="Non c'è nulla in riproduzione al momento",
                                           color=colore))


@bot.command()
async def disconnect(ctx):
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


@bot.command()
async def pause(ctx):
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


@bot.command()
async def resume(ctx):
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


@bot.command()
async def stop(ctx):
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
        await message.channel.send(embed=discord.Embed(description='**FFFFFFFFFFFFFFFF**\n**F**\n**F**\n**F**\n**FFFFFFFFF**\n**F**\n**F**\n**F**\n**F**\n**F**',
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
