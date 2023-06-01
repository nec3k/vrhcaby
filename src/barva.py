from enum import Enum


class Barva(Enum):
    bila = 0
    cerna = 1

    def other(self) -> 'Barva':
        if self == Barva.bila:
            return Barva.cerna
        else:
            return Barva.bila

    def __str__(self) -> str:
        if self == Barva.bila:
            return 'bila'
        else:
            return 'cerna'

    @classmethod
    def load(cls, Barva_str: str) -> 'Barva':
        if Barva_str == 'cerna':
            return Barva.cerna
        elif Barva_str == 'bila':
            return Barva.bila
        else:
            raise ValueError(f"{Barva_str} není platná barva")
