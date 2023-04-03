from enum import IntEnum


class Divisions(IntEnum):
    A = 101
    B = 102
    C = 103
    D = 104
    E = 105
    F = 106
    G = 107
    H = 108
    I = 109
    J = 110
    K = 111
    L = 112
    M = 113
    N = 114
    O = 115
    P = 116
    Q = 117
    R = 118
    S = 119
    T = 120
    U = 121
    V = 122
    W = 123
    X = 124
    Y = 125
    Z = 126

    @classmethod
    def choices(cls):
        return((item.value,item.name) for item in cls)
    
    @classmethod
    def get_division_by_value(cls,value):
        for division in cls.__members__.values():
            if division.value == value:
                return division.name