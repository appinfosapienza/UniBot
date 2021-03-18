def lezione(file_lezioni, parametriOrario):
    """
        Funzione che prendendo in input il file contente le lezioni e la tupla dell'orario corrente
        restituisce il link della lezione in corso, altrimenti avverte che non ci sono lezioni
    """
    str_lezione = ''
    semestre, calendario, diz_lezioni = lettura_file(file_lezioni)       # ritorna le strutture dati nella struttura che servono

    ora = time_lezione(calendario, semestre, parametriOrario)            
    
    if isinstance(ora, str): return ora                                  # ritorna una stringa se non c'è lezione, in cui avverte in quale periodo siamo, altrimenti un numero (chiave)

    return diz_lezioni[ora]                                              # ritorna il link tramite il dizionario lezione, di cui 'ora' è la chiave

#-------------------------------------------------------------#
#--------------FUNZIONI DI SUPPORTO A def LEZIONE-------------#
#-------------------------------------------------------------#

def lettura_file(file_lezione):
    """
        Funzione che prende in input il file lezione e gestische i dati  per impacchettarli nelle
        strutture necessarie da restituire quali: semestre, calendario (settimanale), lista_lezioni (link)
    """     
    l_lezioni = []                                         
    t_calendario = []

    f = open(file_lezione, encoding='utf8')                                 # lettura file
    file = f.readlines()
                                                                            
    for line in file:                                                       # ciclo per ogni linea del file, e a seconda del token iniziale faccio un operazione diversa
        line = line.strip()

        if line.startswith(('-','#','>')):                                  # controllo solo le linee che sono utili
            if line.startswith('#'):                                        # linee che contengono l'orario settimanale ed iniziano per '#'
                line = line[1:]                
                t_calendario.append(line)               

            elif line.startswith('-'):                                      # linee che contengono i link della lezione
                line = line[1:].split('>')                                  
                l_lezioni.append([line[0], line[1]])
            
            elif line.startswith('>'):                                      # linea che contiente la durata del semestre
                semestre = line[1:].split('-')
                semestre = list(map(int,semestre[0].split('/') + semestre[1].split('/')))
                semestre = [(semestre[1],semestre[0],)] + [(semestre[3],semestre[2],)]


    calendario = inizializzazione_calendario(t_calendario)                  # restituisce un diz della settimana, trasformando il precedente array
    lezioni = inizializzazione_lezioni(l_lezioni)                           # restituisce un diz delle lezioni, trasformando il precedente array

    return  semestre, calendario, lezioni 
    
def inizializzazione_calendario(orari):
    """
     Funzione che prende in ingresso un'array di stringhe contenti orari settimanali e li trasforma 
     in un dizionario con chiave il numero del giorno, e valore un array di tuple: [(ora_lezione_inizio, n° lezione), fine_lezione]
    """

    diz_giorni = {'LUNEDI': 0, 'MARTEDI':1, 'MERCOLEDI':2, 'GIOVEDI':3, 'VENERDI':4}  # dizionario per impostare i giorni della settimana
    diz_orari = {}
    conta = 1
    lung = len(orari)   
    
    i = 0
    while i < lung:
        elem = orari[i]
        
                                            
        if elem in diz_giorni.keys():                                           # mette il giorno della settimana come chiave del dizionario
            keys = diz_giorni[elem]
            diz_orari[keys] = diz_orari.get(keys,[])
        
        elif i+1 < lung and orari[i+1] in diz_giorni.keys() or i == lung-1:     # se è l'ultimo orario del giorno, è l'orario di fine lezione e non va in una tupla
            i +=1 
            diz_orari[keys] += [float(elem)]
            continue                                                            # riprende da capo il ciclo con l'elemento successivo
        
        elif i < lung-1:
            diz_orari[keys] += [(float(elem),conta)]                            # costruzione della tupla (orario, numero_lezione)     
            conta +=1
        
        i +=1
                         
    return diz_orari

def inizializzazione_lezioni(lezioni_array):
    """
    Riceve un array contente: [[numeri,link],[numeri,link]...] e lo trasforma in un dizionario
    con chiave l'id della lezione e nel valore la stringa contente uno o più link
    """
    diz_lezioni = {}

    for elem in lezioni_array:                                                 # ciclo per tutto l'array contente i link
        elem[0] = list(map(int, elem[0].split(',')))                           # prendo i numeri prima del link, li splitto per far di ognuno di essi una chiave, e successicamente converto in interi
        for num in elem[0]:                                                    # ciclo per tutti i numeri
            if num not in diz_lezioni.keys():
                diz_lezioni[num] = diz_lezioni.get(num,elem[1])                # aggiungo alla chiave il link 
            else:                                                       
                diz_lezioni[num] += '\nIn contemporanea a:\n' + elem[1]        # nel caso vi siano più lezioni in contemporanea le aggiungo allo stesso orario


    return diz_lezioni

def time_lezione(diz_day, semestre, parametriOrario):
    """
     Funzione che restituisce, dato un calendario e l'orario attuale, l'identificativo (id, numero) della lezione in corso, altrimenti avverte che non ci sono lezioni con una lunga stringa
    """
    day, ore, minuti, giornoMese, mese = parametriOrario
   
    #controlli se stiamo in periodo di sessione o vancaze  
    if not (semestre[0] <= (mese, giornoMese) <= semestre[1]):  
        ms = ''
        if mese == 12:
            return "Sono iniziate le vacanze natalizie! Vai a mangiare il panettone!! Perché non c'è nessuna lezione qui! (anche se io preferisco il pandoro)! E... Auguri!"
        if mese == 8:
            ms = 'Se invece hai finito la sessione... Sono iniziate le vancaze estive!!! DAJEE! Tutti ar mare!' 
        return "Non ci sono lezioni! Studia e in bocca al lupo per gli esami! \n" + ms

    # controllo se si è in giorno di lezione o meno (nel calendario non c'è il giorne della settimana, oppure è vuoto)
    if not day in diz_day.keys() or len(diz_day[day]) == 0: return "Non è giorno di lezione oggi, per caso ieri sera hai alzato un po' troppo il gomito? Prenditi un po' riposo! O studia ;)"

    hour_attuale = float(str(ore) + '.' + str(minuti))                      # prendo l'ora attuale
    lista_lezioni = diz_day[day]                                            # prendo la lista delle lezioni del giorno

    # controlli sull'orario di chiamata: restituisco una stringa che dice a che ora sono finite o inizieranno le lezioni del giorno
    if hour_attuale > lista_lezioni[len(lista_lezioni) - 1]: return "Le lezioni sono finite alle ore " + "**" + str(lista_lezioni[len(lista_lezioni) - 1]) + "0**!"
    if hour_attuale < lista_lezioni[0][0]: return "E'ancora troppo presto! I link saranno disponibili dalle ore " + "**" + str(lista_lezioni[0][0]) + "0**!"

    num = 0                                                                 # controllo del numero id della lezione
    for lezione in lista_lezioni:
        if isinstance(lezione, tuple) and hour_attuale >= lezione[0]:
            num = lezione[1]

    return num