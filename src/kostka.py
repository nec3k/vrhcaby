import random
class Kostka:
    def __init__(self):
        self.kostky = []
    def hod_kostky(self):
        kostka_1 = random.randint(1,6)
        kostka_2 = random.randint(1,6)
        if kostka_1 == kostka_2:
            self.kostky = [kostka_1, kostka_1, kostka_2, kostka_2]
        else:
            self.kostky = [kostka_1, kostka_2]
        """
        Hod - vygeneruje nahodne cislo od min_hodnota do max_hodnota

        Returns:
        int - nahodne cislo od min_hodnota do max_hodnota
        """
        
