# Author: Petri Jehkonen (at) xiphera.com

import random, math, string, glob, os
from random import choices
import numpy as np
from numpy import binary_repr
import matplotlib.pyplot as plt
import pprint
from scipy.interpolate import interp1d
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import statsmodels.api as sm
import warnings
from datetime import date
from datetime import datetime
from dateutil import relativedelta


def salaa_merkeittäin(viesti=None, avain=0x6A, debugging=False):
    if viesti is None:
        viesti = "Kahvi Charlotassa on hyvää ja vahvaa!"

    # Unicodesta Latin-1 koodaukseen ja tavuihin, tekninen seikka, ei oleellista
    b_viesti = bytes(viesti, encoding="latin_1")
    # Paikka enkoodatulle viestille
    c_enkoodattu = []

    # Suoritetaan salaus merkeittäin
    for tavu in b_viesti:
        if debugging:
            print("Merkki  {}".format(chr(tavu)))
            print("Bitit   {}".format(binary_repr(tavu,8)))
            print("Avain   {}".format(binary_repr(avain,8)))
            print("XOR     {}".format(binary_repr(avain^tavu,8)))
            print("Sala    {}".format(chr(avain^tavu)))
        c_enkoodattu.append(avain^tavu)

    if debugging:
        print("Viesti joka enkoodataan on:")
        print(viesti+"\n")

        print("Avain jota käytämme salauksessa on:",hex(k),"\n")

        print("Tavuittain enkoodattu viesti näyttää seuraavalta:")
        for tavu in c_enkoodattu:
            print(chr(tavu),end='')
    return c_enkoodattu


def vertaa_maailmankaikkeuden_ikään(avaimiin_kuluva_aika_a):
    # Verrataan maailmankaikkeuden arveltuun ikään.
    maailmankaikkeudenikä_vuosina = 13787000000
    print("Maailmankaikkeuden ikä vuosina: {} vuotta.".format(maailmankaikkeudenikä_vuosina))

    kertaa_maailmankaikkeuden_ikä= avaimiin_kuluva_aika_a/maailmankaikkeudenikä_vuosina
    print("Avainten laskenta vaatii {:.3e} -kertaa maailmankaikkeuden iän.".format(kertaa_maailmankaikkeuden_ikä))

    erotus = avaimiin_kuluva_aika_a - maailmankaikkeudenikä_vuosina

    if erotus <0:
        print("Tämä olisi keretty laskemaan maailmankaikkeuden arvioidussa elinajassa")
    else:
        if erotus>20000:
            print("Ihmisellä ei ole ollut mitään toivoa laskea tätä avainta")
        else:
            print("Ihmiskunta olisi kerennyt jääkauden jälkeen laskemaan avaimen")


def avaimen_laskemiseen_kuluva_aika(bittejä=None, avainta_sekunnissa=None, debugging=False):
    # Tuotetaan avainten määrä, voit vaihtaa bittimäärää.
    if bittejä is None:
        bittejä = 128

    if avainta_sekunnissa is None:
        avainta_sekunnissa=10**12


    avainten_lukumäärä = 2**bittejä
    avaimiin_kuluva_aika_s = avainten_lukumäärä/avainta_sekunnissa # sekunteina
    avaimiin_kuluva_aika_a = avaimiin_kuluva_aika_s/(60*60*24*365) # vuosina
    print("{}-bittisen avaimen laskemiseen nopeudella {:.2e} avainta sekunnissa,".format(bittejä,avainta_sekunnissa))
    print("kuluu {:.3e} vuotta".format( avaimiin_kuluva_aika_a))
    return avaimiin_kuluva_aika_a


def nist112bits_diff(debugging=False):
    nist_112bits = date.fromisoformat('2015-01-01')
    tänään = date.today()
    ero_kuukausia = (tänään.year-nist_112bits.year)*12 + tänään.month-nist_112bits.month
    if debugging:
        print("Ero kuukausina:",ero_kuukausia)

    mooren_laki_kk = 18
    bittiä_lisää = ero_kuukausia//mooren_laki_kk
    if debugging:
        print("Tarvitaan {} bittiä lisää.".format(bittiä_lisää))
    return bittiä_lisää


def näytäkorrelaatiot(data, siirrokset=40, otsikko="Ei otsikkoa"):
    fig, ax = plt.subplots(1,2,figsize=(10,5))
    sm.graphics.tsa.plot_acf(data, lags=siirrokset, ax=ax[0])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sm.graphics.tsa.plot_pacf(data, lags=siirrokset, zero=True, ax=ax[1])
    plt.suptitle("{}".format(otsikko))
    plt.show()


def tuotajakaumia(n=10000):
    x  = np.arange(n)
    y1 = np.arange(n)
    nolla_ysi = [0,1,2,3,4,5,6,7,8,9]
    y2 = np.repeat(nolla_ysi,int(n/len(nolla_ysi)))
    y3 = np.random.normal(int(n/2), int(n/7), n).astype(int)
    y4 = np.random.randint(0,n,n)

    return y1, y2, y3, y4


def heittelyt(noppa=None, kolikko=None, n=4000000, siemen=20211221, n_bins=3):

    if (noppa is None and kolikko is None) or (noppa and kolikko):
        print("Anna joko noppa=True tai kolikko=True")
        return "En ymmärrä"

    if kolikko:
        max_luku = 2
        x_paikat = np.array([0.2, 0.8])
        x_labelit=['Kruuna','Klaava']
        label = "Kolikon"
    else:
        max_luku = 6
        #x_paikat = np.arange(0, max_luku)
        x_paikat = np.array([0.22, 1.15, 2.05, 2.98, 3.85, 4.8])
        x_labelit=['1','2', '3', '4', '5', '6']
        n_bins=11
        label = "Nopan"
    # Asetetaan siemen
    np.random.seed(siemen)

    # Luodaan neljä otosta
    y1 = np.random.randint(0,max_luku,n)
    y2 = np.random.randint(0,max_luku,n)
    y3 = np.random.randint(0,max_luku,n)
    y4 = np.random.randint(0,max_luku,n)

    fig, axes = plt.subplots(2, 2, figsize=(9,9), sharex=False, sharey=False)
    fig.suptitle('{} heittokertojen vertailu histogrammeilla n ={}'.format(label,n))
    axes[0, 0].hist(y1, bins=n_bins)
    axes[0, 0].set_title('Ensimmäinet {} heittoa'.format(n))
    axes[0, 1].hist(y2, bins=n_bins)
    axes[0, 1].set_title('Toiset {} heittoa'.format(n))
    axes[1, 0].hist(y3, bins=n_bins)
    axes[1, 0].set_title('Kolmannet {} heittoa'.format(n))
    axes[1, 1].hist(y4, bins=n_bins)
    axes[1, 1].set_title('Neljännet {} heittoa'.format(n))

    for ax in axes.flat:
        ax.set_xticks(x_paikat)
        ax.set_xticklabels(x_labelit)

    for ax in axes.flat:
        ax.set(xlabel='Tulos', ylabel='Lukumäärä')

    fig.tight_layout()
    plt.show()


def näytäjakaumia(n_bins=50):
    # Luodaan neljä jakaumaa joissa n-kpl näytteitä
    n  = 10000

    y1, y2, y3, y4 = tuotajakaumia()

    fig, axes = plt.subplots(2, 2, figsize=(12,6), sharex=False, sharey=False)
    fig.suptitle('Jakaumien vertailu histogrammeilla n ={} | bins={}'.format(n,n_bins))
    axes[0, 0].hist(y1, bins=n_bins)
    axes[0, 0].set_title('Tasajakauma')
    axes[0, 1].hist(y2, bins=n_bins)
    axes[0, 1].set_title('Toistuva')
    axes[1, 0].hist(y3, bins=n_bins)
    axes[1, 0].set_title('Normaalijakauma')
    axes[1, 1].hist(y4, bins=n_bins)
    axes[1, 1].set_title('Tasajakauma')

    for ax in axes.flat:
        ax.set(xlabel='Satunnaismuuttujan arvo', ylabel='Lukumäärä')

    fig.tight_layout()
    plt.show()


def salain_a(viesti):
    return atbash(viesti)


def atbash(viesti="Kahvi Charlotassa on hyvää ja vahvaa"):
    substituutio = atbash_substituutio()
    muunnos = []
    for kirjain in viesti:
        if substituutio.get(kirjain)==None:
            muunnos.append(' ')
        else:
            muunnos.append(substituutio.get(kirjain))
    return "".join(muunnos)


def atbash_substituutio():
    kirjaimet = string.ascii_uppercase + 'ÅÄÖ'
    substituutio = dict(zip(kirjaimet,kirjaimet[::-1]))
    return substituutio


def salain_b(viesti, avain):
    isot, pienet = merkistot(suomi=True)
    return caesar(viesti,aakkosto=isot, avain=avain)

def caesar(esikäsitelty_teksti, aakkosto=None, avain=3, purku=False, debuggaus=False):

    if debuggaus:
        print("Saatiin viesti ", esikäsitelty_teksti)

    pienet = ""
    if aakkosto is None:
        print("Aakkostoa ei annettu, valitaan suomen aakkoset!")
        aakkosto, pienet = merkistot(suomi=True)

    if debuggaus:
        print("Aakkosto on ", aakkosto)

    # Jos argumentiksi annetaan suoraan tekstiä, se ei välttämättä ole esikäsitelty, tehdään esikäsittely.
    esikäsitelty_teksti = esikasittele_teksti(esikäsitelty_teksti,aakkosto+pienet)

    if debuggaus:
        print("Muunnettava viesti",esikäsitelty_teksti)

    # Lista johon laitetaan muunnoksen tulos
    muunnettu_teksti = []
    # Muunnos suoritetaan merkki merkiltä
    for kirjain in esikäsitelty_teksti:
        # Aakkoston oletetaan olevan järjestetty ja sisältää vain isot kirjaimet
        # Käsiteltävän kirjaimen suhteellinen paikka aakkostossa
        ennen_muunnosta = aakkosto.index(kirjain)-aakkosto.index(aakkosto[0])
        # Tässä suoritetaan muunnoksen indeksi laskenta
        if not purku:
            muunnoksen_jälkeen=(ennen_muunnosta+avain)%len(aakkosto)
        else:
            muunnoksen_jälkeen=(ennen_muunnosta-avain)%len(aakkosto)

        # Lisätään muunnokseen
        muunnettu_teksti.append(aakkosto[muunnoksen_jälkeen])
        if debuggaus:
            print("Merkki: "+ kirjain +" on muunnettuna : ",aakkosto[muunnoksen_jälkeen])
            print("Aakkoston indeksi ennen muunnosta    : ",ennen_muunnosta)
            print("Aakkoston indeksi muunnoksen jälkeen : ",muunnoksen_jälkeen)

    return "".join(muunnettu_teksti)


def laske_siirros(aakkosto, avain, purku=False, debuggaus=False):
    if not purku:
        siirros = [aakkosto.index(merkki) for merkki in list(avain)]
    else:
        siirros = [-(aakkosto.index(merkki)) for merkki in list(avain)]
    if debuggaus:
        print(siirros)
    return siirros



def salain_c(viesti, avain):
    return vigenere(viesti, avain=avain)

def vigenere(viesti, aakkosto=None, avain="GIOVAN", purku=False, debuggaus=False):

    pienet=""
    if aakkosto is None:
        aakkosto, pienet = merkistot(suomi=True)

    alkuviesti = esikasittele_teksti(viesti, aakkosto+pienet)

    muunnettu_viesti = []

    # Generate ascii index of the first alphabet and offset list
    siirroslista = laske_siirros(aakkosto, avain, purku, debuggaus)

    if debuggaus:
        print("Saatu viesti  : ",viesti)
        print("Alkuviesti    : ",alkuviesti)

    for i,kirjain in enumerate(alkuviesti):
        ennen_muunnosta = aakkosto.index(kirjain)
        siirros_indeksi= (ennen_muunnosta+(siirroslista[i%len(siirroslista)]))%len(aakkosto)
        muunnettu_viesti.append(aakkosto[siirros_indeksi])
        if debuggaus:
            print("Viestin merkki : {}".format(i))
            print("Ennen muunnosta: ", ennen_muunnosta)
            print("Siirros indeksi: ", siirros_indeksi)
            print("Kirjain: "+ kirjain +" muunnetaan: ",aakkosto[siirros_indeksi])

    return "".join(muunnettu_viesti)


def merkistot(suomi = False):
    isot = string.ascii_uppercase
    pienet = string.ascii_lowercase
    numerot = string.digits
    if not suomi:
        return isot, pienet
    else:
        return isot+'ÅÄÖ', pienet+'åäö'

def harjoituksen_tiedostot(tunniste=None):

    if tunniste is None:
        hakemisto = "Tekstit/*.md"

    if tunniste == 'bin':
        hakemisto = "Tekstit/*.bin"
       
    tiedostot = glob.glob(hakemisto)
    return sorted(tiedostot)

def suomi():
    # Lähde https://jkorpela.fi/kielikello/kirjtil.html
    sanakirja = {
        "A": 11.9,
        "I": 10.64,
        "T": 9.77,
        "N": 8.67,
        "E": 8.21,
        "S": 7.85,
        "L": 5.68,
        "O": 5.34,
        "K": 5.24,
        "U": 5.06,
        "Ä": 4.59,
        "M": 3.3,
        "V": 2.52,
        "R": 2.32,
        "J": 1.91,
        "H": 1.83,
        "Y": 1.79,
        "P": 1.74,
        "D": 0.85,
        "Ö": 0.49,
        "G": 0.13,
        "B": 0.06,
        "F": 0.06,
        "C": 0.04,
        "W": 0.01,
        "Å": 0.0,
        "Q": 0.0,
        "X": 0.0,
        "Z": 0.0
    }
    return sanakirja



