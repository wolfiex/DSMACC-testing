
def order(val):
    """
    Function order
    ==============

    Purpose:
    Determine the order of magnitude of a given value (val).
    Return the order as number and a factor 10^(order).

    Variables:
    I/O:
    val:    input value (any number)
    ord:    order of magnitude
    (negative integers for values < 0, 0 for 0, positvie values for values > 0)
    mult:   factor 10^(order)

    Dependencies:
    uses:           numpy
    called from:    fitfcn.fitTUV, fitfcn.fitStat, pltfcn.scatdat
    """
    import numpy as np
    if (val != 0):
        ord  = np.floor(np.log10(np.abs(val)))
    else:
        ord = 0
    mult = 10**ord
    return ord, mult
