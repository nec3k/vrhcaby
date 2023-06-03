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
            return 'bílá'
        else:
            return 'černá'

    @classmethod
    def load(str) -> 'Barva':
        if str == 'cerna':
            return Barva.cerna
        elif str == 'bila':
            return Barva.bila
        else:
            raise Exception("%s není platná barva" % str)
