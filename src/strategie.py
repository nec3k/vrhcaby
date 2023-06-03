import time
from random import shuffle
from src.kameny import Kameny
from src.provedeni_neplatneho_tahu import Provedeni_neplatneho_tahu

class Strategie:
    def tah(self, hraci_deska, barva, hod_kostkami, provedeni_tahu, tahy_protihace):
        raise NotImplemented()
    def game_over(self, tahy_protihace):
        pass
class Multiplayer_Strategie(Strategie):

    #Inicializuje třídu přijímá parametr jmeno, který představuje jméno hráče, pak jméno je uloženo do privátní proměnné _jmeno 
    def __init__(self, jmeno):
        self._jmeno = jmeno
    
    @staticmethod
    def rezim_hry():
        return "Multiplayer"
    #Implementuje tah hráče. 
    #Vypisuje kdo je na radě, hodnota hod kostkami, stav hrací desky
    #Hráč zadá kolik hodnotů, že chce posunout kamen
    def tah(self, hraci_deska, barva, hod_kostkami, provadi_tahu, tahy_protihace):
        print("%s je na řadě, a je %s. Hodnota kostek jsou %s" %(self._jmeno, barva, hod_kostkami))
        while len(hod_kostkami) > 0 and not hraci_deska.hra_konci():
            hraci_deska.vytisknuti_hraci_desky()
            if hraci_deska.nemuze_posunout(barva, hod_kostkami):
                print("Není žádný platný tah. Tvůj tah končí.")
                time.sleep(5)
                break
            print("Zbytek hodnoty je %s" % hod_kostkami)
            pozice = self.pozice_kamene(hraci_deska, barva)
            kamen = hraci_deska.kameny_na_zadane_pozici(pozice)
            while True:
                try:
                    hodnota = int(input("Kolik hodnot chcete posunout kámen (0 = posunout jiným kamenem)?\n"))
                    if hodnota == 0:
                        break
                    hodnota_pouzita_pro_posunuti = provadi_tahu(kamen.pozice, hodnota)
                    for hod in hodnota_pouzita_pro_posunuti:
                        hod_kostkami.remove(hod)
                    print("")
                    print("")
                    break
                except ValueError:
                    print("Neplatná hodnota! Zadejte pouze číslo!!!")
                except Provedeni_neplatneho_tahu as n:
                    print(str(n))

    #Slouží k získání pozice kamene
    #Čte vstup od hráče a ověřuje, zda je zadaná pozice platná. 
    #Pokud je pozice neplatná, vypíše se odpovídající zprávu, a hráč musí zadat  ještě jednou.
    def pozice_kamene(self, hraci_deska, barva):
        hodnota = None
        while hodnota is None:
            try:
                pozice = int(input("Zadejte políčko obsahující kámen, který chcete ho posunout?\n"))
                kamen_v_policku = hraci_deska.kameny_na_zadane_pozici(pozice)
                if kamen_v_policku is None or kamen_v_policku.barva != barva:
                    print("Nemáte žádný kámen v políčku %s" % hodnota)
                else:
                    hodnota = pozice
            except ValueError:
                print("Neplatná hodnota! Zadejte pouze číslo!!!")
        return hodnota

