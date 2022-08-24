# @Author: Petri Jehkonen <petri>
# @Date:   2022-08-12T13:27:02+03:00
# @Email:  petri.jehkonen@xiphera.com
# @Last modified by:   petri
# @Last modified time: 2022-08-24T18:51:39+03:00
# @Copyright: Xiphera LTD.


# Author: Petri Jehkonen (at) xiphera.com

import random
import math
import string
import glob
import os
from random import choices
import numpy as np
from numpy import binary_repr
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pprint
from scipy.interpolate import interp1d
import warnings
from datetime import date
from datetime import datetime
from dateutil import relativedelta
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from PIL import Image


def alusta_t630():

    suuri_luku = b"S\xef8\x8e\xc8\xddff\xf4\x81\xc7 '2\x97\x88\x86\t3\x12\xfbTI5FQ\x05$P\xe85o\\a\xae\x80i=U\x16\t3\xc0i\xbd\xee\xcd\xc0\\\xf6\x13\x0f\xe8jK\x0e\xd9\xf8\xab\xbc\r!0d?\nv\xad\x06\x83\x01,\x83\xf9%\xa8n4\x12\xb3gU\x12\xda\xecw!\xf2O\xb5\r\x1e\xdd\xf0\xa2H5\xe9\xf2\x81\xd4B\x91\xf7r\xfaI!d\xf7\xfa\xafW\xce\xb2\x00x]\xb2[\xf5@:\x07\x9d\x9db\xca\xa8?Ue3G\xe1YVh\x80\x051g\x00\x07hQ\xc4\xf3K\x1b\x0f\\\x08\xfe\x19&6\xb2\x14\xcb\x90\xfd\xfdq+\xd6X\xa5\xc6Q\x84`U\x13\xee#Y\xb2\xdf8\x7fJ8l\x8bV\x89>\xe9\xc7\x83/\xdf\xf7(\x8b\xc0\xb3\xf8\xe11\x04\xcb\x99\x96[\xbdN\x8d\x8d-\xaa\x03\x90*m\xc3\xa1\x08\x91\x17\xd96^9#iX\xfc\xef \xdd\xd1\xcd\xff\xedY\x98\xbaA\xf2g\xbf\xb7q\xb4^\xa5\xc8\xd4\xcb\xd9\x0eZb\xf8"

    avain = suuri_luku[:16]

    return avain, ctr_enkoodaus, ctr_dekoodaus


def ctr_enkoodaus(avain, viesti):
    # Arvotaan kertakäyttönumero satunnaisuudesta
    # Eli alustetaan N satunnaisella 128-bittisellä luvulla
    N = os.urandom(16)

    # Tehdään enkoodaaja avaimesta ja laskurista
    enkryptaaja = Cipher(algorithms.AES(avain), modes.CTR(N),).encryptor()

    # Suoritetaan salaus
    salattu = enkryptaaja.update(viesti) + enkryptaaja.finalize()

    return (N, salattu)


def ctr_dekoodaus(avain, N, salateksti):
    # Tehdään dekoodaaja, avaimesta ja laskurista
    dekoodaaja = Cipher(algorithms.AES(avain), modes.CTR(N),).decryptor()

    return dekoodaaja.update(salateksti) + dekoodaaja.finalize()


def alusta_t620():
    avain, _, _, _, _, _ = alusta_t601()
    kuvatiedosto = './images/cake.png'
    return avain, kuvatiedosto, lue_kuva, salaa_ja_pura_cbc, yhdistele


# Lisätty lohkon_koko ja lohko_tavuina funktion kutsuun oletusarvoina.
def salaa_ja_pura_cbc(tavutieto, avain, IV=None, lohkon_koko=128, lohko_tavuina=16, purku=False):

    # Salatessa funktiolle ei anneta IV:tä eli ensimmäistä kertakäyttönumeroa.
    # Luodaan ensimmäinen kertakäyttönumero tietokoneen entropia-altaasta, joka on siis täysin satunnainen 16-tavuinen, eli 128-bittinen luku
    if IV is None:
        IV = os.urandom(lohko_tavuina)

    # Luodaan AES-CBC lohkosalain käyttäen 128-bittistä avainta.
    aes_ecb_salain = Cipher(algorithms.AES(avain), modes.CBC(IV))

    if purku:
        operaatio = aes_ecb_salain.decryptor()
    else:
        operaatio = aes_ecb_salain.encryptor()

    lohkoja = len(tavutieto)
    käsitellyt = []
    for i, lohko in enumerate(tavutieto):
        if i != lohkoja:
            käsitellyt.append(operaatio.update(lohko))
        else:
            käsitellyt.append(operaatio.update(lohko)+operaatio.finalize())

    if not purku:
        return IV, käsitellyt
    else:
        return käsitellyt


def alusta_t606():
    avain, _, _, _, _, _ = alusta_t601()

    return avain, lue_kuva, salaa_ja_pura, yhdistele


def lue_kuva(tiedosto, lohkon_koko=128, lohko_tavuina=16):
    kuva = np.asarray(Image.open(tiedosto))

    # Otetaan talteen kuvan alkuperäinen muoto
    muodot = kuva.shape

    # Litistetään kuva riviksi
    rivi_kuva = kuva.flatten()

    # Muunnetaan pikselit tavuiksi
    kuva_tavuina = rivi_kuva.tobytes()

    # Suoritetaan lohkominen
    kuva_lohkot = []
    for i in range(0, len(kuva_tavuina), lohko_tavuina):
        kuva_lohkot.append(kuva_tavuina[i:i+lohko_tavuina])

    return muodot, kuva_lohkot


def alusta_t605():

    avain, salatut_lohkot, _ = alusta_t604()
    puretut_lohkot = salaa_ja_pura(salatut_lohkot, avain, purku=True)

    return puretut_lohkot, yhdistele


def yhdistele(lohkot, merkistö=None):

    tavut = bytes()
    for lohko in lohkot:
        tavut += lohko

    # Jos on pyydetty merkkikoodauksen purkua, palautetaan dekoodattu tavukoodi.
    if merkistö is None:
        return tavut
    else:
        return tavut.decode(merkistö)