def vertaa_selväkieli_salakieli(selväteksti, salateksti, otsikko="Ei otsikkoa", kurvi=False):

    aakkoset, _ = merkistot(suomi=True)

    selvä_pros  = list(frekvenssi_prosenteiksi(tuota_frekvenssit(selväteksti), selväteksti).values())
    sala_pros   = list(frekvenssi_prosenteiksi(tuota_frekvenssit(salateksti), salateksti).values())

    x = np.arange(len(aakkoset))



    fig, ax = plt.subplots(figsize=(16,6))
    plt.bar(x-0.2, selvä_pros, width=0.4, ls='dotted',lw=3, fc=(0, 0, 1, 0.5), label = "Selväteksti")
    plt.bar(x+0.2, sala_pros,  width=0.4, ls='dotted',lw=3, fc=(1, 0, 0, 0.5), label = "Salateksti")

    for i,v in enumerate(selvä_pros):
        ax.text(i-0.5, v + 0.1, str(v), color='blue', alpha=0.7, fontweight='bold')

    for i,v in enumerate(sala_pros):
        ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    x_labels = list(aakkoset)
    plt.xticks(x,x_labels)

    plt.ylabel("Esiintymistiheys", fontsize=18)
    plt.xlabel("Kirjain",fontsize=18)
    plt.legend()
    plt.title("Selvä vs Sala: {}".format(otsikko),fontsize=20)

    if kurvi:
        f1 = interp1d(x, np.array(selvä_pros), kind='cubic')
        f2 = interp1d(x, np.array(sala_pros), kind='cubic')

        xnew = np.linspace(x.min(), x.max() , num=600, endpoint=True)
        plt.plot(xnew, f1(xnew), '-', xnew, f2(xnew), '--')
        plt.legend(['Selvä', 'Sala'], loc='best')

    plt.show()



def show_kirjainjakauma(kirjaimet = None, osuus = None, nimi=None, vain_aineisto=False, savefile=False ):
    s_kirjaimet=('A','I','T','N','E','S','L','O','K','U','Ä','M','V','R','J','H','Y','P','D','Ö','G','B','F','C','W','Å','Q','X','Z')
    s_osuus = [11.9, 10.64, 9.77, 8.67, 8.21, 7.85, 5.68, 5.34, 5.24, 5.06, 4.59, 3.30, 2.52, 2.32, 1.91, 1.83, 1.79, 1.74, 0.85, 0.49, 0.13, 0.06, 0.06, 0.04, 0.01, 0.0, 0.0, 0.0, 0.0]

    x = np.arange(len(s_kirjaimet))

    fig, ax = plt.subplots(figsize=(16,6))

    if kirjaimet is None:
        läpinäkyvyys = 0.9
        leveys = 0.8
    else:
        läpinäkyvyys = 0.4
        leveys = 0.5

        järjestetty_lista = []
        for i,kirjain in enumerate(s_kirjaimet):
            järjestetty_lista.append(osuus[kirjaimet.index(kirjain)])


    if not vain_aineisto:
        plt.bar(x, s_osuus, width=leveys, ls='dotted',lw=3, fc=(0, 0, 1, läpinäkyvyys), label = "Suomen kielen kirjainjakauma")

    if kirjaimet is not None:
        if vain_aineisto:
            plt.bar(x, osuus, ls='dashed',lw=5, fc=(1,0,0,0.6), label="Aineisto "+nimi)
        else:
            plt.bar(x, järjestetty_lista, ls='dashed',lw=5, fc=(1,0,0,0.6), label="Aineisto "+nimi)

    if vain_aineisto:
        plt.xticks(x,kirjaimet)
    else:
        plt.xticks(x,s_kirjaimet)

    plt.ylabel("Esiintymistiheys", fontsize=18)
    plt.xlabel("Kirjain",fontsize=18)
    plt.legend()

    if not vain_aineisto:
        for i, v in enumerate(s_osuus):
            ax.text(i-0.5, v + 0.1, str(v), color='blue', alpha=läpinäkyvyys, fontweight='bold')

    if kirjaimet is not None:
        if vain_aineisto:
            for i,v in enumerate(osuus):
                ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')
        else:
            for i,v in enumerate(järjestetty_lista):
                ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    if nimi is None:
        plt.title("Suomen kielen kirjainjakauma",fontsize=20)
    else:
        plt.title("Aineisto: {}".format(nimi),fontsize=20)

    if savefile:
        plt.savefig("suomen_kirjainjakauma.png",dpi=150)
    else:
        plt.show()



# Funktio joka trimmaa tekstin sallittuihin merkkeihin
def esikasittele_teksti(plain_text, dictionary, debug=False):
    plain_text_ok = []
    for character in plain_text:
        if character in dictionary:
            plain_text_ok.append(character.capitalize())
    if debug:
        print("Plain text before preprocessing:")
        print(plain_text)
        print("Plain text after preprocessing;")
        print("".join(plain_text_ok))
    return "".join(plain_text_ok)


# Funktio joka palauttaa aakkoset ja frekvenssit
def tuota_frekvenssit(teksti):
    isot, _ = merkistot(suomi=True)
    kirjainesiintymät = {}
    for kirjain in isot:
        kirjainesiintymät[kirjain]=0
    for kirjain in teksti:
        kirjainesiintymät[kirjain] += 1
    return kirjainesiintymät


def frekvenssi_prosenteiksi(frekvenssi_sanakirja, teksti):
    sanakirja = {}
    for key in frekvenssi_sanakirja.keys():
        sanakirja[key]= np.round(100*frekvenssi_sanakirja[key]/len(teksti), decimals=2)
    return sanakirja


def laske_frekvenssit(teksti):
    kirjainesiintymät = tuota_frekvenssit(teksti)
    esiintymisjärjestys = sorted(kirjainesiintymät.items(), key=lambda x:x[1], reverse=True)
    kirjaimet   = []
    frekvenssit = []
    for pari in esiintymisjärjestys:
        kirjaimet.append(pari[0])
        frekvenssit.append(pari[1])

    prosentit = np.round(100*np.array(frekvenssit)/len(teksti),decimals=2)

    return kirjaimet, prosentit

def laske_frekvenssi_ero_suomeen(sanakirja, verbose=False):
    suomen_jakauma = suomi()
    rms = 0
    for key in suomen_jakauma:
        ero = suomen_jakauma[key]-sanakirja[key]
        rms += np.square(ero)
        if verbose:
            print("Ero suomen kieleen kirjaimella {} on {:5} prosenttia".format(key,np.round(ero ,decimals=2)))

    return np.round(rms,decimals=2)


# Apufunktio joka tulostaa permutaatiot.
def näytä_permutaatiot(viesti):

    viestissä_merkkejä = len(viesti)
    # luodaan indeksilista viestistä
    indeksit = [i for i in range(viestissä_merkkejä)]
    # luodaan satunnaisesti järjestetyt indeksit
    permutoidut_indeksit = random.sample(indeksit, k=viestissä_merkkejä)
    # tehdään salateksti poimimalla permutoidun indeksin järjestyksessä kirjaimet
    salateksti = [viesti[i] for i in permutoidut_indeksit]

    # Tulostetaan viestin tiedot ja yksi permutaatio
    print("Selkoviesti: {} pituus: {}".format(viesti, viestissä_merkkejä))
    print("Mahdollisia permutaatioita: {}".format(math.factorial(viestissä_merkkejä)))
    print("Alkuperäiset indeksit:\n{}\n{}".format(list(viesti),indeksit))
    print("Satunnainen permutaatio:\n{}\n{}".format(salateksti,permutoidut_indeksit))
    print("Salakieli edellisellä permutaatiolla: {}".format("".join(salateksti)))



def onetimepad(viesti="KAHVICHARLOTASSAONHYVÄÄJAVAHVAA"):
    aakkoset = string.ascii_uppercase + 'ÅÄÖ'
    viestissä_merkkejä = len(viesti)
    satunnaisotos=choices(aakkoset, k=len(viesti))
    return "".join(satunnaisotos), vigenere(viesti, aakkosto=aakkoset, avain="".join(satunnaisotos), purku=False, debuggaus=False)


def testaa_hyökkäysmallien_osaaminen(viesti,avain):
    if salain_c(viesti,avain)=='ÄZLRÖYFMVO':
        print("Hienoa, voit edetä harjoituksiin!")
    else:
        print("Ei aivan, yritä uudestaan! Voit kysyä apuja kavereilta, jos tämä tuntuu hankalalta.")

def generoi_caesar_haaste(debuggaus=False, purku=False):
    viesti='Ensilumi suli, takatalvi tuli!'
    isot, pienet = merkistot(suomi=True)
    esikäsitelty_viesti = esikasittele_teksti(viesti, isot+pienet)

    if debuggaus:
        print("Alkuperäinen viesti  :", viesti)
        print("Esikäsitelty viesti  :", esikäsitelty_viesti)


    # Suoritetaan Caesar salaus edellisillä arvoilla
    salateksti=caesar(esikäsitelty_viesti,aakkosto=isot, avain=11, purku=False)
    if debuggaus:
        print("Caesar salateksti on :",salateksti)

    # Suoritetaan salauksen purku asettamalla purku-lippu arvoon True
    dekoodattu_teksti=caesar(salateksti,aakkosto=isot, avain=11, purku=True)
    if debuggaus:
        print("Caesar dekoodattu on :",dekoodattu_teksti)

    if not purku:
        return salateksti
    else:
        return dekoodattu_teksti

def freq_analyze(tiedosto, debuggaus=False):
    # Ensiksi määritellään aakkosto
    isot, pienet = merkistot(suomi=True)
    sallitut = isot + pienet
    aakkoston_koko = len(''.join(set(isot)))
    if debuggaus:
        print("Tekstistä poimitaan vain seuraavat sallitut kirjaimet")
        print(sallitut)
        print("Suomen aakkosia on {}".format(aakkoston_koko))

    tekstitiedostot = harjoituksen_tiedostot()
    nimi = os.path.basename(tekstitiedostot[tiedosto])[:-3]
    teksti = ""
    with open(tekstitiedostot[tiedosto], "r", encoding="utf_8") as file:
        teksti = file.read()
    # Muodostetaan tekstistä kirjainjono, jossa on vain sallitut aakkoset a..ö ja A..Ö
    kirjainjono = esikasittele_teksti(teksti, sallitut)
    kirjainjonon_merkit = ''.join(set(kirjainjono))

    print("Kirjainjonon pitus on {} merkkiä".format(len(kirjainjono)))
    print("Ja siinä esiintyy yhteensä {} eri aakkosta.".format(len(kirjainjonon_merkit)))
    if aakkoston_koko - len(kirjainjonon_merkit) != 0:
        print("Kirjainjonon puuttuvat kirjaimet ovat {}".format(''.join(set(isot).difference(kirjainjonon_merkit))))
    #print("Kirjainjono näyttää tältä:" +kirjainjono)

    # Lasketaan
    frekvenssi_kirjaimet, frekvenssi_prosentit = laske_frekvenssit(kirjainjono)
    show_kirjainjakauma(tuple(frekvenssi_kirjaimet),frekvenssi_prosentit, nimi)

    määrät = tuota_frekvenssit(kirjainjono)
    prosentit = frekvenssi_prosenteiksi(määrät, kirjainjono)
    poikkeaa_suomen_kielestä = laske_frekvenssi_ero_suomeen(prosentit)
    print("{} kirjoitus poikkeaa {} määrän suomen kielestä".format(nimi, poikkeaa_suomen_kielestä))

def näytä_tekstit():
    tekstitiedostot = harjoituksen_tiedostot()
    print("Saatavilla olevat tiedostot")
    for i, nimi in enumerate(sorted(tekstitiedostot)):
        print("Tiedostoindeksi: {} on {}".format(i,nimi[8:-3]))

def lue_bin_tiedosto(indeksi=None):
    if indeksi is None:
        print("Et antanut indeksiä.\n")
        harjoituksen_tiedostot('bin')
        bin_viesti=""
    else:
        binääritiedostot = harjoituksen_tiedostot()
        tiedosto=indeksi
        with open(binääritiedostot[tiedosto], "r", encoding="utf_8") as file:
            bin_viesti = "".join(file.readlines())
     
    return bin_viesti

def lue_tiedosto_merkkijonoksi(indeksi=None, debuggaus=False):
    if indeksi is None:
        print("Et antanut indeksiä.\n")
        näytä_tekstit()
        alkuperäinen_viesti=""
    else:
        tiedosto=indeksi
        isot, pienet = merkistot(suomi=True)
        sallitut = isot + pienet
        aakkoston_koko = len(''.join(set(isot)))

        if debuggaus:
            print("Tekstistä poimitaan vain seuraavat sallitut kirjaimet")
            print(sallitut)
            print("Suomen aakkosia on {}".format(aakkoston_koko))

        tekstitiedostot = harjoituksen_tiedostot()
        nimi = os.path.basename(tekstitiedostot[tiedosto])[:-3]
        teksti = ""
        with open(tekstitiedostot[tiedosto], "r", encoding="utf_8") as file:
            teksti = file.read()
        # Muodostetaan tekstistä kirjainjono, jossa on vain sallitut aakkoset a..ö ja A..Ö
        alkuperäinen_viesti = esikasittele_teksti(teksti, sallitut)
        kirjainjonon_merkit = ''.join(set(alkuperäinen_viesti))
    return alkuperäinen_viesti

def materiaalin_freq(viesti, otsikko="Ei annettu otsikkoa"):
    # Lasketaan frekvenssit
    frekvenssi_kirjaimet, frekvenssi_prosentit = laske_frekvenssit(viesti)
    show_kirjainjakauma(tuple(frekvenssi_kirjaimet),frekvenssi_prosentit, otsikko)

