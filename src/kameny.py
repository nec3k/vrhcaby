from src.barva import Barva

class Kameny:
    def __init__(self, barva, pozice):
        self.barva = barva
        self.pozice = pozice
    def dostane_do_cile(self):
        if self.barva == Barva.bily:
            return 25 - self.pozice
        else:
            return self.pozice
        