def alusta_t604(viesti="KAHVI"):

    avain, lohkot_tavuina, _ = alusta_t603()
    salatut_lohkot = salaa_ja_pura(lohkot_tavuina, avain)

    return avain, salatut_lohkot, salaa_ja_pura


def alusta_t603(viesti="KAHVI"):

    lohko_bitteinä = 128
    lohko_tavuina = lohko_bitteinä//8

    avain, _, _, _, _, _ = alusta_t601(viesti)

    tiedosto = './Tekstit/kakkuresepti.txt'
    lohkot_tavuina = lue_tiedosto_ja_esikäsittele(tiedosto, lohko_bitteinä, näytä_tiedosto=False)

    return avain, lohkot_tavuina, salaa_ja_pura


def alusta_t602(viesti="KAHVI"):
    return lue_tiedosto_ja_esikäsittele


# Funktio suorittaa tavutiedolle joko salauksen tai purun annetulla avaimella.
# Jos purku=False, niin funktio enkoodaa.
# Jos purku=True, niin funktio dekoodaa.


def salaa_ja_pura(tavutieto, avain, purku=False):
    # Luodaan AES-ECB lohkosalain käyttäen 128-bittistä avainta.
    aes_ecb_salain = Cipher(algorithms.AES(avain), modes.ECB())

    # luodaan joko enkryptaus tai dekryptaus
    if purku:
        operaatio = aes_ecb_salain.decryptor()
    else:
        operaatio = aes_ecb_salain.encryptor()

    # Katsotaan kuinka monta lohkoa pitää prosessoida.
    lohkoja = len(tavutieto)

    # Tehdään tila käsitellylle datalle.
    käsitellyt = []

    for i, lohko in enumerate(tavutieto):
        if i != lohkoja:
            käsitellyt.append(operaatio.update(lohko))
        else:
            käsitellyt.append(operaatio.update(lohko)+operaatio.finalize())

    return käsitellyt


# Funktio palauttaa tavu-muodosa luetun tiedoston.
def lue_binääri_tiedosto(tiedostonnimi):
    with open(tiedostonnimi, 'rb') as file:
        sisältö_tavuina = file.read()

    return sisältö_tavuina


# Funktio lukee tiedoston, jakaa sen lohkoiksi
# Ja päddää viimeiseen lohkon sisältämään 128-bittiä.
# Jos näytä_tiedosto parametri on True, näytetään tiedoston sisältö
# Oletus nyt on että lohkon koko on 128-bittiä
def lue_tiedosto_ja_esikäsittele(tiedostonnimi, lohkon_koko=128, näytä_tiedosto=False):

    # Jos haluamme näyttää tekstitiedoston sisällön
    if näytä_tiedosto:
        with open(tiedostonnimi, 'r', encoding='UTF-8') as file:
            tekstiä = file.readlines()

        print("".join(tekstiä))

    # Luetaan tavuina tiedosto sisään
    tavu_data = lue_binääri_tiedosto(tiedostonnimi)

    # Määritellään lohkon koko tavuina
    lohko_tavuina = lohkon_koko//8

    # Tehdään paikka lohkoille
    lohkot = []

    # Suoritetaan lohkominen
    for i in range(0, len(tavu_data), lohko_tavuina):
        lohkot.append(tavu_data[i:i+lohko_tavuina])

    # Suoritetaan päddäys viimeiselle lohkolle
    päddää = padding.PKCS7(lohkon_koko).padder()
    lohkot[-1] = päddää.update(lohkot[-1])+päddää.finalize()

    # Palautetaan tavumuodossa olevat lohkot, joista viimeinen on lavennettu 128-bittiseksi
    return lohkot


def alusta_t601(viesti="KAHVI"):

    # Asetetaan päddäykselle koko, joka vastaa AES lohkon kokoa eli 128-bittiä.
    lohko_bitteinä = 128
    lohko_tavuina = lohko_bitteinä//8

    # Luodaan päddäyksen tuottaja sekä päddäyksen poistaja
    täydennä_päddäys = padding.PKCS7(lohko_bitteinä).padder()
    poista_päddäys = padding.PKCS7(lohko_bitteinä).unpadder()

    luku_2048_bittiä = b"S\xef8\x8e\xc8\xddff\xf4\x81\xc7 '2\x97\x88\x86\t3\x12\xfbTI5FQ\x05$P\xe85o\\a\xae\x80i=U\x16\t3\xc0i\xbd\xee\xcd\xc0\\\xf6\x13\x0f\xe8jK\x0e\xd9\xf8\xab\xbc\r!0d?\nv\xad\x06\x83\x01,\x83\xf9%\xa8n4\x12\xb3gU\x12\xda\xecw!\xf2O\xb5\r\x1e\xdd\xf0\xa2H5\xe9\xf2\x81\xd4B\x91\xf7r\xfaI!d\xf7\xfa\xafW\xce\xb2\x00x]\xb2[\xf5@:\x07\x9d\x9db\xca\xa8?Ue3G\xe1YVh\x80\x051g\x00\x07hQ\xc4\xf3K\x1b\x0f\\\x08\xfe\x19&6\xb2\x14\xcb\x90\xfd\xfdq+\xd6X\xa5\xc6Q\x84`U\x13\xee#Y\xb2\xdf8\x7fJ8l\x8bV\x89>\xe9\xc7\x83/\xdf\xf7(\x8b\xc0\xb3\xf8\xe11\x04\xcb\x99\x96[\xbdN\x8d\x8d-\xaa\x03\x90*m\xc3\xa1\x08\x91\x17\xd96^9#iX\xfc\xef \xdd\xd1\xcd\xff\xedY\x98\xbaA\xf2g\xbf\xb7q\xb4^\xa5\xc8\xd4\xcb\xd9\x0eZb\xf8"

    avain = luku_2048_bittiä[:16]

    viesti_tavuina = bytes(viesti, 'UTF-8')

    pädätty_viesti = täydennä_päddäys.update(viesti_tavuina)+täydennä_päddäys.finalize()

    # Luodaan AES-ECB lohkosalain käyttäen 128-bittistä avainta.
    aes_ecb_salain = Cipher(algorithms.AES(avain), modes.ECB())

    # Luodaan enkryptaus, eli salaava toiminne
    enkryptaus = aes_ecb_salain.encryptor()

    # Luodaan enkryptaus, eli salaava toiminne
    dekryptaus = aes_ecb_salain.decryptor()

    kahvi_salakielellä = enkryptaus.update(pädätty_viesti) + enkryptaus.finalize()

    purettu_salakieli = dekryptaus.update(kahvi_salakielellä)+dekryptaus.finalize()

    # Luodaan AES-ECB lohkosalain käyttäen 128-bittistä avainta.
    AE = Cipher(algorithms.AES(avain), modes.ECB())

    # Luodaan enkryptaus, eli salaava toiminne
    e = AE.encryptor()

    # Luodaan enkryptaus, eli salaava toiminne
    d = AE.decryptor()

    return avain, pädätty_viesti, e, kahvi_salakielellä, d, purettu_salakieli


