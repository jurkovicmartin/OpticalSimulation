"""
Other functions.
"""

def calculateTransSpeed(symbolRate: int, modulationOrder: int) -> int:
    """
    Calculates transmission speed in bits/s.
    """
    # How many bits are 1 symbol
    if modulationOrder == 2:
        symbolBits = 1
    elif modulationOrder == 4:
        symbolBits = 2
    elif modulationOrder == 8:
        symbolBits = 3
    elif modulationOrder == 16:
        symbolBits = 4
    elif modulationOrder == 32:
        symbolBits = 5
    elif modulationOrder == 64:
        symbolBits = 6
    elif modulationOrder == 128:
        symbolBits = 7
    elif modulationOrder == 256:
        symbolBits = 8
    else: raise Exception("Unexpected error")

    return symbolRate*symbolBits