def vertaa_selväkieli_salakieli(selväteksti, salateksti="", otsikko=None, kurvi=False, debuggaus=False):

    salateksti_puuttuu = len(salateksti)==0
    if salateksti_puuttuu:
        print("väärä funktio, tarvitsen selvätekstin ja salatekstin")
    aakkoset, _ = merkistot(suomi=True)
    leveys = 0.8

    selvä_pros  = list(frekvenssi_prosenteiksi(tuota_frekvenssit(selväteksti), selväteksti).values())

    if not salateksti_puuttuu:
        sala_pros   = list(frekvenssi_prosenteiksi(tuota_frekvenssit(salateksti), salateksti).values())
        leveys = 0.8

    if debuggaus:
        print("selväteksti:", selväteksti)
        print("salateksti :", salateksti)
        print("selväpros  :", selvä_pros)
        print("salapros   :", sala_pros)

    x = np.arange(len(aakkoset))

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(16,12))

    x_siirros = 0


    axes[0].bar(x-x_siirros, selvä_pros, width=leveys, ls='dotted',lw=3, fc=(0, 0, 1, 0.5), label = "Selväteksti")
    axes[1].bar(x+x_siirros, sala_pros,  width=leveys, ls='dotted',lw=3, fc=(1, 0, 0, 0.5), label = "Salateksti")

    if False:
        for i,v in enumerate(selvä_pros):
            axes[0].text(i-0.5, v + 0.1, str(v), color='blue', alpha=0.7, fontweight='bold')

        if not salateksti_puuttuu:
            for i,v in enumerate(sala_pros):
                axes[1].text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    x_labels = list(aakkoset)
    axes[0].set_xticks(x,minor=False)
    axes[1].set_xticks(x,minor=False)
    axes[0].set_xticklabels(x_labels, fontdict=None, minor=False)
    axes[1].set_xticklabels(x_labels, fontdict=None, minor=False)

    axes[0].title.set_text('Selväteksti')
    axes[1].title.set_text('Salateksti')

    axes[0].set_ylabel('Esiintymistiheys', fontsize=16)
    axes[1].set_ylabel('Esiintymistiheys', fontsize=16)

    #axes[0].set_xlabel("Kirjain",fontsize=18)
    axes[1].set_xlabel("Kirjain",fontsize=18)

    axes[0].legend()
    axes[1].legend()



    if otsikko is None:
        otsikko="Tuntematon aineisto"

    fig.suptitle("Aineisto: {}".format(otsikko),fontsize=20)

    if kurvi:
        f1 = interp1d(x, np.array(selvä_pros), kind='cubic')
        f2 = interp1d(x, np.array(sala_pros), kind='cubic')

        xnew = np.linspace(x.min(), x.max() , num=601, endpoint=True)
        plt.plot(xnew, f1(xnew), '-', xnew, f2(xnew), '--')
        plt.legend(['Selvä', 'Sala'], loc='best')

    plt.show()


def tekstin_frekvenssi_aakkosissa(selväteksti, salateksti="", otsikko=None, kurvi=False, tiedostoon=False, debuggaus=False):

    salateksti_puuttuu = len(salateksti)==0
    aakkoset, _ = merkistot(suomi=True)
    leveys = 0.8

    selvä_pros  = list(frekvenssi_prosenteiksi(tuota_frekvenssit(selväteksti), selväteksti).values())

    if not salateksti_puuttuu:
        sala_pros   = list(frekvenssi_prosenteiksi(tuota_frekvenssit(salateksti), salateksti).values())
        leveys = 0.4

    if debuggaus:
        print("selväteksti:", selväteksti)
        print("salateksti :", salateksti)
        print("selväpros  :", selvä_pros)
        print("salapros   :", sala_pros)

    x = np.arange(len(aakkoset))

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16,6))

    if salateksti_puuttuu:
        x_siirros = 0
    else:
        x_siirros = 0.2

    ax.bar(x-x_siirros, selvä_pros, width=leveys, ls='dotted',lw=3, fc=(0, 0, 1, 0.5), label = "Selväteksti")

    if not salateksti_puuttuu:
        ax.bar(x+x_siirros, sala_pros,  width=leveys, ls='dotted',lw=3, fc=(1, 0, 0, 0.5), label = "Salateksti")

    if False:
        for i,v in enumerate(selvä_pros):
            ax.text(i-0.5, v + 0.1, str(v), color='blue', alpha=0.7, fontweight='bold')

        if not salateksti_puuttuu:
            for i,v in enumerate(sala_pros):
                ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    x_labels = list(aakkoset)
    plt.xticks(x,x_labels)

    plt.ylabel("Esiintymistiheys", fontsize=18)
    plt.xlabel("Kirjain",fontsize=18)
    plt.legend()

    if otsikko is None:
        otsikko="Tuntematon aineisto"

    plt.title("Aineisto: {}".format(otsikko),fontsize=20)

    if kurvi:
        f1 = interp1d(x, np.array(selvä_pros), kind='cubic')
        f2 = interp1d(x, np.array(sala_pros), kind='cubic')

        xnew = np.linspace(x.min(), x.max() , num=601, endpoint=True)
        plt.plot(xnew, f1(xnew), '-', xnew, f2(xnew), '--')
        plt.legend(['Selvä', 'Sala'], loc='best')

    if tiedostoon:
        plt.savefig("frekvenssi.png")
    else:
        plt.show()