def alusta_t549():

    return merkit_heksamerkeiksi, yleinen_lohkosalain, päddäyksen_poisto


def merkit_heksamerkeiksi(avain, pituus=8):
    assert len(avain) == pituus, "merkkijonossa pitää olla kahdeksan merkkiä"

    heksa_avain = "0x"
    for byte in bytes(avain, encoding='latin-1'):
        heksa_avain += str(hex(byte))[2:].upper()

    return heksa_avain


def alusta_t548():
    viesti, _ = alusta_t546()
    pädätty_viesti, k2, _ = alusta_t547()
    salattu_yleisellä_lohkosalaimella = yleinen_lohkosalain(pädätty_viesti, k2)

    return viesti, salattu_yleisellä_lohkosalaimella, k2, yleinen_lohkosalain, päddäyksen_poisto


def alusta_t547():
    viesti, _ = alusta_t546()
    pädätty_viesti = päddäys(viesti)
    k2 = 0xA1B2C3D4E5F60718
    return pädätty_viesti, k2, yleinen_lohkosalain


def alusta_t546():
    v1 = "Kahvi Charlotassa on hyvää ja vahvaa!"

    return v1, päddäys


# Tätä funktiota käytetään kun selvätekstiin lisätään merkkejä lohkon täyttämiseksi.
def päddäys(merkkijono, lohkon_koko=64, merkistö='latin-1'):
    """ Päddäys-funktio, lisää merkkijonon loppuun heksoja 0x00, 0x01, ... kunnes lohkon koko bitteinä täyttyy
    Parametrit:
        merkkijono (string): Merkkijono johon lisätään päddäys, oletus "latin-1"-merkistökoodaus
        lohkon_koko (int): Lohkon koko bitteinä, oletus 64-bittiä.

    Palauttaa:
        string: Merkkijono, jonka bittimäärä on jaollinen lohkon koon bittimäärällä.
    """
    mj_pituus_bits = len(merkkijono.encode(merkistö))*8
    return merkkijono + "".join([chr(laskuri) for laskuri in range(int((lohkon_koko - (mj_pituus_bits) % lohkon_koko)/8))])


# Tätä funktiota käytetään poistamaan päddäys decryptatusta merkkijonosta.
def päddäyksen_poisto(merkkijono, pad_alku='\x00'):
    """ Päddäyksen poisto -funktio, palauttaa merkkijonon ilman päddäystä
    Parametrit:
        merkkijono (string): Merkkijono johon lisätään päddäys, oletus "latin-1"-merkistökoodaus
        pad_alku (chr): Tunniste mikä määrittää milloin päddäys alkaa.

    Palauttaa:
        string: Merkkijono, jossa ei ole enää päddäystä.
    """

    return merkkijono[:merkkijono.find(pad_alku)]


