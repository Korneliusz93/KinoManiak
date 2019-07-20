import sys, os
from peewee import *

if os.path.exists(':test.db:'):
    os.remove(':test.db:')
# tworzymy instancję bazy używanej przez modele
db = SqliteDatabase(':test.db:') # 'memory'

class Katalog(Model):  # klasa bazowa
    class Meta:
        database = db

#tabela film
class Film(Katalog):
    rok_produkcji = CharField(default='')
    kategoria = CharField(default='')
    tytul = CharField(null=False)

#tabela aktor
class Aktor(Katalog):
    imie = CharField(null=False)
    nazwisko = CharField(null=False)
    wiek = CharField(default='')
    plec = CharField(null=False)
    etnicznosc = CharField(default='')
    film = ForeignKeyField(Film, related_name='aktorzy',null=True)

def InputDodajFilm():
    tyt = input('Podaj tytuł filmu: ')
    rok = input('Podaj rok produkcji: ')
    kat = input('Podaj kategorię: ')
    #sprawdzenie czy film o tytule istnieje
    test = False
    for pozycja in Film.select():
        if tyt == pozycja.tytul: test = True
    #wlasciwy zapis filmu do bazy
    if test is False:
        inst_film = Film(tytul = tyt, rok_produkcji = rok, kategoria = kat)
        inst_film.save()
        return None
    else:
        print('Film jest już w bazie !')

def InputDodajAktora():
    im = input('Podaj imię: ')
    nazw = input('Podaj nazwisko: ')
    lata = input('Podaj wiek: ')
    sex = input('Podaj płeć (k - kobieta, m - mężczyzna): ')
    etn = input('Podaj przynależność etniczną: ')
    fil = input('Podaj film, w którym występował: ')

    test = False

    for persona in Aktor.select():
        if im == persona.imie and nazw == persona.nazwisko:
            print('Aktor o tych personaliach jest już w bazie !')
            return None
    
    for Dzielo in Film.select():
        if fil == Dzielo.tytul:
            test = True
#            print('Test worked positive')
    if test:            
        inst_film = Film.select().where(Film.tytul == fil).get()
        inst_aktor = Aktor(imie = im,nazwisko = nazw, wiek = lata,plec = sex, etnicznosc = etn,film = inst_film)
        test = False
#        print('val test changed to negative')
    else:
        inst_aktor = Aktor(imie = im,nazwisko = nazw, wiek = lata,plec = sex, etnicznosc = etn)
#        print('val negative')
    inst_aktor.save()

#def OdczytajFilm():
#    for film in Film.select():
#        print(film.id, film.tytul, film.rok_produkcji, film.kategoria)

#def OdczytajAktora():
#    for artysta in Aktor.select():
#        print(artysta.id, artysta.nazwisko, artysta.plec, artysta.film.tytul)

def WyszukajFilm():
    ttl = input('Podaj proszę tytuł filmu: ')
    rk = input('Podaj rok produkcji filmu: ')
    ktgr = input('Podaj kategorię filmu: ')
    decyzja = input('1) Zawiera wszystkie Kategorie\n 2) Którąkolwiek z kategorii')

    if decyzja == '2':
        for dzielo in Film.select():
            if dzielo.tytul == ttl or dzielo.rok_produkcji == rk or dzielo.kategoria == ktgr:
                print('ID: ' + str(dzielo.id),'Tytuł: ' + dzielo.tytul,'Rok produkcji: ' + dzielo.rok_produkcji,'Kategoria: ' + dzielo.kategoria, sep='\n')
    if decyzja == '1':
        for dzielo in Film.select():
            if dzielo.tytul == ttl and dzielo.rok_produkcji == rk and dzielo.kategoria == ktgr:
                print('ID: ' + dzielo.id,'Tytuł: ' + dzielo.tytul,'Rok produkcji: ' + dzielo.rok_produkcji,'Kategoria: ' + dzielo.kategoria, sep='\n')

def WyszukajAktora():
    im=input('Podaj proszę imię aktora: ')
    naz=input('Podaj proszę nazwisko aktora: ')
    plc=input('Podaj proszę płeć aktora: ')
    wk=input('Podaj proszę wiek aktora: ')
    etn=input('Podaj proszę etniczność aktora: ')
    flm = input('Podaj film, w którym występował: ')

    for artysta in Aktor.select().join(Film):
        if artysta.imie == im or artysta.nazwisko == naz or artysta.plec == plc or artysta.wiek == wk or artysta.etnicznosc == etn or artysta.film.tytul == flm:
            print('ID: ' + str(artysta.id), artysta.imie,artysta.nazwisko,'Płeć: ' + artysta.plec,'Wiek: ' + artysta.wiek,'Etniczność: ' + artysta.etnicznosc,'Film: ' + artysta.film.tytul, sep='\n')
                    