def freq_testi_a():
    return "LOQÖÖPUSÖJSYRQÖPVYPSURAVÖVQOJÖLOQÖÖPUSÖJSYRQÖNÖIROÅOYRVOÖRSYQUKJUNOUSÖORUORRIJSLUKJÖRRUSÖINNUÖÖPNÖRHYRISKYKKÖQYRSYUPSIISÖIZYPHÖUSSÖJEAORUSÖUSSYÖQIIJÖSIUPUVÖPJYYRRUKJÖSÖINNUÖKQÖLQÖJJUJUKSUPKBJÖSÖPÖSÖUSYPNBUHBBSOQYPKUNOUSÖÖTÖHÖLOUJJUKBLSYQBKJBQUJBBPQIJJÖNOUSÖVÖRIKUNEKEBJEANÖUSÖKKÖÖPKURRBPÖRSIJJÖQUKYKJÖÖPVIORUQÖJJÖHÖPVÖSÖINNUÖKYUORRIJYNBOUSYIZYPQISÖUPYPVBPKÖUVEHBPNÖRSSUOPTOSÖUKYKJÖQEEQBKJBBPYKUPYYKJBTÖORUYVJUPEJKBBKJBBTOPSUPHYLLÖPLÖVÖÖKUPBÖÖQIPÖVBPORURÖKSYKSYRRIJYJJBTOKVBPJYSUKUJEAJBTOSÖNBUHBSIJYPORUJYVPEJKUUVYPSUPÖKJUVBPYPORUKUIILÖKJYJJÖHÖHIOKUYPPYPSIUPHOUKUOKJÖÖNÖLURÖQQÖKJÖVÖRIÖUKUPNEKJEJJBBQEEPJUNAEZBPSLUKJÖRRUYKUPYURRYNOUSÖKÖPOUSÖINNUÖÖRRYKYPHOUKUNÖPPÖIRSONIORYRRYPUUPYJJBKYVOISIJJYRUKUJBPPYHBSYBSISSIRÖPTIILYRJÖQUPIRRÖYUORYORRIJSOKSÖÖPKYRRÖUKJÖNAEJBBSÖINNUÖKHÖKJÖKUUVQUKYJJALQBBHBJKUUVYPTÖKBLSYHBJSLUKJÖRRUJSIPSIRTUPRÖUJIQYRRÖRÖQNÖUJJYPUSÖPKKÖHÖÖLÖPÖORUÖUPÖYJJBPUUZYPJUYRRYOKIUKUSBBLQYTÖYJJBPYSIORUKUHÖJQIJJÖKYRRÖUKJÖOPRÖQNÖUZYPTÖNÖUQYPYPYRBQBSÖINNUÖKSBBPJEUNÖRHYRYQÖÖPÖKUÖSÖKJÖTOSÖVÖRIKUSORQYSLUKJÖRRURÖKUÖVBPQEUPESEBBPNÖLYQQUPSIUPSOKSÖÖPVBPYKJBJIPJIUSIUPVBPORUKUNÖRÖPPIJÖUSÖÖPTORROUPSÖJIORUORRIJJÖPWYLUPKIOKUJIUQNUÖOKJOKNÖUSSOTÖSÖINÖPSBEPJUOPJOZYRRÖHURSÖKJIPIJQYRSOUKYKJUQUYKKÖPOUNOTÖRRYÖKUÖSSÖÖPNOUKJIJJIÖQUPIRRÖQYPYYNÖRTOPNÖLYQQUPTÖKUPBHOUJOKJÖÖSOVJÖRÖQNÖÖKUQUSKUNEEJBUKUJYRBQBRJBYPYQQBPKUSKUYJJBTOSÖUKYPOPKYILÖJJÖHÖYPPIKQYLSSYTBNOUSÖKÖPOUJÖVJOQÖJJÖÖPTÖSÖJIUVYJUKÖPOTÖÖPKURRBSÖINNUÖKYUORRIJJÖHÖPPIJSOKSÖÖPSIPUPWÖKJÖKUJBSIJKIJÖÖPKIOJIUKÖPOPPYPNYLUÖÖJJYYSKUÖROUJJYRUTÖPVEHBSKUOPPYSKUSOKSÖYRBQBVÖRIÖÖYJJBTOSÖUPYPKYILÖÖOQÖÖJUYJBBPHÖPVÖSIPUPWÖKORUKÖPOPIJSÖINNUÖKEQQBLKUSIUJYPSUPQUKJBNOUSÖNIVIUNOTÖPNYRSSBRBKPBOROORUORRIJVEHBYPPYTÖSIPÖUSÖSIRIUTÖLÖVÖÖÖRSOUHULLÖJÖSÖKKÖÖPVBPYRRBYUORRIJQUJBBPKEEJBSÖJIÖYJJBORUOJJÖPIJYKNÖPTÖRÖUKYPNÖRHYRISKYYPKÖNOUSÖÖPKÖUJKUYVSBYPYQQBPSIUPORUKUSIIRIPIJQIJJÖSOKSÖVBPYUORRIJIKSOPIJQEEPPUPKYPSIQQYQQUPSÖKHÖHÖPVBPORUJÖLTOPPIJNOTÖRRYNÖLYQQÖPQEEPJUNÖRSSUOPVBPORUÖTÖJYRRIJYJJBNOUSÖNÖRÖUKUNUÖPRÖQNÖUJJYPKÖRIOQUSKUVÖRIKUJNBBKJBNELÖQUZYURRYVBPSEKEUKUULJBBSKYYPSYKSIKJYRIPYKUJJYRENAEZUKJBKUSKUYJJBORYPSIIRRIJPUUKJBUSBPUNOUSÖHÖKJÖKUSYLJOQÖJJÖIPYKJÖÖPÖÖLLYORUPEJNYRSSBJIKSÖRRUPYPQIUKJOYUSBVBPVÖRIPPIJÖTÖJYRRÖSOSOÖKUÖÖYPJIPPYSYJBBPTOSÖVÖRIÖUKUSIRSYÖÖÖHUSOPNOUSSUNELÖQUZUYPHIOSKUSÖINNUÖKKÖPOUPYVBPOHÖJNYRSSBSÖKÖSUHUBHOUKUJNEKJEJJBBKYRRÖUKYPOQÖRRYJÖSÖNUVÖRRYKUJYYJJYORYVÖÖHYURRIJSOKSÖÖPNBBKYHBPPYQÖÖURQÖRRYNOUSÖHÖKJÖKUTÖRBVJUNÖRHYRYQÖÖPÖKUÖSÖKJÖTOSÖORUÖKJIPIJRUUSSYYKYYPSÖSKUNBUHBBQEAVYQQUPSÖINNUÖKJIRUNIVIQÖÖPNOTÖRRYQEEPJUNAEZBKJBYPNUZBQIIJOSKUKJÖVBPKÖPOUKUPBTÖQUPBYQQYORYSIUPVÖKKÖPLUSÖKSÖINNUÖKVBPJBYUVBJSBVZEJBNÖRTOÖSÖÖPHÖUSSÖJYSUKUHBBLBPKUTOUJISKYPQIJJÖQYUZBPSÖVZYPOPQÖSKYJJÖHÖHULVYUKJBQQYKYÖUPÖSUPNUJBBNÖUSSÖPKÖNOUSÖÖTÖJJYRUQUPSBHIOSKUVÖRIÖJNEKJEJJBBNAEZBPSÖINNUÖKSEKEUVÖRIÖPNBBKJBNUÖPRÖQNÖUJJYPURIOQYUZBPOPJOUQUJJÖHÖPEJSIPOPPUOPNIORYRRÖQQYTÖÖIJYJJÖHÖKUJBEVJBNÖRTOPSIUPKYÖIJJÖÖQYUJBKUJBSIJKIJÖÖPKIOJIUKÖPOPPYPNYLUÖÖJJYYSKUÖROUJJYRUTÖPVEHBSKUOPPYSKUHÖPVÖSÖINNUÖKORUVYJSYPBBPYJUTÖKÖPOUHUUQYUPNLOXYYJJÖÖPJOUQYURRYSOLÖÖPUPTÖTBJJUHUUKUOVTYPIOLÖÖTOUJÖPOIZÖJJÖÖYRBQBQQYÖUSÖPÖJBLSYUPOPKYYJJBOPIKSOJJÖHÖEVJYYPÖUPOÖÖPTIQÖRÖÖPKYPRUKBSKUQYUZBPOPLISOURJÖHÖHUUKUSYLJÖÖNBUHBKKBNÖÖKJOJJÖHÖLÖQÖZÖPSIIPÖUSÖPÖTÖÖPPYJJÖHÖÖRQITÖSAEVURRYVBPHÖUSYPUVBPYPKURQBPKBJBEJJEUHBJSEEPYRUKJBVBPYPNIVIYKKÖÖPNLOXYYJÖKJÖVBPORUVILKSÖKQUYKTOSÖELUJJUSUUHÖÖKJÖRIOPJYYKJÖÖPVIORUQÖJJÖYRBBUKRÖQUPONNUYPQISÖÖPQUSBKYHUUZYKOVTYPIOLÖOPNOUSÖSEKEUKÖPOUJNÖLUNBUHBBKUJJYPYJJYPORYIPYRQOUPIJSOKSÖÖPQÖJSIKJÖQUKYKJÖSÖINNUÖKHÖKJÖKUTOSÖUKYPQIKRUQUPHUUZYKHYRHORRUKIIKOPNEVUUPHÖYRRIKQÖJSÖQYUZBPOPSBEJBHBÖUPÖSUPSYLLÖPYRBQBQQYÖUSÖPÖQYSÖKKÖNEVBKKBSÖINIPWUKKÖQYSSÖOPNÖRTOPSÖIYQNÖPÖSIUPNELÖQUZUJPIOLYPÖNBBJUPSBEJJBBHBVBJLÖVÖPUSÖINNÖPUNYLIKJÖQUKYYPÖTÖJJYRUPORYHÖPUTOPÖUPNBUHBPBPUUPLUSÖKYJJBHOUKUPRBVJYBQYSSÖÖPÖROUPHÖILÖKJIÖQIJJYPHOUPIJTBJJBBJBJBSÖUSSYÖSYPYPSBBPHÖKJIIRRYKURRBSLUKJÖRRUJOHÖJVÖILÖUJÖYKUPYUJBKÖQÖÖPÖUSÖÖPSÖJKYRUPSIUPSÖUVQUKYJHÖYRKUHÖJSÖINNÖPUOVUSOVJUQYSSÖÖQIIJÖQÖJNEVUUPHÖYRJÖTÖJORUHÖJPUUPLUSSÖUJÖYJJBVYURRBORUOQÖNÖRHYRUTOUZYPTÖSÖQYRUYPKÖÖJJIYQIJJÖIKYUQQÖJVYUKJBORUHÖJSAEVYQNUBSIUPQUPBSÖUSSURBVJUHBJNÖRÖKUHÖJJEEJEHBUKUPBTÖLUNIKJUHÖJNEVUUPHÖYRRIKQÖJSÖPKEQÄORUJNOLJJUPKÖNUYRYYPYLBKKIIJÖLUSYLJOUSIRSYPYYPKÖQYRSYUPHIOZYPÖÖHUSOPNOUSSUQIJJÖKÖPOUHBKEHBPKBNÖRTOPYPYQQBPSIPVBPYPORURBVZYJJBHBJÖPWYLUKKÖNÖLUPSOLJJYRUPNBBVBPOKJÖQÖÖPPÖVSÖÖQUSKYJJYRBVZYQYSSÖÖPPEJNOUSÖSEKEUKUSKUYJJBÖTÖJIKQYSÖKJÖNUJBBQUPIJYROKKÖKYKÖÖQUPIJSYKJBQBBPESKUJOUSSOUKYJNBUHBJPBUZYPVERRETYPQESBJSLUKJÖRRUJTÖJIOPSÖVHURÖPVULHUJJBHBJLIOÖJNYRSBBPJOJYIJJÖÖIPYRQÖÖPUSOKSÖKYPTBRSYYPQUPIRRÖYUORUKUQUJBBPKEEJBYRBBKUPBIPYRQOUJRÖQNÖUKJÖTÖNELÖQUZYUKJÖKUPBORYJYLURÖUPYPSIUPQUPBKURRBKUPBVÖRIÖJJOJYIJJÖÖIPYRQÖKUQUPBVÖRIÖPHÖUPVÖÖHYURRÖQYSÖKJÖORYPSIHUJYRRIJJIVÖPKUÖSYLJOTÖSIUPSÖSIRTYPÖÖHUSOPNOUSSUKÖÖHIPÖISUORRYTÖSUYLLBPNÖSORRUKYJKYUJKYQBPSYLJÖÖNEVBPSUHYPYPPYPSIUPSOKSYJÖPKUJBSIHUJJYRYPSYUJBOPHUYLYRRBPUTÖYZYKKBPUQUKJBSYKSIKJYRYQQYTÖQUJSBLISOISKYJLISOURYQQYEVZYKKBQIJJÖNYRSBBPNYJJEHBPUTÖJEEZEPKYPHIOSKUIPYRQOUQÖÖPKUPBNBUHBPBSÖINNUÖKÖPJOUNOTÖRRYRIHÖPNEKJEJJBBQEEPJUNAEZBPSÖUSSUYUHBJHOUJOJYIJJÖÖIPYRQUÖÖPKÖQÖRRÖJÖHÖRRÖRBVZYNÖIROÅOYRVOÖRSYQUKJUÖRSINYLBUKJYOKOPTIRSÖUKJIHIOPPÖTIRSÖUKJIKIOQYPPOKKÖPPÖNYLPILOQÖÖPUSÖJSYRQÖPVYPSURAVÖVQOJÖLOQÖÖPUSÖJSYRQÖNÖIROÅOYRVOÖRSYQUKJUNOUSÖORUORRIJSLUKJÖRRUSÖINNUÖÖPNÖRHYRISKYKKÖQYRSYUPSIISÖIZYPHÖUSSÖJEAORUSÖUSSYÖQIIJÖSIUPUVÖPJYYRRUKJÖSÖINNUÖKQÖLQÖJJUJUKSUPKBJÖSÖPÖSÖUSYPNBUHBBSOQYPKUNOUSÖÖTÖHÖLOUJJUKBLSYQBKJBQUJBBPQIJJÖNOUSÖVÖRIKUNEKEBJEANÖUSÖKKÖÖPKURRBPÖRSIJJÖQUKYKJÖÖPVIORUQÖJJÖHÖPVÖSÖINNUÖKYUORRIJYNBOUSYIZYPQISÖUPYPVBPKÖUVEHBPNÖRSSUOPTOSÖUKYKJÖQEEQBKJBBPYKUPYYKJBTÖORUYVJUPEJKBBKJBBTOPSUPHYLLÖPLÖVÖÖKUPBÖÖQIPÖVBPORURÖKSYKSYRRIJYJJBTOKVBPJYSUKUJEAJBTOSÖNBUHBSIJYPORUJYVPEJKUUVYPSUPÖKJUVBPYPORUKUIILÖKJYJJÖHÖHIOKUYPPYPSIUPHOUKUOKJÖÖNÖLURÖQQÖKJÖVÖRIÖUKUPNEKJEJJBBQEEPJUNAEZBPSLUKJÖRRUYKUPYURRYNOUSÖKÖPOUSÖINNUÖÖRRYKYPHOUKUNÖPPÖIRSONIORYRRYPUUPYJJBKYVOISIJJYRUKUJBPPYHBSYBSISSIRÖPTIILYRJÖQUPIRRÖYUORYORRIJSOKSÖÖPKYRRÖUKJÖNAEJBBSÖINNUÖKHÖKJÖKUUVQUKYJJALQBBHBJKUUVYPTÖKBLSYHBJSLUKJÖRRUJSIPSIRTUPRÖUJIQYRRÖRÖQNÖUJJYPUSÖPKKÖHÖÖLÖPÖORUÖUPÖYJJBPUUZYPJUYRRYOKIUKUSBBLQYTÖYJJBPYSIORUKUHÖJQIJJÖKYRRÖUKJÖOPRÖQNÖUZYPTÖNÖUQYPYPYRBQBSÖINNUÖKSBBPJEUNÖRHYRYQÖÖPÖKUÖSÖKJÖTOSÖVÖRIKUSORQYSLUKJÖRRURÖKUÖVBPQEUPESEBBPNÖLYQQUPSIUPSOKSÖÖPVBPYKJBJIPJIUSIUPVBPORUKUNÖRÖPPIJÖUSÖÖPTORROUPSÖJIORUORRIJJÖPWYLUPKIOKUJIUQNUÖOKJOKNÖUSSOTÖSÖINÖPSBEPJUOPJOZYRRÖHURSÖKJIPIJQYRSOUKYKJUQUYKKÖPOUNOTÖRRYÖKUÖSSÖÖPNOUKJIJJIÖQUPIRRÖQYPYYNÖRTOPNÖLYQQUPTÖKUPBHOUJOKJÖÖSOVJÖRÖQNÖÖKUQUSKUNEEJBUKUJYRBQBRJBYPYQQBPKUSKUYJJBTOSÖUKYPOPKYILÖJJÖHÖYPPIKQYLSSYTBNOUSÖKÖPOUJÖVJOQÖJJÖÖPTÖSÖJIUVYJUKÖPOTÖÖPKURRBSÖINNUÖKYUORRIJJÖHÖPPIJSOKSÖÖPSIPUPWÖKJÖKUJBSIJKIJÖÖPKIOJIUKÖPOPPYPNYLUÖÖJJYYSKUÖROUJJYRUTÖPVEHBSKUOPPYSKUSOKSÖYRBQBVÖRIÖÖYJJBTOSÖUPYPKYILÖÖOQÖÖJUYJBBPHÖPVÖSIPUPWÖKORUKÖPOPIJSÖINNUÖKEQQBLKUSIUJYPSUPQUKJBNOUSÖNIVIUNOTÖPNYRSSBRBKPBOROORUORRIJVEHBYPPYTÖSIPÖUSÖSIRIUTÖLÖVÖÖÖRSOUHULLÖJÖSÖKKÖÖPVBPYRRBYUORRIJQUJBBPKEEJBSÖJIÖYJJBORUOJJÖPIJYKNÖPTÖRÖUKYPNÖRHYRISKYYPKÖNOUSÖÖPKÖUJKUYVSBYPYQQBPSIUPORUKUSIIRIPIJQIJJÖSOKSÖVBPYUORRIJIKSOPIJQEEPPUPKYPSIQQYQQUPSÖKHÖHÖPVBPORUJÖLTOPPIJNOTÖRRYNÖLYQQÖPQEEPJUNÖRSSUOPVBPORUÖTÖJYRRIJYJJBNOUSÖNÖRÖUKUNUÖPRÖQNÖUJJYPKÖRIOQUSKUVÖRIKUJNBBKJBNELÖQUZYURRYVBPSEKEUKUULJBBSKYYPSYKSIKJYRIPYKUJJYRENAEZUKJBKUSKUYJJBORYPSIIRRIJPUUKJBUSBPUNOUSÖHÖKJÖKUSYLJOQÖJJÖIPYKJÖÖPÖÖLLYORUPEJNYRSSBJIKSÖRRUPYPQIUKJOYUSBVBPVÖRIPPIJÖTÖJYRRÖSOSOÖKUÖÖYPJIPPYSYJBBPTOSÖVÖRIÖUKUSIRSYÖÖÖHUSOPNOUSSUNELÖQUZUYPHIOSKUSÖINNUÖKKÖPOUPYVBPOHÖJNYRSSBSÖKÖSUHUBHOUKUJNEKJEJJBBKYRRÖUKYPOQÖRRYJÖSÖNUVÖRRYKUJYYJJYORYVÖÖHYURRIJSOKSÖÖPNBBKYHBPPYQÖÖURQÖRRYNOUSÖHÖKJÖKUTÖRBVJUNÖRHYRYQÖÖPÖKUÖSÖKJÖTOSÖORUÖKJIPIJRUUSSYYKYYPSÖSKUNBUHBBQEAVYQQUPSÖINNUÖKJIRUNIVIQÖÖPNOTÖRRYQEEPJUNAEZBKJBYPNUZBQIIJOSKUKJÖVBPKÖPOUKUPBTÖQUPBYQQYORYSIUPVÖKKÖPLUSÖKSÖINNUÖKVBPJBYUVBJSBVZEJBNÖRTOÖSÖÖPHÖUSSÖJYSUKUHBBLBPKUTOUJISKYPQIJJÖQYUZBPSÖVZYPOPQÖSKYJJÖHÖHULVYUKJBQQYKYÖUPÖSUPNUJBBNÖUSSÖPKÖNOUSÖÖTÖJJYRUQUPSBHIOSKUVÖRIÖJNEKJEJJBBNAEZBPSÖINNUÖKSEKEUVÖRIÖPNBBKJBNUÖPRÖQNÖUJJYPURIOQYUZBPOPJOUQUJJÖHÖPEJSIPOPPUOPNIORYRRÖQQYTÖÖIJYJJÖHÖKUJBEVJBNÖRTOPSIUPKYÖIJJÖÖQYUJBKUJBSIJKIJÖÖPKIOJIUKÖPOPPYPNYLUÖÖJJYYSKUÖROUJJYRUTÖPVEHBSKUOPPYSKUHÖPVÖSÖINNUÖKORUVYJSYPBBPYJUTÖKÖPOUHUUQYUPNLOXYYJJÖÖPJOUQYURRYSOLÖÖPUPTÖTBJJUHUUKUOVTYPIOLÖÖTOUJÖPOIZÖJJÖÖYRBQBQQYÖUSÖPÖJBLSYUPOPKYYJJBOPIKSOJJÖHÖEVJYYPÖUPOÖÖPTIQÖRÖÖPKYPRUKBSKUQYUZBPOPLISOURJÖHÖHUUKUSYLJÖÖNBUHBKKBNÖÖKJOJJÖHÖLÖQÖZÖPSIIPÖUSÖPÖTÖÖPPYJJÖHÖÖRQITÖSAEVURRYVBPHÖUSYPUVBPYPKURQBPKBJBEJJEUHBJSEEPYRUKJBVBPYPNIVIYKKÖÖPNLOXYYJÖKJÖVBPORUVILKSÖKQUYKTOSÖELUJJUSUUHÖÖKJÖRIOPJYYKJÖÖPVIORUQÖJJÖYRBBUKRÖQUPONNUYPQISÖÖPQUSBKYHUUZYKOVTYPIOLÖOPNOUSÖSEKEUKÖPOUJNÖLUNBUHBBKUJJYPYJJYPORYIPYRQOUPIJSOKSÖÖPQÖJSIKJÖQUKYKJÖSÖINNUÖKHÖKJÖKUTOSÖUKYPQIKRUQUPHUUZYKHYRHORRUKIIKOPNEVUUPHÖYRRIKQÖJSÖQYUZBPOPSBEJBHBÖUPÖSUPSYLLÖPYRBQBQQYÖUSÖPÖQYSÖKKÖNEVBKKBSÖINIPWUKKÖQYSSÖOPNÖRTOPSÖIYQNÖPÖSIUPNELÖQUZUJPIOLYPÖNBBJUPSBEJJBBHBVBJLÖVÖPUSÖINNÖPUNYLIKJÖQUKYYPÖTÖJJYRUPORYHÖPUTOPÖUPNBUHBPBPUUPLUSÖKYJJBHOUKUPRBVJYBQYSSÖÖPÖROUPHÖILÖKJIÖQIJJYPHOUPIJTBJJBBJBJBSÖUSSYÖSYPYPSBBPHÖKJIIRRYKURRBSLUKJÖRRUJOHÖJVÖILÖUJÖYKUPYUJBKÖQÖÖPÖUSÖÖPSÖJKYRUPSIUPSÖUVQUKYJHÖYRKUHÖJSÖINNÖPUOVUSOVJUQYSSÖÖQIIJÖQÖJNEVUUPHÖYRJÖTÖJORUHÖJPUUPLUSSÖUJÖYJJBVYURRBORUOQÖNÖRHYRUTOUZYPTÖSÖQYRUYPKÖÖJJIYQIJJÖIKYUQQÖJVYUKJBORUHÖJSAEVYQNUBSIUPQUPBSÖUSSURBVJUHBJNÖRÖKUHÖJJEEJEHBUKUPBTÖLUNIKJUHÖJNEVUUPHÖYRRIKQÖJSÖPKEQÄORUJNOLJJUPKÖNUYRYYPYLBKKIIJÖLUSYLJOUSIRSYPYYPKÖQYRSYUPHIOZYPÖÖHUSOPNOUSSUQIJJÖKÖPOUHBKEHBPKBNÖRTOPYPYQQBPSIPVBPYPORURBVZYJJBHBJÖPWYLUKKÖNÖLUPSOLJJYRUPNBBVBPOKJÖQÖÖPPÖVSÖÖQUSKYJJYRBVZYQYSSÖÖPPEJNOUSÖSEKEUKUSKUYJJBÖTÖJIKQYSÖKJÖNUJBBQUPIJYROKKÖKYKÖÖQUPIJSYKJBQBBPESKUJOUSSOUKYJNBUHBJPBUZYPVERRETYPQESBJSLUKJÖRRUJTÖJIOPSÖVHURÖPVULHUJJBHBJLIOÖJNYRSBBPJOJYIJJÖÖIPYRQÖÖPUSOKSÖKYPTBRSYYPQUPIRRÖYUORUKUQUJBBPKEEJBYRBBKUPBIPYRQOUJRÖQNÖUKJÖTÖNELÖQUZYUKJÖKUPBORYJYLURÖUPYPSIUPQUPBKURRBKUPBVÖRIÖJJOJYIJJÖÖIPYRQÖKUQUPBVÖRIÖPHÖUPVÖÖHYURRÖQYSÖKJÖORYPSIHUJYRRIJJIVÖPKUÖSYLJOTÖSIUPSÖSIRTYPÖÖHUSOPNOUSSUKÖÖHIPÖISUORRYTÖSUYLLBPNÖSORRUKYJKYUJKYQBPSYLJÖÖNEVBPSUHYPYPPYPSIUPSOKSYJÖPKUJBSIHUJJYRYPSYUJBOPHUYLYRRBPUTÖYZYKKBPUQUKJBSYKSIKJYRYQQYTÖQUJSBLISOISKYJLISOURYQQYEVZYKKBQIJJÖNYRSBBPNYJJEHBPUTÖJEEZEPKYPHIOSKUIPYRQOUQÖÖPKUPBNBUHBPBSÖINNUÖKÖPJOUNOTÖRRYRIHÖPNEKJEJJBBQEEPJUNAEZBPSÖUSSUYUHBJHOUJOJYIJJÖÖIPYRQUÖÖPKÖQÖRRÖJÖHÖRRÖRBVZYNÖIROÅOYRVOÖRSYQUKJUÖRSINYLBUKJYOKOPTIRSÖUKJI"

