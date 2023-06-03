import json
from random import randint

from src.hraci_deska import Hraci_deska
from src.barva import Barva
from src.strategie import Strategie
from src.provedeni_neplatneho_tahu import Provedeni_neplatneho_tahu

class Nacteni_hraci_desky:
    hraci_deska: Hraci_deska

    def __init__(self, hraci_deska):
        self.hraci_deska = hraci_deska

    def __getattr__(self, jmeno):
        if hasattr(self.hraci_deska, jmeno) and callable(getattr(self.hraci_deska, jmeno)):
            return getattr(self.hraci_deska, jmeno)

        return super(Nacteni_hraci_desky, self).__getattr__(jmeno)

    def pridavani_kamene(self, pocet_kamene, barva, pozice):
        self.__raise_exception__()

    def presunuti_kamene(self, kamen, hod_kostek):
        self.__raise_exception__()

    def __raise_exception__(self):
        raise Exception("Chyba")
    
class Hra:
    def __init__(self, bila_strategie: Strategie, cerna_strategie: Strategie, hrac_zacina_hru: Barva):
        self.hraci_deska = Hraci_deska.puvodni_hraci_deska()
        self.hrac_zacina_hru = hrac_zacina_hru
        self.strategie = {
            Barva.bila: bila_strategie,
            Barva.cerna: cerna_strategie
        }
    
    def spusteni_hry(self, verbose = True):
        if verbose:
            print("%s začíná hru" % self.hrac_zacina_hru)
            self.hraci_deska.vytisknuti_hraci_desky()
        i = self.hrac_zacina_hru.value
        tahy = []
        seznam_hodnot_kostek = []
        while True:
            predchozi_hod_kostkami = seznam_hodnot_kostek.copy()
            hod_kostkami = [randint(1,6), randint(1,6)]
            if hod_kostkami[0] == hod_kostkami[1]:
                hod_kostkami = [hod_kostkami[0]] * 4
            seznam_hodnot_kostek = hod_kostkami.copy()
            barva = Barva(i % 2)
            if verbose:
                print("%s byly vyhozeny %s" % (barva, hod_kostkami))
            
            def provedeni_tahu(pozice, hodnota_kostky):
                hodnota_pro_provedeni_tahu = self.ziskani_hodu_kostkou_pro_provedeni_tahu(pozice, hodnota_kostky, hod_kostkami)
                if hodnota_pro_provedeni_tahu is None:
                    raise Provedeni_neplatneho_tahu("Nelze posunout ten kámen o %d" % hodnota_kostky)
                for hodnota in hodnota_pro_provedeni_tahu:
                    kamen = self.hraci_deska.kameny_na_zadane_pozici(pozice)
                    puvodni_pozice = pozice
                    pozice = self.hraci_deska.posune_kamen(kamen, hodnota)
                    hod_kostkami.remove(hodnota)
                    tahy.append({'puvodni_pozice': puvodni_pozice, 'hodnota_kostky': hodnota, 'nove_pozice': pozice})
                    predchozi_hod_kostkami.append(hodnota)
                return hodnota_pro_provedeni_tahu
            
            hraci_deska_snapshot = self.hraci_deska.to_json()
            hod_kostkami_snapshot = hod_kostkami.copy()

            tahy_protihrace = tahy.copy()
            tahy.clear()

            self.strategie[barva].tah(
                Nacteni_hraci_desky(self.hraci_deska),
                barva,
                hod_kostkami.copy(),
                lambda pozice, hodnota_kostky: provedeni_tahu(pozice, hodnota_kostky),
                {'hod_kostkami': predchozi_hod_kostkami, 'tahy_protihrace': tahy_protihrace}
            )

            if verbose and len(hod_kostkami) > 0:
                print('Nebyly provedeny všechny tahy. %s hraje %s neposune %s' % (
                    barva,
                    self.strategie[barva].__class__.__name__,
                    hod_kostkami))
                self.hraci_deska.vytisknuti_hraci_desky()
                state = {
                    'hraci_deska': json.load(hraci_deska_snapshot),
                    'hod_kostkami': hod_kostkami_snapshot,
                    'barva_ma_tah': barva.__str__(),
                    'strategie': self.strategie[barva].__class__.__name__,
                }
                print(json.dumps(state))
            
            if verbose:
                self.hraci_deska.vytisknuti_hraci_desky()
            i = i + 1
            if self.hraci_deska.hra_konci():
                if verbose:
                    print('%s vyhraje!' % self.hraci_deska.kdo_vyhraje())
                    self.strategie[barva.other()].game_over({
                        'hod_kostkami': seznam_hodnot_kostek,
                        'tah protihrace': tahy

                    })
                    break

    def ziskani_hodu_kostkou_pro_provedeni_tahu(self, pozice, pozadovany_tah, dostupny_hod):
        if dostupny_hod.__contains__(pozadovany_tah):
            if self.hraci_deska.muze_posunout(self.hraci_deska.kameny_na_zadane_pozici(pozice), pozadovany_tah):
                return [pozadovany_tah]
            return None
        if len(dostupny_hod) == 1:
            return None
        hraci_deska = self.hraci_deska.vytvori_kopie()
        hodnota_pro_provedeni_tah = []
        soucasna_pozice = pozice
        if not hraci_deska.muze_posunout(hraci_deska.kameny_na_zadane_pozici(soucasna_pozice), dostupny_hod[0]):
            dostupny_hod = dostupny_hod.copy()
            dostupny_hod.reverse()
        
        for hodnota in dostupny_hod:
            kamen = hraci_deska.kameny_na_zadane_pozici(soucasna_pozice)
            if not hraci_deska.muze_posunout(kamen, hodnota):
                break
            soucasna_pozice = hraci_deska.posune_kamen(kamen, hodnota)
            hodnota_pro_provedeni_tah.append(hodnota)
            if sum(hodnota_pro_provedeni_tah) == pozadovany_tah:
                return hodnota_pro_provedeni_tah
        return None

    def kdo_zacina_hru(self):
        return self.hrac_zacina_hru
    def kdo_vyhraje(self):
        return self.hraci_deska.kdo_vyhraje()