def UpdateFilm():
    id_ = input('Podaj numer id filmu: ')
    decyzja = input('Co chcesz zmienić?\n1. Tytul\n2. Rok produkcji\n Kategorię\n')
    if decyzja == '1':
        korekta = input('Wprowadz poprawkę: ')
        inst_film = Film.select().where(Film.id == int(id_)).get()
        #inst_film.tytul = Film.select().where(Film.tytul == korekta).get()
        inst_film.tytul = korekta
        inst_film.save()  # zapisanie zmian w bazie
    if decyzja == '2':
        korekta = input('Wprowadz poprawkę: ')
        inst_film = Film.select().where(Film.id == int(id_)).get()
        inst_film.rok_produkcji = korekta
        inst_film.save()  # zapisanie zmian w bazie
    if decyzja == '3':
        korekta = input('Wprowadz poprawkę: ')
        inst_film = Film.select().where(Film.id == int(id_)).get()
        inst_film.kategoria = korekta
        inst_film.save()  # zapisanie zmian w bazie

def UpdateAktor():
    id_ = input('Podaj numer id aktora: ')
    decyzja = input('Co chcesz zmienić? (imie/nazwisko/wiek/etnicznosc/film - dla wystąpienia w filmie)')
    korekta = input('Wprowadz poprawkę: ')
    if decyzja != 'film':
        inst_aktor = Aktor.select().where(Aktor.id == int(id_)).get()
        if decyzja == 'imie':
            inst_aktor.imie = korekta
            inst_aktor.save()  # zapisanie zmian w bazie
        if decyzja == 'nazwisko':
            inst_aktor.nazwisko = korekta
            inst_aktor.save()  # zapisanie zmian w bazie
        if decyzja == 'wiek':
            inst_aktor.wiek = korekta
            inst_aktor.save()  # zapisanie zmian w bazie
        if decyzja == 'etnicznosc':
            inst_aktor.etnicznosc = korekta
            inst_aktor.save()  # zapisanie zmian w bazie
    elif decyzja == 'film':
        inst_aktor = Aktor.select().join(Film).where(Aktor.id == int(id_)).get()
        inst_aktor.film = Film.select().where(Film.tytul == korekta).get()
        inst_aktor.save()  # zapisanie zmian w bazie
    else: print('Brak kategorii ! Podaj poprawną kategorię.')

def Usun():
    wybor = input('Chcesz usunąć:\n 1 - aktora,\n 2 - film\n')
    id_=int(input('Podaj numer ID: '))
    if wybor == '1':
        Aktor.select().where(Aktor.id == id_).get().delete_instance()
    if wybor == '2':
        Film.select().where(Film.id == id_).get().delete_instance()

def Menu():
    print('Co chcesz zrobić?\n 1. Wprowadzic film \n 2. Wprowadzic dane aktora \n 3. Sprawdz filmy\n 4. Sprawdz aktorow\n 5. Edytuj film\n 6. Edytuj aktora\n 7. Usuń wpis\n 0. Wyjscie')
    
db.connect()
db.create_tables([Film, Aktor])  # tworzymy tabele

#SetupDB()
x = 1
while x is not 0:
    Menu()
    x = int(input())
    if x == 1:
        InputDodajFilm()
    elif x == 2:
        InputDodajAktora()
    elif x == 3:
        WyszukajFilm()
    elif x == 4:
        WyszukajAktora()
    elif x == 5:
        UpdateFilm()
    elif x == 6:
        UpdateAktor()
    elif x == 7:
        Usun()

# zmiana klasy ucznia o identyfikatorze 2
#inst_uczen = Uczen().select().join(Klasa).where(Uczen.id == 2).get()
#inst_uczen.klasa = Klasa.select().where(Klasa.nazwa == '1B').get()
#inst_uczen.save()  # zapisanie zmian w bazie

# usunięcie ucznia o identyfikatorze 3
#Uczen.select().where(Uczen.id == 3).get().delete_instance()
