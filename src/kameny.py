from src.barva import Barva

class Kameny:

    #je konstruktorem třídy, self.barva je atribut pro uchování barvy kamene, self.pozice je atribut pro uchování pozice kamene
    def __init__(self, barva, pozice):
        self.barva = barva
        self.pozice = pozice

    #Slouží k výpočtu vzdálenosti kamene do cíle
    #Pokud barva kamene je bílá, vrátí se rozdíl mezi 25 a hodnotou atributu pozice. 
    # Pokud barva není bílá (je černá), vzdálenost je rovna pozice kamene
    def dostane_do_cile(self):
        if self.barva == Barva.bila:
            return 25 - self.pozice
        else:
            return self.pozice
        