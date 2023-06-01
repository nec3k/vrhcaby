from random import shuffle
import json
import copy

from src.barva import Barva
from src.kameny import Kameny

class Hraci_deska:
    def __init__(self):
        self._kameny = []
    
    @classmethod
    def puvodni_hraci_deska(cls):
        hraci_deska = Hraci_deska()
        hraci_deska.pridavani_kamene(2, Barva.bila, 1)
        hraci_deska.pridavani_kamene(5, Barva.cerna, 6)
        hraci_deska.pridavani_kamene(3, Barva.cerna, 8)
        hraci_deska.pridavani_kamene(5, Barva.bila, 12)
        hraci_deska.pridavani_kamene(5, Barva.cerna, 13)
        hraci_deska.pridavani_kamene(3, Barva.bila, 17)
        hraci_deska.pridavani_kamene(5, Barva.bila, 19)
        hraci_deska.pridavani_kamene(2, Barva.cerna, 24)
        return hraci_deska
    
    def pridavani_kamene(self, pocet_kamenu, barva, pozice):
        for i in range(pocet_kamenu):
            self._kameny.append(Kameny(barva, pozice))

    def muze_posunout(self, kamen, hodnota_kostky):
        if len(self.seznam_kamenu_na_zadane_pozici(self.pozice_vzateho_kamene(kamen.barva))) > 0:
            if kamen.pozice != self.pozice_vzateho_kamene(kamen.barva):
                return False
        if kamen.barva == Barva.cerna:
            hodnota_kostky = -hodnota_kostky
        nova_pozice = kamen.pozice + hodnota_kostky
        if nova_pozice <= 0 or nova_pozice >= 25:
            if not self.muze_posunout_pryc(kamen.barva):
                return False
            if nova_pozice != 0 and nova_pozice != 25:
                return not any(x.dostane_do_cile() >= abs(hodnota_kostky) for x in self.seznam_kamenu(kamen.barva))
            return True
        kamen_v_nove_pozici = self.seznam_kamenu_na_zadane_pozici(nova_pozice)
        if len(kamen_v_nove_pozici) == 0 or len(kamen_v_nove_pozici) == 1:
            return True
        return self.seznam_kamenu_na_zadane_pozici(nova_pozice)[0].barva == kamen.barva

    def nemuze_posunout(self, barva, hod_kostkami):
        pozice_kamenu = [x.pozice for x in self.seznam_kamenu(barva)]
        pozice_kamenu  = list(set(pozice_kamenu))

        hod_kostkami = list(set(hod_kostkami))

        kameny = []
        for pozice_kamene in pozice_kamenu:
            kameny.append(self.kameny_na_zadane_pozici(pozice_kamene))
        for hodnota in hod_kostkami:
            for kamen in kameny:
                if self.muze_posunout(kamen, hodnota):
                    return False
        return True
    
    def muze_posunout_pryc(self, barva):
        return all(x.dostane_do_cile() <= 6 for x in self.seznam_kamenu(barva))
    
    def posune_kamen(self, kamen, hodnota_kostky):
        if not self.kameny.__contains__(kamen):
            raise Exception('Ten kámen není ve hrací desce')
        if not self.muze_posunout(kamen, hodnota_kostky):
            raise Exception('Nemůže posunout')
        if kamen.barva == Barva.cerna:
            hodnota_kostky = -hodnota_kostky

        nova_pozice = kamen.pozice + hodnota_kostky
        if nova_pozice <= 0 or nova_pozice >= 25:
            self.odebrani_kamene(kamen)

        kamen_v_nove_pozici = self.seznam_kamenu_na_zadane_pozici(nova_pozice)

        if len(kamen_v_nove_pozici) == 1 and kamen_v_nove_pozici[0].barva != kamen.barva:
            posunuty_kamen = kamen_v_nove_pozici[0]
            posunuty_kamen.pozice = self.pozice_vzateho_kamene(posunuty_kamen.barva)

        kamen.pozice = nova_pozice
        return nova_pozice

    def seznam_kamenu_na_zadane_pozici(self, pozice):
        return [x for x in self._kameny if x.pozice == pozice]
    
    def kameny_na_zadane_pozici(self, pozice):
        kameny = self.seznam_kamenu_na_zadane_pozici(pozice)
        if len(kameny) == 0:
            return None
        return kameny[0]

    def seznam_kamenu(self, barva):
        kameny = [x for x in self._kameny if x.barva == barva]
        shuffle(kameny)
        return kameny
    
    def seznam_odebranych_kamenu(self, barva):
        return self.seznam_kamenu_na_zadane_pozici(self.pozice_vzateho_kamene(barva))
    
    def hra_konci(self):
        return len(self.seznam_kamenu(Barva.bila)) == 0 or len(self.seznam_kamenu(Barva.cerna)) == 0
    
    def kdo_vyhraje(self):
        if not self.hra_konci():
            raise Exception('Hra ještě nekončí')
        return Barva.bila if len(self.seznam_kamenu(Barva.bila)) == 0 else Barva.cerna
    
    def vytvori_kopie(self):
        return copy.deepcopy(self)
    
    def posune_pomoci_lambda(self):
         return lambda l, r: self.posune_kamen(self.kameny_na_zadane_pozici(l), r)
    
    def vytisknuti_hraci_desky(self):
        print("  13                  18   19                  24   25")
        print("---------------------------------------------------")
        hranice = "|"
        for i in range(13, 18 + 1):
            hranice = hranice + self.textova_reprezentace_kamene(i)
        hranice = hranice + "|"
        for i in range(19, 24 + 1):
            hranice = hranice + self.textova_reprezentace_kamene(i)
        hranice = hranice + "|"
        hranice = hranice + self.textova_reprezentace_kamene(self.pozice_vzateho_kamene(Barva.cerna))
        print(hranice)
        for _ in range(3):
            print("|                        |                        |")
        hranice = "|"
        for i in reversed(range(7, 12+1)):
            hranice = hranice + self.textova_reprezentace_kamene(i)
        hranice = hranice + "|"
        for i in reversed(range(1, 6+1)):
            hranice = hranice + self.textova_reprezentace_kamene(i)
        hranice = hranice + "|"
        hranice = hranice + self.textova_reprezentace_kamene(self.pozice_vzateho_kamene(Barva.bila))
        print(hranice)
        print("---------------------------------------------------")
        print("  12                  7    6                   1    0")

    def textova_reprezentace_kamene(self, pozice):
        kameny = self.seznam_kamenu_na_zadane_pozici(pozice)
        if len(kameny) == 0:
            return " .  "
        if kameny[0].barva == Barva.bila:
            return " %sB " % (len(kameny))
        else:
            return " %sC " % (len(kameny))
        
    def pozice_vzateho_kamene(self, barva):
        if barva == Barva.bila:
            return 0
        else:
            return 25
        
    def to_json(self):
        data = {}
        for pozice in range(26):
            kameny = self.seznam_kamenu_na_zadane_pozici(pozice)
            if len(kameny) > 0:
                data[pozice] = {'barva': kameny[0].barva.__str__(), 'pocet': len(kameny)}
        return json.dumps(data)
    def odebrani_kamene(self, kamen):
        self.kamen.remove(kamen)