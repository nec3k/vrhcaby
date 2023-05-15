from typing import Any

class Policko:
    """
    Policko - funguje podobne jako zasobnik
    """
    def __init__(self):
        self.zasobnik = Stack()
    def pridat(self, kamen) -> None:
        """
        pridat - prida na policko kamen, pokud to jde podle pravidel, jinak vyhodi vyjimku
        """
    def lze_pridat(self, kamen) -> bool:
        """
        lze_pridat - vyhodnocuje, zda lze pridat kamen na herni policko

        returns:
            bool - Jestli lze kamen pridat na toto policko
        """
    def odebrat(self) -> Any:
        """
        odebrat - odebere kamen z vrchu zasobniku

        returns:
            Any - objekt navrchu zasobniku
        """