def freq_testi_b():
    return "ÄIIÖZÅCZYZBJVHCRAZBVBDCÖZZHZÄÄCÅVBDIYVVBJICFCZGGRRÄRHÄVÖARVUIGÄIBBRBÖPYVHVÄVGÄIGHVÖIGHRHRIGHRRRZBVZGHCBRCBÄRHÄVÖARVUIGÄIBBRGGRDZUVHMBHPMGZGHIBBCBDQMHPÄZFÅRGHRHPMGZGHIBBCGGRÄPMHZZBÖPYVHVÄVGÄIGHVÖIÄRBGRÖRZGRÖCZHHVVGHRRÖCZHHVVBRÖÖVÄZFÅCZHHRBVVHÄRBGRÖRZGVHVGZHHZJPHVHHPJRÖHZCBAVHGZVBÄPMHHQQBÖZZHHMJPPÖRZBGPPUPBHQPAIIHVHRRBGZHVBVHHPJRÖHZCBCAZGHRAZÖÖRRÖIVZÖÖRVZGRZGZDPPGPPBHQZGVGHZHVYUPAVHGPÖRZGGRHRFÄCZHVHHIÅRIIUZGHIGYRÄÄIZHRÄPMHPBBQGGPAIIHCGHRFÄCZHHRZGZGZZFHMAZGHPRJCYRÄÄIZGHRÅRJCZARDVFPZGZGHPÄRGJRHIGYRÄÄIZGHRÅRHÄIJRDVZHHVZGVBAVHGPBÄRGJRHIÄGVBAVBVHVÖAZZBRZBVZGHCÄCCGHIIÖPYVHVÄVGÄIGHVÖIBÄRYUVGHRÄVGÄIGHVÖIBRÖCZHHRBVVGHRDIYVVBJICFCGHRVBGZAAPZGVBBZZGHPÄPMHHZJRGVAAZGHCÖZZHCBÄRBGRBVUIGHRÅRARZÄZJVÖPÅRHCZGVBGCGZRRÖZUVACÄFRRHHZVBÄRBGRBVUIGHRÅRDZFZHHRFRBHRBVBDIYVHHRÅCYHZDIYVAZVGARHHZJRBYRBVBDQMHPÄZFÅRBRGZRÄCYHRDHÄJDHPMGZGHIBHCHCFGHRZÄÖCÖRÄZRÖCZHVRJCYRÄÄIZUVBÖCDVHHRAZGVÄGZJRÖHZCBARZÖÖRÄRBGRÖRZGRÖCZHVÄRRJDÖPYVHVÄVGÄIGHVÖIDIYVAZVGARHHZJRBYRBVBÖPYVHVÄVGÄIGHVÖIRJRFHVBVGZHVÖÖPPBDPZJPÅPFÅVGHMÄGVBRGZRDIYVAZVGBVIJCGHCVYUCHHRRVHHPRGZRÖPYVHVHPPBARRÅRAVHGPHRÖCIGJRÖZCÄIBHRRBÖPYVHVÄVGÄIGHVÖIIBJRFRHRRBVBZBHPPBHIBHZRRGZRBÄPGZHHVÖMGGPBCIURHVHRRBRZÄRHRIÖIHVHHIÅVBRGZCZUVBCGRÖHRGCJZHHIÅRAVBVHHVÖMHRDCÅRARZÄZJVÖPJRGRFJCZGRDIYVAZVGAVHGPHCJRHAVZÖÖVHCUVÖÖRHPFÄVZHPBZZBZYAZGHVBÄIZBAIZUVBÄZBÖRÅZVBBPÄQÄIÖARGHRAVHGPHVZJPHCÖVJRZBDIIDVÖHCÅRHVCÖÖZGIIUVBFRRÄRRZBVVÄGZJRRBAVHGZÖÖPCBJRÖHRJRAVFÄZHMGCGRBRZÖARGHCDCÖZHZZÄÄRRÅRÖICBBCBACBZAICHCZGIIUVBMÖÖPDZHCRZÖARGHCBAIIHCÄGVBHCFÅIBBRGGRBVCJRHÄCFJRRARHHCARBHPFÄVPYZZÖZBZVÖIÅRYZZÖZJRFRGHCÖICBBCBACBZAICHCZGIIUVBBPÄQÄIÖARGHRBVCJRHÄCHZJRÖHRJRÖÖVAPPFPÖÖVÖRÅVÅRÅRGICAVBIYRBRÖRZGZGHRÖRÅVZGHRGIIFZBCGRRGIIÄZBAVHGZGGPMADPFZGHQRFJCÅVBÖZGPÄGZAVHGZÖÖPCBRFJCRBZZBJZFÄZGHMÄGVBARHÄRZÖIBÄIZBYRFFRGHIGHCZAZBBRBÄZBBPÄQÄIÖARGHRÖCDIÖHRÄMGVCBAMQGGZZHPVHHPAVHGZÖÖPCGRBRÖICBHCRCBZHGVZGRFJCBPAPAVHGZVBACBZBRZGVHRFJCHÄVFHCJRHGZZHPÄIZBÄRAVHGPHCJRHAVZÖÖVVÖZBVYHCYVBÄZFVZÄPÅRAMQGMÖDVMUVBRZYVAVZUPBDZHPZGZÄZBÖQMHPPMYPDRFVAAZBHRDCÅRAZHRHRAVHGZVBAIZHRÄZBRFJCÅRÄIZBDIIBHICHRBBCÖÖZGHRRFJCRBPZGHPVUVÖÖPARZBZHIZGHRGMZGHPCBHPFÄVPPVHHPAVHGZPAAVYCZUVHRRBYMJZBÅRJZZGRRGHZBMHAVCÖVAAVGRRBVVHHPBBVVUIGÄIBBRBÄPGZHHVÖMMBÄRBGRÖRZGRÖCZHHVVBÅCBÄRHRJCZHHVVBRCBGZZFHMPRJCYRÄÄIZGHRÅRHÄIJRBÄRGJRHIÄGVBAVBVHVÖAPPBJRÖHZCBAVHGZGGPHPAPÄRBGRÖRZGRÖCZHVCBAZVÖVGHPBZHPFÄVPÅRYRÖIRBÄZZHHPPRÖCZHHVVBÖRRHZÅCZHRÅRÄRZÄÄZRRÖÖVÄZFÅCZHHRBVZHRJRÖHZCCBGICAVBGIIFZBAVHGPBCAZGHRÅRÅRJRÖHZCBARRHÄRHHRJRHBCZBBVÖÅPGCGRBGICAVBHICHHRJRGHRAVHGPARRGHRRJCYRÄÄIIGGRYRÄÄIIÄMDGPAVHGPÄRRUVHRRBAZÖHVZÄCÄCBRRBÅPÖÅVÖÖVÅPHVHPPBHRJRÖÖZGVGHZAIIHRARDIIACBZAICHCZGIIHHRHIFJRRARRBÅRAIZUVBHZÖRÖÖVZGHIHVHRRBHRZÄMÖJVHPPBIIGZHRZAZÄÄCÅRHÄIJRGGRÄRGJRHIÄGVGGRAVHGPPVZIIUZGHVHRÅRÄRGJRHVHRMYHVBPHRGRZÄPZGVBPDIIGIÄIDCÖJVBRJRRBAVHGZÄQZGGPCBACBVBZÄPZGZPDIZHRÅCZGHRDCZGHVHRRBCGRÄVFFRÖÖRRBRJCYRÄÄIIHRVZHVYUPJRRBAVHGPGPZÖMMRZBRVBVAAPBHRZJPYVAAPBDVZHHVZGVBPIIGZRHRZAZRVZÖPYHQÄCYHRZGVGHZZGHIHVHRJRRBAVHGPIIUZGHIIÖICBHRZGVGHZÅRHÄIJRGGRAVHGPBÄRGJRHIÄGVGGRYCZHCAVBVHVÖAPHÅCIGHRJRHAMQGHZÖRBHVVBÅRHRJCZHHVVBAIÄRRBAZÄGZÅRHÄIJRÄRGJRHIGGZHHVBCBYMJPRGZRVBGZBBPÄZBGVBRJIÖÖRJCZURRBHIFJRHRAVHGPÖICBBCBACBZAICHCZGIIHHRGVBRJIÖÖRJCZURRBVUZGHPPAVHGZVBJZFÄZGHMGÄPMHHQPDRFVAAZBÅRGVBRJIÖÖRJCZURRBAMQGHCFÅIRZÖARGHCBAIIHCGHRÅRHÄIJRÄRGJRHIGAMQGHIÄVVAVHGPHVCÖÖZGIIUVBÅRÖCGHIGRGHVVBBCGHRAZGHRGZÖÖPGVBRJIÖÖRARYUCÖÖZGZAARBACBZAVHGPBDIIGRRURRBÄRGJRHVHHIRRFJCÄÄRRÄGZHIÄÄZDIIÄGZJRGVAAZGHCÖZZHHCÄRBBRHHRRÅRHÄIJRRBÄRGJRHIÄGVVBGZZFHMAZGHPBZZGGPJRÖHZCBAVHGZGGPÅCZGGRGVCBARYUCÖÖZGHRÖPYHQÄCYHRZGVGHZAVZUPBHIÖZGZGZZFHMPÅRHÄIJRRBÄRGJRHIÄGVVBÅRVHVBÄZBBZZBHIÖZGZHVYUPHIFJVARRAVHGZGGPGICAVHGZGGPÅRHÄIJRBÄRGJRHIÄGVBAVBVHVÖAPÖÖPJCZURRBÖZGPHPVÄCÖCXZGHRÄVGHPJMMHHPJCZURRBGICÅVÖÖRHIFJVARRBYZZÖZJRFRGHCRÅRJPYVBHPPGZZHPÖPYHVJZPYZZÖZUZCÄGZUZÅRHMDDZCÄGZUIIÖZDPPGHQÅPGRARBRZÄRZGVGHZÅRHÄIJRBÄRGJRHIÄGVBAVBVHVÖAZPHIÖVVHIÄVRAMQGMÄGZHMZGAVHGZGGPAMQGYRÖÖZHIGCBGZHCIHIBIHAVHGZVBYCZUCBDRFRBHRAZGVVBGRZBZHGVYRÖÖZHIGBVIJCHHVÖIZGGRZGHIRGZZBPDQMUPGGPÅCGGRGCJZHHZZBIGVZGHRAVHGZVBÄPMHHQQBÖZZHHMJZGHPHCZAVBDZHVZGHPYRÖÖZHIGRZÄCCBMHDPZJZHHPPAVHGPYRÖÖZHIÄGVBCAZGHRÅRDCÖZZHHZGVHÖZBÅRIÄGVHGZHVBVHHPMYHVVBGCJZHVHRRBDRFVAAZBÄVGHPJPAVHGPHRÖCIGDIIBGRRHRJIIGÖICBBCBACBZAICHCZGIIGJZFÄZGHMGÄPMHHQZÖARGHCDCÖZHZZÄRBHRJCZHHVVHÅRARRBÄPMHQBVFZAICUCHYRÖÖZHIGCBÖZBÅRBBIHVHHPAVHGPYRÖÖZHIÄGVBJICHIZGVGGRHIÖCIHIGHRJCZHHVVGGRCHVHRRBBMÄMZGHPDRFVAAZBYICAZCCBJRZÄIHIÄGVHYZZÖZBZVÖIIBÅRÖICBBCBACBZAICHCZGIIHVVBAVHGPHRÖCIUVBÅRHVCÖÖZGIIUVBDIIBHRFDVVBFZBBRÖÖRAVHGPYRÖÖZHIÄGVÖÖVRGVHVHRRBBZVÖIHRJCZHVAMQGHRÖCIGAVHGZVBÖICBBCBYCZHCRVUZGHVHPPBÅRYRÖÖZHIGCBCYÅVÖARGGRRBGZHCIHIBIHGZZYVBVHHPAVHGPYRÖÖZHIÄGVBARZÖÖRVUZGHVHPPBÅRHÄIJRBÄRGJRHIÄGVBAVBVHVÖAZPRFJCZGRDIYVAZVGGICARÖRZGVHÖRRÅRGHZVZJPHÄRBBRHRRJCYRÄÄIZHRAMQGAZBPCÖVBÄCÄVBIHGVBÄIZBÄRÖRDGIIUVBAQÄÄZARZGVARBZHIHHIAVHGPCBÄZBMYHPÄÄZPAIIHHIBIHRJCYRÄÄIIRIÄVRÄGZCÖVBBPYBMHGICAVGGRBZZBRJCYRÄÄIIRIÄVZHRÄIZBÅRHÄIJRBÄRGJRHIÄGVBYRÄÄIIÄCYHVZHRRJCYRÄÄIZGHRÖICDIAZBVBVZHZVHVBÄPPBHRFÄCZHRAVHGPHRÖCIUVBÖCDVHHRAZGHRÅRHPÖÖRZGHRVZÄIÄRRBCÖVVGZHHPBMHHPAPRÖCZHVÄIZHVBÄZBCGRÖHRRBÄVFHCCGZZHPVHHPZYAZGVHVZJPHCÖVHMMHMJPZGZPBMÄMZGVVBAVHGZVBYCZHCCBVZÖVBÅIÖÄRZGHIBMÖVBIIHZGVBAIÄRRBÖICBBCBJRFRÄVGÄIÄGVBÖRGÄVÖARHCGCZHHRJRHGICAVBAVHGZVBYZZÖZBZVÖIÅVBCÖVJRBJICBBRYICARHHRJRGHZRZÄRZGVAAZBCUCHVHHIRDZVBVADZPHPAPVBHZGVGHPPBÄCFCGHRRZÖARGHCJZZGRRBAVHGPDCÖZHZZÄRBHPFÄVMHHPJRÖHZCBAVHGPHCJRHAVZUPBÄRZÄÄZVBMYHVZGHPCARZGIIHHRCBHPFÄVPPVHHPHPHPÄRBGRÖÖZGCARZGIIHHRÄPMHVHPPBÄVGHPJPGHZAVHGZVBACBZBRZGVHMADPFZGHQÅRJZFÄZGHMGRFJCHYICAZCZUVBDIYVAZVGARHHZJRBYRBVBVUIGHRÅRFRBHRBVBAVZÖÖPCBHPYPBÄVGÄIGHVÖIIBDMMUVHHMVHIÄPHVVBCÖZÄCGVÄIIGZJRZGVZHGVAPBDIYVVBJICFCRBVÄPMHVHPPBVBBVBÄIZBUVSRHHZRÖCZHVHRRBDZFZHHRFRBHRBVBGURFJCZGRDIYVAZVGYMJPHÄIIÖZÅRHGRRAAVHPBPPBÄPGZHVÖHPJPÄGZRÖCZHHVVBÅCÖÖRHCUVÖÖRCBJRZÄIHIGHRHIÖVJRZGIIUVBAVHGPBYCZUCÖÖVÅRHVCÖÖZGIIHVAAVHIÖVJRZGIIUVBBPÄMAZÖÖVAVZUPBCBCÖHRJRYICÖZGGRAAVARRZÖARBÖRRÅIZGVGHRAVHGPÄRUCGHRÅRAVHGZVBHZÖRBYVZÄÄVBVAZGVGHPAVZUPBCBCÖHRJRYICÖZGGRAAVGZZHPÄIZBÄRAVHGZVBÄVGHPJPPBYCZHCCBÅRÄPMHHQQBÅRAVHGZVBGICÅVÖIIBÄZZBBZHVHPPBYICAZCHRBZZBGICAVGGRÄIZBARRZÖARBÖRRÅIZGVGHZGRACZBÖICBBCBACBZAICHCZGIIUVBHIFJRRAZGVBCBCÖHRJRÄVGÄZQGGPDPPHQÄGZPHVYUVGGPAAVGRARRBRZÄRRBAVZUPBCBCÖHRJRYICÖZGGRAAVAMQGAVHGPHVCÖÖZGIIHVAAVÄZÖDRZÖIÄMJMGHPÅRGVBMÖÖPDZHPAZGVGHPÅRDRFRBHRAZGVGHRRJCYRÄÄIZUVBÄZVÖHPAZBVBGICAVGGRVZÄIZHVBÄRRBCÖVFRHÄRZGIARRZÖARBÖRRÅIZGVVBAVHGPÄRHCCBÅRGICAVGGRAVZÖÖPVZCÖVGVÖÖRZGHRHZÖRBBVHHRVHHPRJCYRÄÄIZUVBÄZVÖHPAZBVBHPGGPRÖCZHHVVGGRVGZHVHMGGPAICUCGGRCÖZGZHRFDVVBAVZUPBAVHGPAAVÄRGJRJRHVBVAAPBÄIZBBZZHPÄPMHVHPPBCBAMQGYMJPMAAPFHPPHPGGPZÖARGHCÄVGÄIGHVÖIBZÖARDZZFZGGPVHHPJRZBÄRGJRJRHAVHGPHGZHCJRHZÖARÄVYPGHPYZZÖZUZCÄGZUZRYZZÖVBÄVFFMHHPAZBVBAVHGZZBCBBZGHIIJRZBYCZHRARÖÖRAVHGZPÅRYMJPGGPAVHGPHRÖCIUVGGRHIÖZGZGRÖÖZRGVÄPRJCYRÄÄIIHVHHPÅRHÄIJRÄRGJRHIGBZZBÄIZBBMHÄZBVFZÖRZGVHHRJRHAVHGZVBÄRGJRHIÄGVVBVFZDRZÄCZÖÖRDRZBCHHRJRHAVHGPHRÖCIUVBACBZAICHCZGIIHHRVIGGRAVHGPDZBHRRÖRCBÄRGJRBIHJZZAVJICGZÄMAAVBHVBRZÄRBRAIHHRAVHGPÄRHCÅRHÄIIARRZÖARÖÖRVFZHHPZBYICÖVGHIHHRJRRJRIYHZRGMZHPHPYPBAVHGPÄRHCCBARRZÖARÖÖRCJRHAIIBAIRGGRJPVGHQBÄRGJIÅRGZHPÄRIHHRFIIRBFVYIBDIIBÅRAIZUVBYMQUMÄÄVZUVBHRFJVAVHGPÄRHCRÖZGPPJZPGVZÄÄCÅRCJRHAMQGHZVUCBDIIHVYVZÄÄCYRÖÖZBHCÖRZHCBHCZAZBHRÅRARRHRÖCIHVVBÄPMHVHHPJZVBRÖIVZUVBÖRRÅVBVAZBVBÅRAVHGPDRÖCHARRZÖARÖÖRRFJCZGRDIYVAZVGAVHGPÄRUCBHCFÅIAZGVÄGZÅRÖICBBCBACBZAICHCZGIIUVBMÖÖPDZHPAZGVÄGZHRFJZHGVAAVÄIÖÖVÄZBARRÖÖVÅRARZUVBGZGPÖÖPVFZRÖIVZÖÖRMÄGZÖQÖÖZGZPHCZAZRÅRFRHÄRZGIÅRHRFJZHGVAAVÄIÖIHHRÅZVBHZVHCZGIIUVBÖZGPPAZGHPGZZHPAZGHPÄRIDRGGRCÖVJRHHICHHVVHCJRHHIÖÖVVHÄIZBÄRVVHHZGVGHZÅRVÄCÖCXZGVGHZBVCBHICHVHHIÅRAZBÄPÖRZBVBARRBÄPMHHQQBÄCYUZGHIJRÄIÖIHIGÅPÖÄZHICHHVZÖÖRCBVGZAVFÄZÄGZDRÖAIQÖÅMÖZYRGCZÅRÄRRÄRCÅRARZGGZCJRHGVÖÖRZGZRYMQUMÄÄVZHPÅCHÄRARRZÖARBÖRRÅIZGVGHZRZYVIHHRJRHAVHGPÄRHCRÄRBBIGHVHRRBZYAZGZPHVÄVAPPBJRÖZBHCÅRÅCHÄRVZJPHRZYVIHRAVHGPÄRHCRÅRÖICBBCBACBZAICHCZGIIUVBYVZÄÄVBVAZGHPAVHGPHJCZJRHÖICURAZÖÅCCBZRÄVGHPJZPÅRGCGZRRÖZGHRRGVARRDRFRBHRJZRHMQDRZÄÄCÅRMADPFZARRZÖARRHVYUPPBHPPÖÖPGICAVGGRGVÖÖRZGHRDCÖZHZZÄÄRRÅCÄRCBVBBRÄCZHRJRRÅRDZHÄPÅPBHVZGHPRÖCZHHVVGGRRJCYRÄÄIIÄZVÖHCÄCGÄZGZJRÖHZCBCAZGHRAZRARZHRHPGGPCBMAAPFFVHHPJPAZBÄPÖRZGZRRÖIVVÖÖZGZRJRZÄIHIÄGZRRÖCZHHVVBJCZARRBHIÖCRZYVIHHRZGZJRÖHZCBCAZGHRAZGHRAVHGPARZGHRGIIFZBCGRGZÅRZHGVVDCYÅCZGÅRZHPGICAVGGRDPPHQGRZYVIHHRZGZGIIFHRRÖIVVÖÖZGHRVDPCZÄVIUVBAIÄRZGIIHHRÅRRJCYRÄÄIIÄZVÖÖCÖÖRCÖZGZAVFÄZHHPJZPDRZÄRÖÖZGZRJRZÄIHIÄGZRRGZRRÄCÄCBRZGIIHVBRHRFÄRGHVÖHRVGGRCBAMQGYICARHHRJRVHHPJICGZHHRZBVBDPPHVYRÄÄIIÅRIIUZGHRAZGRÖRCBMYUVBDFCGVBHZBAVHGPDZBHRRÖRGHRAAVGZZGMÄGZDFCGVBHHZÄCÄCARRAAVAVHGPDZBHRRÖRGHRGRARRBRZÄRRBDFCGVBHHZRAVHGZGHPAAVCBHPMGZBGICÅVÖHIHRZFRÅCZHVHIGGRÄPMHQGGPHPGHPZGCCGIIGCBHZIÄRGHZGICÅVÖHIRÅRBPZUVBGICAVGGRHZIÄRGHZGICÅVÖHIÅVBAVHGZVBCGIIGÄCÄCVIBGICÅVÖÖIZGHRAVHGZGHPCBDICÖVHGZZGDICÖVHÄCÄCVIBRÖIVVÖÖRGICÅVÖÖIZGHRAVHGZGHPGZÅRZHGVVGICAVGGRMÖDVPBPJCZAAVAMQGÄVFHCRVHHPMÖZDFCGVBHHZRHRÖCIGAVHGZGHPAAVCBGVFHZWZCZHIÅRMÖDVPBPJCZAAVAMQGHCUVHRVHHPAVZÖÖPCBYMJPÅRHCZAZJRAVHGPÖRÄZBMHHZVUPBVHHPAVHGPGVÄHCFZBHCZAZÅRHCHHRJRHJRÄRJRGHZYICAZCCBÖICBBCBACBZAICHCZGIIUVBÅRZÖARGHCCBÖZZHHMJPHÄMGMAMÄGVHÅRCJRHRZUCGHZCÖÖVVHAIÄRBRHPGGPHMQGGPÅCJICGZRÖICBBCBACBZAICHCZGIIUVGHRYICÖVYHZAZBVBÅRÖRRÅRDCYÅRZBVBMYHVZGHMQCBVFZHHPZBHPFÄVPPAVZUPBÄRZÄÄZVBHRJCZHHVVBRHIÖVVCÖÖRAVHGPÖRÅZVBIYRBRÖRZGIIGÄVYZHMÄGVBDMGPMHHPAZBVBÅRÄCFÅRRAZBVBÅRGZHPHMQHPCBHVYHPJPÖRRÅRGHZMYHVZGHMQGGPVFZHCZAZÅCZUVBÄRBGGRAVZUPBHVÄVAZVBDPPHQGHVBCBDVFIGHIHHRJRHIHÄZHHIIBHZVHCCBVZHIBHVVGVVBGZZHPGMMGHPCÖVBÄZBZÖCZBVBVHHPAVHGPYRÖÖZHIGCBHPBPGMÄGMBPZÖACZHHRBIHDVFIGHRJRBGRÅRHÄIJRBÄRGJRHIÄGVBRÖIVZHRVFZDICÖZÖÖVGICAVRÅCHHRGRRAAVHIHÄZHHIIBHZVHCCBDVFIGHIJRRÖICHVHHRJRRÅRÄPMHPBBQGGPHVGHRHHIRHZVHCRÅCHRÄPMHVHPPBAIIBAIRGGRHIÖVJRZGIIUVBFRHÄRZGIÅRHVYUVGGPAAVÅRRBBVHRRBAVHGPBÄRGJRHIÄGVÖÖVÄZBHRJCZHHVZHRVZFRÅRRJZRÄVZBCÅRÅCHÄRJCZJRHCÖÖRJRYZBXCÖÖZGZRÖPYUVVUIGÄIBBRBHPMGZGHIBBCBDQMHPÄZFÅRYHHDGKKKVUIGÄIBHRWZWZJRGÄZDCMHRÄZFÅRRGZRÄCYHRGZJIHDHÄRGDLJZZHRHHIAICÄÄRIGMHÖÄIIÖZÅCZYZBJVHCRAZBVBDCÖZZHZÄÄCÅVBDIYVVBJICFCZGGRRÄRHÄVÖARVUIGÄIBBRBÖPYVHVÄVGÄIGHVÖIGHRHRIGHRRRZBVZGHCBRCBÄRHÄVÖARVUIGÄIBBRGGRDZUVHMBHPMGZGHIBBCBDQMHPÄZFÅRGHRHPMGZGHIBBCGGRÄPMHZZBÖPYVHVÄVGÄIGHVÖIÄRBGRÖRZGRÖCZHHVVGHRRÖCZHHVVBRÖÖVÄZFÅCZHHRBVVHÄRBGRÖRZGVHVGZHHZJPHVHHPJRÖHZCBAVHGZVBÄPMHHQQBÖZZHHMJPPÖRZBGPPUPBHQPAIIHVHRRBGZHVBVHHPJRÖHZCBCAZGHRAZÖÖRRÖIVZÖÖRVZGRZGZDPPGPPBHQZGVGHZHVYUPAVHGPÖRZGGRHRFÄCZHVHHIÅRIIUZGHIGYRÄÄIZHRÄPMHPBBQGGPAIIHCGHRFÄCZHHRZGZGZZFHMAZGHPRJCYRÄÄIZGHRÅRJCZARDVFPZGZGHPÄRGJRHIGYRÄÄIZGHRÅRHÄIJRDVZHHVZGVBAVHGPBÄRGJRHIÄGVBAVBVHVÖAZZBRZBVZGHCÄCCGHIIÖPYVHVÄVGÄIGHVÖIBÄRYUVGHRÄVGÄ"

