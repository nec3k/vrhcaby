from random import randint
import random

from src.barva import Barva
from src.hra import Hra
from src.strategie import Multiplayer_Strategie

if __name__ == '__main__':

    mode = input("Proti AI nebo Multiplayer? \n")
    if mode ==  "Proti AI":
        pass

    else:
        #Hod kostek pro zjištění, že kdo bude hrát první
        #Pokud mají stejnou hodnotu => opakuje hod kostek
        kostka_hrac_1 = random.randint(1,6)
        kostka_hrac_2 = random.randint(1,6)

        while kostka_hrac_1 == kostka_hrac_2:
            kostka_hrac_1 = random.randint(1,6)
            kostka_hrac_2 = random.randint(1,6)

        if kostka_hrac_1 > kostka_hrac_2:
            hrac_zacina_hru = Barva.bila

        else:
            hrac_zacina_hru = Barva.cerna

        #1.hrac = bile kameny, 2.hrac = cerne kameny
        #Dictonary(slovník) přijímají jména hráčů: 2 keys Barva.bila, Barva.cerna
        hraci = {
            Barva.bila: input('Jméno 1.hráče: '),
            Barva.cerna: input('Jméno 2.hráče: ')
        }
        #vloží hodnotu 3 parametrů class Hra: bila_strategie, cerna_strategie, hrac_zacina_hru
        hra = Hra(
            bila_strategie = Multiplayer_Strategie(hraci[Barva.bila]),
            cerna_strategie = Multiplayer_Strategie(hraci[Barva.cerna]),
            hrac_zacina_hru = hrac_zacina_hru
        )

        #Spuští hru, verbose = False znamená, že nebude vypisovat informace o průběhu hry 
        hra.spusteni_hry(verbose=False)

        #vypisuje jméno vítěze hry 
        print("%s vyhraje!" % hraci[hra.kdo_vyhraje()])

        #stav hrací desky na konci hry
        hra.hraci_deska.vytiknuti_hraci_desky()