# Lohkosalain olettaa että se saa tavujonon, jonka koko on jaollinen lohkon koolla.
def yleinen_lohkosalain(tavujono, avain, lohkon_koko=64, merkistö='latin-1', näytälohkot=False):

    assert (len(tavujono)*8) % lohkon_koko == 0, "Päddäys unohtunut"

    # Tarvittaessa muutetaan merkkijono tavujonoksi 'latin-1' merkistökoodauksella
    if type(tavujono) is str:
        bytejono = tavujono.encode(merkistö)

    # Jos avain on merkkijono (heksadesimaaleja), muunnetaan avain luvuksi
    if type(avain) is str:
        avain = int(avain, 16)

    # Paikka enkoodatulle viestille
    XOR_tulos_merkkijonona = ""

    # Lohkotaan bytejono siten että jokainen tavu muodostaa oman lohkon

    for lohkon_numero in range((len(bytejono)*8)//lohkon_koko):
        # Otetaan yksi lohko ja tehdään siitä 64-bittinen luku
        lohko = bytejono[(lohkon_numero*8):((lohkon_numero+1))*(lohkon_koko//8)]
        # Ja tehdään lohkosta yksi 64-bittinen luku
        lohko_int = int.from_bytes(lohko, "big")

        # Lasketaan siitä XOR avaimen kanssa.
        lohkon_xor = lohko_int ^ avain

        # Muunnetaan tulos tavujonoksi
        lohkon_xor_bytes = lohkon_xor.to_bytes(8, 'big')

        # Tallenetaan XOR tulos listaan.
        XOR_tulos_merkkijonona += "".join([chr(tavu) for tavu in lohkon_xor_bytes])

        if näytälohkot:
            print("Lohkon numero   :", lohkon_numero)
            print("Lohkon sisältö  :", lohko)
            print("Lohkon xor      :", lohkon_xor)
            print("Lohkon xor Bytes:", lohkon_xor_bytes)
            print("Merkkijono nyt  :", XOR_tulos_merkkijonona)

    return XOR_tulos_merkkijonona


def alusta_t545():
    # Luodaan kolme viestiä
    v1 = "Kahvi Charlotassa on hyvää ja vahvaa!"
    v2 = "Kaivi Charlotassa on hyvää ja vahvaa!"
    v3 = "Kqhvi Charlotassa on hyvää ja vahvaa!"

    # Luodaan kaksi avainta, joiden viimeinen bitti eroaa.
    ka = 0b01011010
    kb = 0b01011011

    # Luodaan kaksi salakirjoitusta
    sk1 = yksinkertainen_lohkosalain(merkkijono=v1, avain=ka)
    sk2 = yksinkertainen_lohkosalain(merkkijono=v1, avain=kb)
    sk3 = yksinkertainen_lohkosalain(merkkijono=v2, avain=ka)
    sk4 = yksinkertainen_lohkosalain(merkkijono=v3, avain=ka)

    return v1, v2, v3, ka, kb, sk1, sk2, sk3, sk4


def alusta_t542():

    viesti = "Kahvi Charlotassa on hyvää ja vahvaa!"
    k1 = 0x6A
    k2 = "0xA1B2C3D4E5F60718"

    return viesti, yksinkertainen_lohkosalain, k1, k2


def alusta_t432():
    # Varuiksi luodaan aiemmin tehdyt muuttujat
    teksti = lue_tiedosto_merkkijonoksi(4)
    laatija = "Mats Löfström suomi"
    return teksti, laatija


def alusta_t421():
    # Luo Bobin viestin Alicelle
    salakirjoitus = "PFQÄFÄFDCLCSSTGSEFJQJJLNSJCSNSTDMMEQHSHHMVXTESHSDCSSPSTDQHHSHLEPSHSHHMÅSVXTNSEPSDCQQJSVCMQDQDSSRLDDSSTDLJJSQDLTPQTXLVRFCCSQDQTLCCXÅMVJSÖQRLCXXTHFJPLTNQQHFTÖXXDCXJSMSTCSQSSPMTSPQCXPQLJCXDQTXFJLCCLENLQDQTSJQGL"
    return salakirjoitus


# Yksinkertainen lohkosalain
def yksinkertainen_lohkosalain(merkkijono, avain, näytälohkot=False):
    """Yksinkertainen lohkosalain demo-funktio
       Parametrit:
       merkkijono (string): Lohkosalaimella enkoodattava tai dekoodattava tieto, oletus "latin-1" koodattu
       avain (int): Symmetrinen avain, jota käytetään enkoodauksessa ja dekoodauksessa
       näytälohkot (bool): Lippu, jolla määritetään näytetäänkö lohkosalauksen välivaiheet.

       Palauttaa:
          string: Enkoodattu tai dekoodattu merkkijono.
    """
    # Salaimissa on useita tarkistuksia suojattavan tiedon tyypeille sekä annettujen parametrien hyvyyksille.
    # Nämä tarkistukset ja algoritmin sisäiset tyyppimuunnokset ovat salaimen käyttäjälle näkymättömiä.

    # Seuraavassa muutetaan merkkijonon ASCII merkit tavuiksi, olettaen että merkkijono on 'latin-1' merkistö-koodattua.
    # Tämä muunnos ei välttämättä toimi muilla merkki-koodauksilla.
    tavutettu_merkkijono = bytes(merkkijono, encoding="latin_1")

    # Luodaan paikka enkoodauksen tai dekoodauksen tulokselle
    XOR_tulos = []

    # Pilkotaan merkkijono lohkoiksi. Jokainen tavu (eli merkki) muodostaa oman lohkon.
    for lohko in tavutettu_merkkijono:
        # Suoritetaan salaimen matemaattinen operaatio (XOR) tavuittain avaimen kanssa.
        XOR_tulos.append(avain ^ lohko)

        # Jos haluat nähdä miten lohko käsitellään aseta funktiokutsuun näytälohkot=True
        if näytälohkot:
            print("Lohko on {}, avain {} ja XOR {}".format(
                chr(lohko), hex(avain), binary_repr(avain ^ lohko, 8)))

        # Muunnetaan salaimen tulos merkkijonoksi, yleensä haluamme käsitellä vain bittejä ja tavuja.
        # Tässä esimerkissä käsittelemme kirjain-merkkejä, joten demonstraation vuoksi muunnamme salaimen tuottaman datan merkkijonoksi.
        XOR_merkkijonona = "".join([chr(lohko) for lohko in XOR_tulos])

    # Palautetaan merkkijonona.
    return XOR_merkkijonona


def laske_tiiviste(teksti, tekstipalaute=True, debug=False):

    # Testataan että annettu teksti on todellakin tekstimuotoinen
    assert isinstance(teksti, str), "Anna tiivistefunktiolle merkkijono!"

    # Muunnetaan merkkijono tavujonoksi:
    tavuviesti = teksti.encode()

    # Otetaan käyttöön SHA256 tiivistefunktio-olio, tästä puhumme seuraavissa kappaleissa
    sha256tiivistefunktio = hashlib.sha256()

    # Lasketaan tiiviste
    sha256tiivistefunktio.update(tavuviesti)

    # Muunnetaan tiiviste etumerkittömäksi 256 bittiseksi kokonaisluvuksi
    oikea_tiiviste_tavuina = sha256tiivistefunktio.digest()
    oikea_tiiviste_lukuna = int.from_bytes(oikea_tiiviste_tavuina, byteorder='big')

    if debug:
        # Näytetään teksti ja tiiviste heksana
        print("Teksti oli               :", teksti)
        print("Laskettu tiiviste heksana:", sha256tiivistefunktio.hexdigest())

    # Palautetaan tiiviste joko heka-stringinä tai sitten bytenä
    if tekstipalaute:
        return sha256tiivistefunktio.hexdigest()
    else:
        return sha256tiivistefunktio.digest()


def b_laske_tiiviste(teksti, tekstipalaute=False, debug=False):
    return laske_tiiviste(teksti, tekstipalaute, debug)


def testaa_tiivisteet(eka_tiiviste, toka_tiiviste, debug=False):

    # Testataan että funktiolle annetut argumentit ovat oikeaa tieto typpiä
    assert isinstance(eka_tiiviste, bytes), "Ensimmäiseksi annettu tiiviste pitää olla tavumuodossa"
    assert isinstance(toka_tiiviste, bytes), "Toiseksi annettu tiiviste pitää olla tavumuodossa"

    # Testataan että tiivisteet ovat yhtä pitkiä
    assert len(eka_tiiviste) == len(
        toka_tiiviste), "Tiivisteet ovat erimittaisia, näitä ei voi testata"

    # Muunnetaan tavumuotoinen tiiviste etumerkittömäksi 256 bittiseksi kokonaisluvuksi
    eka_lukuna = int.from_bytes(eka_tiiviste, byteorder='big')
    toka_lukuna = int.from_bytes(toka_tiiviste, byteorder='big')

    # Lasketaan XOR, "ero"-luvussa jokainen '1'-bitti tarkoittaa että alkuperäisten tiivisteiden bitit olivat eri
    ero = eka_lukuna ^ toka_lukuna

    # Lasketaan ykkösbittien määrä
    tiiviste_bittien_ero = bin(ero).count('1')

    if debug:
        # Näytetään tiivisteiden ero
        print("Eroa tiivisteiden välillä on " + str(tiiviste_bittien_ero) + " bittiä")

    # Palautetaan tiivisteiden ero vielä numerona
    return tiiviste_bittien_ero


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
            print("Bitit   {}".format(binary_repr(tavu, 8)))
            print("Avain   {}".format(binary_repr(avain, 8)))
            print("XOR     {}".format(binary_repr(avain ^ tavu, 8)))
            print("Sala    {}".format(chr(avain ^ tavu)))
        c_enkoodattu.append(avain ^ tavu)

    if debugging:
        print("Viesti joka enkoodataan on:")
        print(viesti+"\n")

        print("Avain jota käytämme salauksessa on:", hex(k), "\n")

        print("Tavuittain enkoodattu viesti näyttää seuraavalta:")
        for tavu in c_enkoodattu:
            print(chr(tavu), end='')
    return c_enkoodattu


def vertaa_maailmankaikkeuden_ikään(avaimiin_kuluva_aika_a):
    # Verrataan maailmankaikkeuden arveltuun ikään.
    maailmankaikkeudenikä_vuosina = 13787000000
    print("Maailmankaikkeuden ikä vuosina: {} vuotta.".format(maailmankaikkeudenikä_vuosina))

    kertaa_maailmankaikkeuden_ikä = avaimiin_kuluva_aika_a/maailmankaikkeudenikä_vuosina
    print(
        "Avainten laskenta vaatii {:.3e} -kertaa maailmankaikkeuden iän.".format(kertaa_maailmankaikkeuden_ikä))

    erotus = avaimiin_kuluva_aika_a - maailmankaikkeudenikä_vuosina

    if erotus < 0:
        print("Tämä olisi keretty laskemaan maailmankaikkeuden arvioidussa elinajassa")
    else:
        if erotus > 20000:
            print("Ihmisellä ei ole ollut mitään toivoa laskea tätä avainta")
        else:
            print("Ihmiskunta olisi kerennyt jääkauden jälkeen laskemaan avaimen")


def avaimen_laskemiseen_kuluva_aika(bittejä=None, avainta_sekunnissa=None, debugging=False):
    # Tuotetaan avainten määrä, voit vaihtaa bittimäärää.
    if bittejä is None:
        bittejä = 128

    if avainta_sekunnissa is None:
        avainta_sekunnissa = 10**12

    avainten_lukumäärä = 2**bittejä
    avaimiin_kuluva_aika_s = avainten_lukumäärä/avainta_sekunnissa  # sekunteina
    avaimiin_kuluva_aika_a = avaimiin_kuluva_aika_s/(60*60*24*365)  # vuosina
    print("{}-bittisen avaimen laskemiseen nopeudella {:.2e} avainta sekunnissa,".format(bittejä, avainta_sekunnissa))
    print("kuluu {:.3e} vuotta".format(avaimiin_kuluva_aika_a))
    return avaimiin_kuluva_aika_a


def nist112bits_diff(debugging=False):
    nist_112bits = date.fromisoformat('2015-01-01')
    tänään = date.today()
    ero_kuukausia = (tänään.year-nist_112bits.year)*12 + tänään.month-nist_112bits.month
    if debugging:
        print("Ero kuukausina:", ero_kuukausia)

    mooren_laki_kk = 18
    bittiä_lisää = ero_kuukausia//mooren_laki_kk
    if debugging:
        print("Tarvitaan {} bittiä lisää.".format(bittiä_lisää))
    return bittiä_lisää


def näytäkorrelaatiot(data, siirrokset=40, otsikko="Ei otsikkoa"):
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    sm.graphics.tsa.plot_acf(data, lags=siirrokset, ax=ax[0])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sm.graphics.tsa.plot_pacf(data, lags=siirrokset, zero=True, ax=ax[1])
    plt.suptitle("{}".format(otsikko))
    plt.show()


def tuotajakaumia(n=10000):
    x = np.arange(n)
    y1 = np.arange(n)
    nolla_ysi = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y2 = np.repeat(nolla_ysi, int(n/len(nolla_ysi)))
    y3 = np.random.normal(int(n/2), int(n/7), n).astype(int)
    y4 = np.random.randint(0, n, n)

    return y1, y2, y3, y4


def heittelyt(noppa=None, kolikko=None, n=4000000, siemen=20211221, n_bins=3):

    if (noppa is None and kolikko is None) or (noppa and kolikko):
        print("Anna joko noppa=True tai kolikko=True")
        return "En ymmärrä"

    if kolikko:
        max_luku = 2
        x_paikat = np.array([0.2, 0.8])
        x_labelit = ['Kruuna', 'Klaava']
        label = "Kolikon"
    else:
        max_luku = 6
        # x_paikat = np.arange(0, max_luku)
        x_paikat = np.array([0.22, 1.15, 2.05, 2.98, 3.85, 4.8])
        x_labelit = ['1', '2', '3', '4', '5', '6']
        n_bins = 11
        label = "Nopan"
    # Asetetaan siemen
    np.random.seed(siemen)

    # Luodaan neljä otosta
    y1 = np.random.randint(0, max_luku, n)
    y2 = np.random.randint(0, max_luku, n)
    y3 = np.random.randint(0, max_luku, n)
    y4 = np.random.randint(0, max_luku, n)

    fig, axes = plt.subplots(2, 2, figsize=(9, 9), sharex=False, sharey=False)
    fig.suptitle('{} heittokertojen vertailu histogrammeilla n ={}'.format(label, n))
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
    n = 10000

    y1, y2, y3, y4 = tuotajakaumia()

    fig, axes = plt.subplots(2, 2, figsize=(12, 6), sharex=False, sharey=False)
    fig.suptitle('Jakaumien vertailu histogrammeilla n ={} | bins={}'.format(n, n_bins))
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
        if substituutio.get(kirjain) == None:
            muunnos.append(' ')
        else:
            muunnos.append(substituutio.get(kirjain))
    return "".join(muunnos)


def atbash_substituutio():
    kirjaimet = string.ascii_uppercase + 'ÅÄÖ'
    substituutio = dict(zip(kirjaimet, kirjaimet[::-1]))
    return substituutio


def salain_b(viesti, avain):
    isot, pienet = merkistot(suomi=True)
    return caesar(viesti, aakkosto=isot, avain=avain)


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
    esikäsitelty_teksti = esikasittele_teksti(esikäsitelty_teksti, aakkosto+pienet)

    if debuggaus:
        print("Muunnettava viesti", esikäsitelty_teksti)

    # Lista johon laitetaan muunnoksen tulos
    muunnettu_teksti = []
    # Muunnos suoritetaan merkki merkiltä
    for kirjain in esikäsitelty_teksti:
        # Aakkoston oletetaan olevan järjestetty ja sisältää vain isot kirjaimet
        # Käsiteltävän kirjaimen suhteellinen paikka aakkostossa
        ennen_muunnosta = aakkosto.index(kirjain)-aakkosto.index(aakkosto[0])
        # Tässä suoritetaan muunnoksen indeksi laskenta
        if not purku:
            muunnoksen_jälkeen = (ennen_muunnosta+avain) % len(aakkosto)
        else:
            muunnoksen_jälkeen = (ennen_muunnosta-avain) % len(aakkosto)

        # Lisätään muunnokseen
        muunnettu_teksti.append(aakkosto[muunnoksen_jälkeen])
        if debuggaus:
            print("Merkki: " + kirjain + " on muunnettuna : ", aakkosto[muunnoksen_jälkeen])
            print("Aakkoston indeksi ennen muunnosta    : ", ennen_muunnosta)
            print("Aakkoston indeksi muunnoksen jälkeen : ", muunnoksen_jälkeen)

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

    pienet = ""
    if aakkosto is None:
        aakkosto, pienet = merkistot(suomi=True)

    alkuviesti = esikasittele_teksti(viesti, aakkosto+pienet)

    muunnettu_viesti = []

    # Generate ascii index of the first alphabet and offset list
    siirroslista = laske_siirros(aakkosto, avain, purku, debuggaus)

    if debuggaus:
        print("Saatu viesti  : ", viesti)
        print("Alkuviesti    : ", alkuviesti)

    for i, kirjain in enumerate(alkuviesti):
        ennen_muunnosta = aakkosto.index(kirjain)
        siirros_indeksi = (ennen_muunnosta+(siirroslista[i % len(siirroslista)])) % len(aakkosto)
        muunnettu_viesti.append(aakkosto[siirros_indeksi])
        if debuggaus:
            print("Viestin merkki : {}".format(i))
            print("Ennen muunnosta: ", ennen_muunnosta)
            print("Siirros indeksi: ", siirros_indeksi)
            print("Kirjain: " + kirjain + " muunnetaan: ", aakkosto[siirros_indeksi])

    return "".join(muunnettu_viesti)


def merkistot(suomi=False):
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


def näytä_kirjainjakauma(kirjaimet=None, osuus=None, nimi=None, vain_aineisto=False, savefile=False):
    s_kirjaimet = ('A', 'I', 'T', 'N', 'E', 'S', 'L', 'O', 'K', 'U', 'Ä', 'M', 'V',
                   'R', 'J', 'H', 'Y', 'P', 'D', 'Ö', 'G', 'B', 'F', 'C', 'W', 'Å', 'Q', 'X', 'Z')
    s_osuus = [11.9, 10.64, 9.77, 8.67, 8.21, 7.85, 5.68, 5.34, 5.24, 5.06, 4.59, 3.30, 2.52,
               2.32, 1.91, 1.83, 1.79, 1.74, 0.85, 0.49, 0.13, 0.06, 0.06, 0.04, 0.01, 0.0, 0.0, 0.0, 0.0]

    x = np.arange(len(s_kirjaimet))

    fig, ax = plt.subplots(figsize=(16, 6))

    if kirjaimet is None:
        läpinäkyvyys = 0.9
        leveys = 0.8
    else:
        läpinäkyvyys = 0.4
        leveys = 0.5

        järjestetty_lista = []
        for i, kirjain in enumerate(s_kirjaimet):
            järjestetty_lista.append(osuus[kirjaimet.index(kirjain)])

    if not vain_aineisto:
        plt.bar(x, s_osuus, width=leveys, ls='dotted', lw=3, fc=(
            0, 0, 1, läpinäkyvyys), label="Suomen kielen kirjainjakauma")

    if kirjaimet is not None:
        if vain_aineisto:
            plt.bar(x, osuus, ls='dashed', lw=5, fc=(1, 0, 0, 0.6), label="Aineisto "+nimi)
        else:
            plt.bar(x, järjestetty_lista, ls='dashed', lw=5,
                    fc=(1, 0, 0, 0.6), label="Aineisto "+nimi)

    if vain_aineisto:
        plt.xticks(x, kirjaimet)
    else:
        plt.xticks(x, s_kirjaimet)

    plt.ylabel("Esiintymistiheys", fontsize=18)
    plt.xlabel("Kirjain", fontsize=18)
    plt.legend()

    if not vain_aineisto:
        for i, v in enumerate(s_osuus):
            ax.text(i-0.5, v + 0.1, str(v), color='blue', alpha=läpinäkyvyys, fontweight='bold')

    if kirjaimet is not None:
        if vain_aineisto:
            for i, v in enumerate(osuus):
                ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')
        else:
            for i, v in enumerate(järjestetty_lista):
                ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    if nimi is None:
        plt.title("Suomen kielen kirjainjakauma", fontsize=20)
    else:
        plt.title("Aineisto: {}".format(nimi), fontsize=20)

    if savefile:
        plt.savefig("suomen_kirjainjakauma.png", dpi=150)
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
        kirjainesiintymät[kirjain] = 0
    for kirjain in teksti:
        kirjainesiintymät[kirjain] += 1
    return kirjainesiintymät


def frekvenssi_prosenteiksi(frekvenssi_sanakirja, teksti):
    sanakirja = {}
    for key in frekvenssi_sanakirja.keys():
        sanakirja[key] = np.round(100*frekvenssi_sanakirja[key]/len(teksti), decimals=2)
    return sanakirja


def laske_frekvenssit(teksti):
    kirjainesiintymät = tuota_frekvenssit(teksti)
    esiintymisjärjestys = sorted(kirjainesiintymät.items(), key=lambda x: x[1], reverse=True)
    kirjaimet = []
    frekvenssit = []
    for pari in esiintymisjärjestys:
        kirjaimet.append(pari[0])
        frekvenssit.append(pari[1])

    prosentit = np.round(100*np.array(frekvenssit)/len(teksti), decimals=2)

    return kirjaimet, prosentit


def laske_frekvenssi_ero_suomeen(sanakirja, verbose=False):
    suomen_jakauma = suomi()
    rms = 0
    for key in suomen_jakauma:
        ero = suomen_jakauma[key]-sanakirja[key]
        rms += np.square(ero)
        if verbose:
            print("Ero suomen kieleen kirjaimella {} on {:5} prosenttia".format(
                key, np.round(ero, decimals=2)))

    return np.round(rms, decimals=2)


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
    print("Alkuperäiset indeksit:\n{}\n{}".format(list(viesti), indeksit))
    print("Satunnainen permutaatio:\n{}\n{}".format(salateksti, permutoidut_indeksit))
    print("Salakieli edellisellä permutaatiolla: {}".format("".join(salateksti)))


def onetimepad(viesti="KAHVICHARLOTASSAONHYVÄÄJAVAHVAA"):
    aakkoset = string.ascii_uppercase + 'ÅÄÖ'
    viestissä_merkkejä = len(viesti)
    satunnaisotos = choices(aakkoset, k=len(viesti))
    return "".join(satunnaisotos), vigenere(viesti, aakkosto=aakkoset, avain="".join(satunnaisotos), purku=False, debuggaus=False)


def testaa_hyökkäysmallien_osaaminen(viesti, avain):
    if salain_c(viesti, avain) == 'ÄZLRÖYFMVO':
        print("Hienoa, voit edetä harjoituksiin!")
    else:
        print("Ei aivan, yritä uudestaan! Voit kysyä apuja kavereilta, jos tämä tuntuu hankalalta.")


def generoi_caesar_haaste(debuggaus=False, purku=False):
    viesti = 'Ensilumi suli, takatalvi tuli!'
    isot, pienet = merkistot(suomi=True)
    esikäsitelty_viesti = esikasittele_teksti(viesti, isot+pienet)

    if debuggaus:
        print("Alkuperäinen viesti  :", viesti)
        print("Esikäsitelty viesti  :", esikäsitelty_viesti)

    # Suoritetaan Caesar salaus edellisillä arvoilla
    salateksti = caesar(esikäsitelty_viesti, aakkosto=isot, avain=11, purku=False)
    if debuggaus:
        print("Caesar salateksti on :", salateksti)

    # Suoritetaan salauksen purku asettamalla purku-lippu arvoon True
    dekoodattu_teksti = caesar(salateksti, aakkosto=isot, avain=11, purku=True)
    if debuggaus:
        print("Caesar dekoodattu on :", dekoodattu_teksti)

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

    print("Kirjainjonon pituus on {} merkkiä".format(len(kirjainjono)))
    print("Ja siinä esiintyy yhteensä {} eri aakkosta.".format(len(kirjainjonon_merkit)))
    if aakkoston_koko - len(kirjainjonon_merkit) != 0:
        print("Kirjainjonon puuttuvat kirjaimet ovat {}".format(
            ''.join(set(isot).difference(kirjainjonon_merkit))))
    # print("Kirjainjono näyttää tältä:" +kirjainjono)

    # Lasketaan
    frekvenssi_kirjaimet, frekvenssi_prosentit = laske_frekvenssit(kirjainjono)
    näytä_kirjainjakauma(tuple(frekvenssi_kirjaimet), frekvenssi_prosentit, nimi)

    määrät = tuota_frekvenssit(kirjainjono)
    prosentit = frekvenssi_prosenteiksi(määrät, kirjainjono)
    poikkeaa_suomen_kielestä = laske_frekvenssi_ero_suomeen(prosentit)
    print("{} kirjoitus poikkeaa {} määrän suomen kielestä".format(nimi, poikkeaa_suomen_kielestä))


def näytä_tekstit():
    tekstitiedostot = harjoituksen_tiedostot()
    print("Saatavilla olevat tiedostot")
    for i, nimi in enumerate(sorted(tekstitiedostot)):
        print("Tiedostoindeksi: {} on {}".format(i, nimi[8:-3]))


def lue_bin_tiedosto(indeksi=None):
    if indeksi is None:
        print("Et antanut indeksiä.\n")
        harjoituksen_tiedostot('bin')
        bin_viesti = ""
    else:
        binääritiedostot = harjoituksen_tiedostot()
        tiedosto = indeksi
        with open(binääritiedostot[tiedosto], "r", encoding="utf_8") as file:
            bin_viesti = "".join(file.readlines())

    return bin_viesti


def lue_tiedosto_merkkijonoksi(indeksi=None, debuggaus=False):
    if indeksi is None:
        print("Et antanut indeksiä.\n")
        näytä_tekstit()
        alkuperäinen_viesti = ""
    else:
        tiedosto = indeksi
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
    näytä_kirjainjakauma(tuple(frekvenssi_kirjaimet), frekvenssi_prosentit, otsikko)


def vertaa_selväkieli_salakieli(selväteksti, salateksti="", otsikko=None, kurvi=False, debuggaus=False):

    salateksti_puuttuu = len(salateksti) == 0
    if salateksti_puuttuu:
        print("väärä funktio, tarvitsen selvätekstin ja salatekstin")
    aakkoset, _ = merkistot(suomi=True)
    leveys = 0.8

    selvä_pros = list(frekvenssi_prosenteiksi(tuota_frekvenssit(selväteksti), selväteksti).values())

    if not salateksti_puuttuu:
        sala_pros = list(frekvenssi_prosenteiksi(
            tuota_frekvenssit(salateksti), salateksti).values())
        leveys = 0.8

    if debuggaus:
        print("selväteksti:", selväteksti)
        print("salateksti :", salateksti)
        print("selväpros  :", selvä_pros)
        print("salapros   :", sala_pros)

    x = np.arange(len(aakkoset))

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(16, 12), edgecolor="black", linewidth=4)

    x_siirros = 0

    axes[0].bar(x-x_siirros, selvä_pros, width=leveys, ls='dotted',
                lw=3, fc=(0, 0, 1, 0.5), label="Selväteksti")
    axes[1].bar(x+x_siirros, sala_pros,  width=leveys, ls='dotted',
                lw=3, fc=(1, 0, 0, 0.5), label="Salateksti")

    if False:
        for i, v in enumerate(selvä_pros):
            axes[0].text(i-0.5, v + 0.1, str(v), color='blue', alpha=0.7, fontweight='bold')

        if not salateksti_puuttuu:
            for i, v in enumerate(sala_pros):
                axes[1].text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    x_labels = list(aakkoset)
    axes[0].set_xticks(x, minor=False)
    axes[1].set_xticks(x, minor=False)
    axes[0].set_xticklabels(x_labels, fontdict=None, minor=False)
    axes[1].set_xticklabels(x_labels, fontdict=None, minor=False)

    axes[0].title.set_text('Selväteksti')
    axes[1].title.set_text('Salateksti')

    axes[0].set_ylabel('Esiintymistiheys', fontsize=16)
    axes[1].set_ylabel('Esiintymistiheys', fontsize=16)

    # axes[0].set_xlabel("Kirjain",fontsize=18)
    axes[1].set_xlabel("Kirjain", fontsize=18)

    axes[0].legend()
    axes[1].legend()

    if otsikko is None:
        otsikko = "Tuntematon aineisto"

    fig.suptitle("Aineisto: {}".format(otsikko), fontsize=20)

    if kurvi:
        f1 = interp1d(x, np.array(selvä_pros), kind='cubic')
        f2 = interp1d(x, np.array(sala_pros), kind='cubic')

        xnew = np.linspace(x.min(), x.max(), num=601, endpoint=True)
        plt.plot(xnew, f1(xnew), '-', xnew, f2(xnew), '--')
        plt.legend(['Selvä', 'Sala'], loc='best')

    plt.show()


def tekstin_frekvenssi_aakkosjärjestyksessä(selväteksti, salateksti="", otsikko=None, kurvi=False, tiedostoon=False, debuggaus=False):

    salateksti_puuttuu = len(salateksti) == 0
    aakkoset, _ = merkistot(suomi=True)
    leveys = 0.8

    selvä_pros = list(frekvenssi_prosenteiksi(tuota_frekvenssit(selväteksti), selväteksti).values())

    if not salateksti_puuttuu:
        sala_pros = list(frekvenssi_prosenteiksi(
            tuota_frekvenssit(salateksti), salateksti).values())
        leveys = 0.4

    if debuggaus:
        print("selväteksti:", selväteksti)
        print("salateksti :", salateksti)
        print("selväpros  :", selvä_pros)
        print("salapros   :", sala_pros)

    x = np.arange(len(aakkoset))

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 6))

    if salateksti_puuttuu:
        x_siirros = 0
    else:
        x_siirros = 0.2

    ax.bar(x-x_siirros, selvä_pros, width=leveys, ls='dotted',
           lw=3, fc=(0, 0, 1, 0.5), label="Selväteksti")

    if not salateksti_puuttuu:
        ax.bar(x+x_siirros, sala_pros,  width=leveys, ls='dotted',
               lw=3, fc=(1, 0, 0, 0.5), label="Salateksti")

    if False:
        for i, v in enumerate(selvä_pros):
            ax.text(i-0.5, v + 0.1, str(v), color='blue', alpha=0.7, fontweight='bold')

        if not salateksti_puuttuu:
            for i, v in enumerate(sala_pros):
                ax.text(i-0.5, v + 0.1, str(v), color='red', alpha=0.7, fontweight='bold')

    x_labels = list(aakkoset)
    plt.xticks(x, x_labels)

    plt.ylabel("Esiintymistiheys", fontsize=18)
    plt.xlabel("Kirjain", fontsize=18)
    plt.legend()

    if otsikko is None:
        otsikko = "Tuntematon aineisto"

    plt.title("Aineisto: {}".format(otsikko), fontsize=20)

    if kurvi:
        f1 = interp1d(x, np.array(selvä_pros), kind='cubic')
        f2 = interp1d(x, np.array(sala_pros), kind='cubic')

        xnew = np.linspace(x.min(), x.max(), num=601, endpoint=True)
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