def freq_testi_c():
    return "ASJMYRÖPEHAXFHAUSPIQFKQÄÖQLJWQÄXINQYQAITUCLÄLHTKZKPCBÄUVVÅSCHÄJZÄASGRBPTAKUCHCBVWÅKCLÄKPSDGÅPQXÅÄJTTDVÄIGKÄXPVYJLTEEDLPZRRYMTENPZRÅÄÖÖKZWRUDAFÄHTKÖLHCYMTIDUÅMDÄÖWYHDQGFÖQDCDBOYZÄYIYYTVKOWÄAPQYZKQXGXSZCLZÖYZYÄKIZUKTEPHHTGLUNRWTZPÄESLRMOMRIPMFPÄEHZRRBÅXQOMLWYÅFVPUYQTZZULIBCJPQVÖQTZLAZZXLVTÄBRIÄILUÖCBJVSGXMMZOOMDWXQRTKRAIQZJTDIHDCÅÖCWTKDBQDPINCYRVÖWIÅPAZRXKRUERDÅGCSGDPXJZNÖVBDJXWÅZVRIBHQSWITWLVFEJQÖÄRGÅMRXYQNCHJUZKPAÄKHASVTXLZMMHMWRBQHJLXPFHPGWÖZIÅMDIDGVÄPCÅISRAÄZVIIRWCBTNUJMWDPYÅFOCFÖIXENPNCHJUZKPAÄKHASVTXLZPQYZKQXGNUVÅCFYÄFOMZJLJZXOBVYGDÖIQJTSZRTRHTZGBMXIVIHJSPUHKVÖSGDÅTVGXPRZÖRVWSJDSVRTJVYLRAJKJLTEYHÄFTCULVNXÖZDEDBGSÄXPVMTÖIFXXPRZCBÅTGJAQVPBÄWPLÖJVJTÖMKXLPIÅMFPNZXÖÅGQBGGÅÄBÅFKLPVZQTLXHTGLUNRWTZPÄESLRMOMRIPÅLÖHTZSIRTLXEBÄKILCBLKRYOYEXÅCEIWBHQDINXÄLÄNOTLRSCFPVRÄRÄDEZCBVKHPTKLTÅASDQCJFFLLOEDMJOIÄAOCHPVHTÖÄÖIHPRYLRQQTDAQYEZNOKCBWQYJLVNMBIVÅZFQHXQWLJEJPVKÄBOFLSÖWJHDGBNCBCÄLEÖUVHXQOYICYÅZTBMJEWCÅFKGBGRBOPZXIMAISUAUGDYMFEJRAPLZAÄKHTMJRTFRYCBASBBOQÄLXRRÅRWÖGSÖLRTQIRPSJUSMZENPVXJQÄCJUTONXBMFFEPULRRAQHXLSLEDBVTÅÅWQMÅPÄZRTRHÅÄAPLSEBÅNEHÄBKCULUSRAÄZVIIRWNOWQYJLVYMIIIÅCFLLKIXMFEHÖVÅQXÖÖVFPVCSCBOMPRXÄOBWILXXLUHQHSMXHXGKXXPGRÄDPVÄRNSZVJGÖSPPNSRÄRÄKXEPHPLHÖMYIPNUVTRHWJRBÅGFITAWJÄBKCBXIXITFJJOJÖLPWKZUHOVARZCBEPIYLKHOMSVXLYHPHDAGDZZFERLUYÄHAZGWTSVPJMTOBRXQJHZÄLIDQGÅZÖWVODRGJIDÄBUÄBJVÄTOLZRLÄFKYWKZUHOVARZCBÅPPOLKÄVZVJJDCÅÖCWTYLXNUVWÄALPWKZXTAWEQTPVUTRÖMTXYWJQJGHÅÄFAÖIVJAZREKWPLÖLVJIOIEPTLUZJRRÄBLJZJMDRVRTRWQLÄNMJEWCGPEHTTRWPVLYHLVYGBRMTYTVDEDBGKÄAWITWATVKÅÄFFLUISÄTWQÅMVCFHRGTOZHPOSRZCFÅGUTOGHPWXLAMATCFQHXÅZXHRÄLXZTZAÅTTÖÄÄDHÄULRZRMTZJTDEDBVKÄAWMPEYMFMÄQYVAÄPDYFPTVHXJRNCHZUMKWLZXÄQVUÄGBMOISWXOXWJTMTSAGHOMLJSPGÅÄÖLVJIWIÄIJSHHLWKZQTYIYEEAYÄQRAWSBGKCEWCGIPMBIJXYVGVWÄALPZVITIVIYSCGBHLGPVODZUECIRVYQÄLXKJUIÄCHQPRCFÅFGJBLVQBCÅVLVYSUCXMJJQCBUWTSITILÄLWFCÖHMARÖRWPÄGGÅBOFPUPÄÄÄVÄAKJÄHÅQRXÄRÄRIÅMDJPUBRÖMUVVÅSLTPAGHÖTONXBILXICAHRTSMTBTSKSCÅJYGXLUGJNPZVÄLCTKPAÄKHASVTXLCJFGZURTYLKPTEVUQDPTGHLAYIDÄBSCUYQTZPVWSHBVMÅFZZJDTVÄIDQBHPRAÄÅFÅLVXXPRZRZWTGJBRTQIRPSJROISENPÖIHPZKPCBÄYQLÄLEBJRMGBWGTWLZZLTPGHKALUFÖWQÄLXRRÅRWKTPTMFYIWÄAVAYSMXHTLJSJRZKCGBWXTXGKXXPGRÄDPVQBJUEIWFPUTZAVODRÄAPBGFPIGOIMXYÅVVUCHZMFOVODRÅLCBJVYHRRNFBUIFHXQDGPGXFRJTTDHXLAPLZAÄKHAWEWTIVUEPWTKHKAZVLZXLPFPOKHTVÄIDÄHÅSDÅLGJPZVJSPCYBBTVMXYÅSEJRÖHEVYWSJPTZZÄQZVLGZKNHLLASLCFRQRXPKJZKCWQERYÄBBMXTÖÅVQCÄAGHÖTONXBILXYÅÖQÄULUOWÖWLXEAYMGBWITWALVQBÄBKQÖLOOWPÅLSHÄAFQHPZYALXZRFYGHKALÅEJBÅGQÄBRNPVOITZLZVRJCFHQWKZNXÖZVVDÄGTMHAAGHTOÖIJFVSQZYOLEÖÅEEJQÖGDGBZFCAAKOHGWÅJZRÄYFKZKQQJGZPUASXÄQÄDMZRGWÅFAUDBZUVXJBRTGUÖWZJZKCWQZFHTGLUNRWTZPÄESLRMOMRIPUVXIJQMQHÖHSIDÄAPBPZRQULOKDAÄVPCÄBUZGBITXYWXLXLYHJJXQRÖZVKBZBRTJVUWTXYÅNQYGBHJDIÄÄÄLXJMBZBKYFJSTTANARIIUHKZAPUVVMQTQTAUGJIQTJPÅGQINCYRRDÅGCSGDPXJZNÖVBDJXWÅZIDJZNRGBIZIÖFYIJQWGPCÖLTÄYOGQJCÖLTZAMXÄYOVZXTVUCALVMTDÅVQÅZÖSCÖTOHXBDYIBQVZÄAXIYTVOTPBCFMMHMWRBPVLMBJGWMFBMXENPZZXLVTÄBRIÄILUÖCBJVSGXMMZOOMDWXPPRLRAJRTYLVRDÄHZJIBÅVXWMFMLZFSBGXGYJPZKOTNVUGWZÄHEWTÅDHFVYPRÖÅRKBÅHIBCBPCIÖWVTXGKXXPGRÄDPVOYZÄWSBJWGPYPZXTÖWXLLZFSBGXGYJPZKOTNVUGZAPUVVMQJSPYLPFLZJXBÄVFXRMKCFTXXTVÄAOXLRÅRAJÅZXÖÅCEFDQYBRXMXALVHPTAVYÄGMIQEXÄNOTLRSCFYIYUPÄVPCSFHPAPLGDSMJVBÄBKQÖLOKDRIJEDRVYÄGPVVBLÄKMTJÖHDZYTEDOIJIIRJYSHZZKYBMJWEKÖPQHLVVQPAZRXKRUERDÅGCSGDPXJZNÖVBDJXWÅZWJWFÖGÖVIOWÖWLXICJLLVXITZAWEWAÄGCLRAXDYÖQVXLIRUÄÖPZKDWQÄXBÄXLLCXÄKBPAAWÄMBZMTSZGWTWNIHIGHKYPÄKDMIJXÅCFYÄFYILÄYVKMWÄXWYUPVRÄAÄVRLGÖRCHJZLSÖFDHHÄHYCULVJQQHJSHBBPLXPVÅJQWJQTBVZYFVWTIBILIHÄULHPXÅZRWTYLXRGVKSCLYCLVFIDÄHÅKZYQYJPZAIHLROÄFPVYAGTYMZFVÅÄHBNXRXRVNRKGÅZÖWLNXBWXLTRHZIMWLOZSMLIDÖCYBVBIYÄMMVOJÄBKCAKRRÄRPZXXLRÅRHLUKWXWLWLÄFHLUPLGCXGKXXPGRÄDÅFRÄAÄVRWGGRSHPZGWPÅEIDÄFICHAOXKÅXZRAMAKYWÖISJTTDEJRVUBRAÄNXÖZECIRVYQÄLXKDDGXOXPHPJÖÖGIAWQÄXIRCYRZYÄXXAÅZJSPRÅRDWIZILXSPÄQHHLUPVSTÖÅABHDMSJVÖNFHZZYRÄLXLLOÖÖTWPZYIQPVUFRÖÄÄLLVGVDÄPUBFLÄYHLLAOTJHVAYOISÄOZGXJCBZQHJTRDTVÄCHCBHLBLVEDDIYHXLJHPUINFHZZYRÄLXLLHÖGJWPQCVTDHMMHMWRBAAEJSPUHKVÖNFHÖIKSCKRYCBDIXXYMFSHKHPRHLZYKNKTZXLCTDZYTGDOÅYECJRUBGWIMJGATVHGBÅCÄDIRÄQQXIHÄULQZRÄOBWLZRJSFUCFTVMXYNARBÄBKQULURTYLKPTEYHPPYLDADIDMYGTLPRBÅOZBZZKQLXLPHTLOZLZZSVFÄVKAPZLSÖPGTFLZUEGDQYIYIJXZÅFHBVBQMXYOTPBÄBKCULURXUWFIDGZZFCNSKOAXZPTBVSÄXPÄUCRÖDHXRZZCBLÅZXTÅÖSVIVCTAZKNLLZYIJDQYQHLTGDOÅDEZCHÄRRYNFHVIFEWÄCJFIAIYEXTQGAÄULQSÖDZTOMFREPUHKVÖQQTYÅCEWMAPLRYÅKDTVGQCZGÅCFASGFPÄBEZZFZZÄPZVQLÄLHTKÖLHCYMTAZUEIHDOLLBGKNTYÅVXJQDLJRZUMKWLZXEAYKYPÖLKJDQCXÄEHHRHAISJWQÄEYGBSZBOIXXZKCWQFRYKQUTOZSMLEJRGLKRBKNXYTAOIMAGTFTOGCLÄXLXPZUMAXGYJPZKOTNVUMTSÅUCWIFHIJRNCBAXKBLZVZWCBHLÖPLTÄYOZRUMFKCWKZUHOVARZCBZLRÖIYJCXHHTRVYÄGBQRBLÄLNRKGÅZÖWIJTXWXLÅCFYGUÖWZJAFVXJÄÖSÄWTVRRYLVVXFRYQRXUGCKRDMZFVÅÄHBNFBUIWBWCUHKCNPNXÖZAHHMHÅGUPÅZEÖIECIRVYQÄLXKDVTTQCCUOZBDQYDTVÄXÄJÖPPZVÅJTRMFWTPSLRGZZJDTVÄWJZÖSCFUIMYKTBEDBVZNQÖÅSQWÄAPBBVUKZYQYJPZKSCQRRCBRGRBPZUZXPJFEVÖZKZPZARZCBHRHCXVWLÄZVTDQYMFOVODRMFWQÄHÅJRRMTEXÄZPXTZZGCYÅUVSZVHÄMJLPÄAISÅPÄGGAQONÄFLVZXÖIJWTKAHKQUTOZSMLEJRWGJÅLLGCTLJSJRCJFWTVRTYLKHTKÖHLUATGZTLZWJMFHKPAÄKHASVTXLDEQRXUGIJÄLWEKZKÄXÖMJTYOVVTLHLPRANFHSMJVTPBHQAZÄYLLZAKÅCHOCÖAQTZQWJWCÄHZJQQÅZHKUKZIIFPDHWQMJAXUVIKOSQGÖLYAÖQÅXBGXÅQDKZYCITGQTRHKÄATLXEBÄGGAQOFPRDÅGCSGDPXJZNÖVBDJXWÅZQTRGSÅWAÄXSXÅNXÄJÖYGÄALGZPVKXTJAHLBJÅZTYMFSVFVUFRWASÄWRGRIYXKÄAWMPEYMFWLKWPLRWXDJDQVTHGÖFLUIZEAYIKJÄLGRBRXQYÅZKCIONOÖKBTADÄYÄZWEKGWMFBIÄILUÖCBJVSGXMMZOOMDWXCBSGXBÅZTBÅJBWCHZDQÖWXWYQFKEKHLJVDQYXÖQFKTTVÖCBPUGDRINWTKYFJÖPTOZMMLÖWCÖZCGLUSTAICKRJÖLPWZÄHEWTZRJGÖSQDZZZXÖWXLXTVUCALVMTDÅVQÅZÖSCÖTOHXBDYIBQVYZÄYIYUWIFHTLBHRGWÖZIÅMDIDGJFPÖOÅSRAÄZVIIRWCBTNUJMWDPYÅFOCFÖIXIWÖLWFCÖLLZPÖXEÅIECIRVYQÄLXKDTNGXUMÖSDQÖPKHÖIJSVFJFPÖOÅSRAÄZVIIRWCBTQYÅZKCIODQYFVÖZGHOMLXTÖVÅWUPZOFÖICXÄIVUÄHBUEIBMJWAÄDMÅFOISXÖSVRFJRJCFLÅHTVWEXLIRUÄÖPZTTAJZXTJAÄPRÖUKWLVÖIHPÖHLUATGZPVÄEHÄBÅCFLÅKDÅTVXIGRSJRQQTBJVYEHCGÅTFCÄUHPNLIHQCTJZAÄGDÅFZZXLVTÄBRIÄILUÖCBJVSGXMMZOOMDWXQHCPJTTQTTLJSJRGLTVYMSTYOKSCQÄHQMYIYFINJMTRJRÄBLTKHPVDMZRÖHEVYWSJPTZZÄQZVLGZKNHLLASLCFRQRXPKJPVWEHRYLPFLZTTQQFRIGUHEDILKDWQKXTLJPJÄPÄEHQHJBBBFHRFPLGDOFÅDHMFKLZYOKDCÄÅSHKRKCGIZQEYÅLEJCFHBVUGSIBGDPWFVÅQCXJÅWAUVRDCBHRHXQTÄAÄZVÄCFUÄYLZKDASQPWGXOCHLÄZYÖGENTHPTQHJTRWSMLSVFRÅRGVDRWTOÖIJCBIMFOMZTAQWITIHHLUPUFÖWQÄLXRVUÄHBÄGCPLESJQJHPRYLKWLUECIRVYQÄLXVQWQKXTLUPQÄCÄKHLLZWCCBHPSPÄYZÖÖHTXLÄVKUINXTXÄAPBÄHÅCBOIYJSMJVCZGÅCFASGFPVNCVIVYRZWTXRNSDMZRGÅMFBQTJÖMKWXDQYÄHBXRTBÅVTQJZZRRYLKDXIJWÄYFMWÖWMXYKZGVWLZUEVYFXKYLZVWCOYCBSIXJDAVREPBHZBOZGJAZVHÄIRSRCNPJTXQYVERHLLGAÄEBWVARZZFLLRYVGDJVNEWBVUTRÖLDYKZGVWLZUEVYÄXROLZMAPRMRWZÄHEWTKZCDQYBRXMXYKZJEIMATÄFPVÄTÖMFIDMFTRZBÄGHAÖXGRTVUMAQQTBLVYWWÄASÄBOÅRTRÄQZRPFPLHPSÄTWQÅMVCFHBVAQMJTTDHXLHÄPBPZODRMFJÄLÖHLUALGCWIFHIJRNFRÖGTWISNEBGWPAVÖIZITOLVXEOUEVÖÄOWTOVVXMTOICXUKHQHJLENDUGBRÅÄÄAÅFEHRXGPROMZÄRMFKRJÖHLUPLGCWMBSDCBPGGSWIAPDKTXJRKCÖLOKJZUÄYBBVÅGGPVGIBMAWÅMTRCMDUUVSAVVWCHMÅFAÄGBLVYWBÄXLRIBITYKZCEDÄUHMTSÖYTAWEPOAÄHBVAJXOBIYIDLCYBRXMXÄVIFWAÄUVKZYITIPVAREKAFQHPZYALXZXÖÄXFPGJSKHÅFVXJBRTJVUWTXYSGQCCFMYVYVBVSIFWTRHZNVWIUCRÖDHXRCJFUIGXWPÄNMARZNRRBÄYTXÄDMZÄWPLÖJVJTÖMGGAQOOÄFXHPBTOÖIJÄHÅQVXIZVSMFPÄIGVKQDZOZLUVXVFVYGBZUSRAÄZVIIRWCBZKNIZUDEDBGSÄXPVYFPTVVTTULLRYTKWYQFKXLSVPUPNFHZZYRÄLXLLGYIXTAÄMTFBRÅCFLÅZÄWTVXJHPTQHJTRTOIESVFYLPFTLXEBÄKBTRHHJÖLNODWGFHTPVOÄFAISCLUUNBGXOCHLÄZYKTBEUYULBRXWIÅSMJVÄBFVRHTLKIBWJECZGÅCFASGFPVCPRKALBYJVÄÄAVARZRZSJZÖQQIOIÄIDQRYÖVBÅUHOVARZQHFJÖPZPTRNUPÖÄBKCGÅHXIXFDXÄJÖKCBXQTÄAÄZVIMAZÄÄPVMRWTZVSTVYTPRMXHPOZVÄLXLLRBÄÅFÅLVXXPRMÅFZZJDTVÄIDQOHRHWIMXYWEXXJVÖGGTWTIZKÖVTBZVTVÖSYTXPZXEAÄZYXLZGDBMJEHQRTKRXHPBTOÖIJÄHÅDQWRGWLUAHHMHÅMTSNODWIFHIBRTJRYLYBLOAHXQHVPRXGYJPZKOTNVUNOAISCLÅTXJQCTGULOXXOIFKTPRURVÖIYYKZÖIHPRYLRAUUJAAVVÄEYLRYPTYÄYOÅSHQAHRGWHLIBZUQITGRPZQÄRÄRÄKTSPGTYÖAÅXWASJMYRÖPEHAXFHAUSPEKRÅRULUOWÖWLXEAÄZYPÖIÄILUÖCBJVSGXMMZOOMDWXKRÅQÖKNYJÖHEWLRZSJFTSYWLOZRIRRSKRYVEIBIFIDMTOCBSIRLXQDNELGEEULURXUWFIDQJTDZYIRFIÄNMTNFPJPYLDHJSFEIDZUQÄOISÄAPGGACMWYJXVOLIQFXXQCTQDZZZTDÅVQÅZÖSCÖTOHXBDYIBQVLLÖTOZIBILWHYULRGQHXEÖLFMDECTRVWMÄÄAMJMDERÖCJPVKCLVÄELQRTFPWTKBTOWIJWULJGPÅGCXIKEAEPSJVÖNUJMWDPXLHPJÖAXUHBMJSVFVÖCBPUGDRINWTKYFJÖPTOZMMLÖWCÖZCFJSTTAJDEDBRULRBÅRKBÅHIBCBPTPÖTJIXGKXXPGRÄDPVOYZÄWSBJWGPYPZXTÖÅDYJQDLJVYQKKÖWHECZGÅCFASGFPVAJERSVJÖQHXÅPZJEHMTOTPÖTJIXGKXXPGRÄDPVOÄAPGGACMMÅFSMXHLZYIJRRICHGLKHTXJEARZRCBLÄZCJÅLIHQÄHNWKZJTXMJOTLDSÄTPZGIMICSCRJRÄBLTKHYIKFXRRSKIÖIXCPLVRÅCFYJRYLYBLOZRZÄFHLHPZGIPVHPTRGPÄÖWILÄYTTRWÄFLQHDZÅJZZZJJCFZMAWQYJLVHBXTVUCALVMTDÅVQÅZÖSCÖTOHXBDYIBQVZRMÖAOBVIAHHMHÅQVDMTXXIFKIMAZIRADTTAXSJHGRÅTÄLVGBPZZRBGXÅJRRMTEXÄZPXTZZGCYÅUVSZVHÄMJLPÄAISÅPÄZRUÄFÅFVÖZGHYIÅMDLGPBRRXDWPVDMIRRUTZWSKJJZÅDHYÖKPRBZKWLVYBYÅFVPUYQTZPVMXYMFTÄUPÅDHVWFWJÄHLPROMPRXÅLCBJUOCHAWSUCLKQTLBLLRBÄSÄYQKXXPZLPBLPGHPVKOOJUPEYPÄGJBNJCCHRQZAAÄEBWLÖIJMTOÄHBÅQOWLAKÅCHLLSZZJXBIKMUCRRRRYLKCKRDMZFVÅCBLÄZJLUZHCMHZTRÖITWPLVQCZGÅCFASGFÅFDMIRRUBZASÅJPZVHXQALLRÖJKJAOJYFNVUICXLDYÖIEXÄJÖHRHPVJTAÄÖIHPAFQHPZYALXZRLZTRCFBQRBÖGXOBGXÅQHZZZÄYÄJIIQVMÅFLÄZFWILWTNOSGGBITWPVEEHQZEPWGTRXÖNUVEPUUGBRMTQÖÖFHXPULYFPVNTÖÄNZTLCYLRJVJHLÄKVTBZRÄÖBWIÅOIEMWPCÅRVYÅYJJTDRÄLXFPVYITDLVTRLÄUKCBDIXWINUVEPUUGBRMTJÖGYHXGÄYÄWBNUJMWDPITAMÅFOISXÖNUVHÄGVKALZKDDIJIDCBVPABQZJLZKYVAPÖCBZULÄYTVRWQUHKÖLVJIWIÄXOTPYPZYÄKADIDMYGTLPROMYÄRÄAPBBVURIÖVKHTVÄIDDZUJRYLYWLUDEDBGSÄXSIXRYLSOLÄÖPDZNMXTBÅAKJPVNYBRMXJTLAKTPVVAYVWSCPZÅDHFCWNBTVMIDQKWDÄFÅEQÖIJXBQÄIDEPSJRYLKWLUDIÖMBLLZTÅNENSZÖINVSÄUPTGZPÄGQZSÖKCHTÅKDLÅLIÄQYVAÄPDÄCZKÖZTPULRWKZYJLTVRWQÖHEVBÖZTYNUVAÄBHBRZKNKAIKSCJMJIROMYUÖDLEWCBUMFOISXÖQCEDQÄHBCXQTTYÅZRÄLCTKPAÄKHASVTXRÅHEPÖÅEAPZHBTRHKÄAWMPEYMFOEKALPWIMTDGKÖEDQRÅRGÅMRTZUÄYBBVÅMTSLDRÖLZXLGÄÅGXBIZJAIEXBGXHDZYTEDOIJIEAÄZYYLZSSUTAKÅCHHRHAMSTBKÖIDJZRQCXHÄHTOVQTRTOCFTVUCXGKXXPGRÄDPVUVSÅGQBÄBKQÖLOKDAXZPTPRÖBVYITBPLFMDEVUÖCÖLKYKZGVWLZUEVYÅTTÖIKXKNDKÄHPZGIBQDPTRHQZAAÄEBWIYECMTOFVÖZOWÖWLXIYRÅRRWTGYTVDCDBRYCYLZYTXUVQSHÖPEYPÄGJBNUPÖÄSEBVOISENPÖIHPZKPCBÄOWPÅLSHÄAFQHPZYALXZRAJPTKVOPEDDQKRÄLXÅGÖWQXÄVÅYEZCBZÄFMMZIZZYRÄLXZRPWTKHUIÄJSJÅHLUPÅVSÖÅEBBRZSJUPVSÄYQKXXPGVKGLSKDRGDPXPQÖCFDGMXÖZZKXPZUEVYIZJCXHHTRVYÄWKZUHOVARZCBZYRBÄRTRMFSCRVSCJTÅOEYÅGGÅPRKGCDMXAAIELXRCJIGIOGHLVLIHÄFZÄAXISSUTAKÅCHHRHQHRÖLLVQÄBFVRHZKNYTVDEDBGKÄAWITWATVKÄBVZRCÖISRAÄZVIIRWCBÅFYTXUVWRRHZMATLGZÖMYEDERYÄBBMXTANUVÅCFYÄFYIYCZÄKZTPZNFVBPKBAQFKYMFZKRBÅRSQÅLVSKGÖQÄÖQLJWQÄXINQYQAITYIÖLKOHGWÅJZRÄYFKZKQQJCTÄHBLGCTLJSJRCJIGIGXTDÅVQÅZÖSCÖTOHXBDYIBQVTÄHATFYAÄJDCQJÅGÖWZOAALVKXLGÅÄÖXITDJÅLEDCBVAYPVNTWAEMBHCUQORLGCWMBSDCBZTAQQTTWXSXLGRWPZWGTWIZTODÄGMGBASJTXQKLEAÄLWDIASDTASMDRVZMAAXUHBINWTKYFJÖPTOZMMLÖWCÖZCVYTOZBÅLEJQFEBVBÅLSÖWJHDGBNMABMRXDQKIHGBNÄJPAKDPUVRZÄJZÄASGRBPTAKUCHCBVWÅKILUEEIÄÄNZÖWMXYZÄWSBJVURZWTYFZZLIHMTOCJPVKCLVÄE"
