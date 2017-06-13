"""
*******************
*                 *
* Library frmtRXN *
*                 *
*******************

PURPOSE:
    Combine kinetic data of individual duplicate reactions
    stored in entry 1 of the rrate dictionary. Different rates
    are summed up and of several rates of same kind, a product
    is formed. (see help function cmbnRATES for more information)

FUNCTIONS:
    - cmbnRATES
"""


def cmbnRATES(rrate):

    """
    **********************
    *                    *
    * Function cmbnRATES *
    *                    *
    **********************

    PURPOSE:
        Combine kinetic data of individual duplicate reactions
        stored in entry 1 of the rrate dictionary. Different rates
        are summed up and of several rates of same kind, a product
        is formed.

    IMPORTED PYTHON LIBRARIES:
        numpy (as np)

    VARIABLES:

    I/O:
        - rrate:    dictionary with mechanistic and kinetic data of
                    combined duplicate reactions and line numbers of
                    all duplicate entries

    internal:
        - key:      counter for loop over keys in rrate
        - i,j,k:    counter for loops
        - crate:    list strings of kinetic data of individual reactions
        - cm:       multiplier for crate (number of occurrences of
                    individual rate constants for particular multiple entry)

    """

# import python libraries
    import numpy as np

# loop over all multiple entries
    for key in rrate:
# initialise lists of individual kinetic data and  number of occurrences
# with rate of first occurrence
        cm    = [1]
        crate = [rrate[key][1][0]]

# loop over all kinetic data stored for current multiple entry:
        for i in range(len(rrate[key][1])-1):
# find new different rates for current key and append crate list
            if all([crate[k] != rrate[key][1][i] \
                for k in range(len(crate))]) \
                and rrate[key][1][-1] != None:
                crate.append(rrate[key][1][i])
                cm.append(1)
# second loop over all kinetic data stored for current multiple entry:
            for j in range(i+1,len(rrate[key][1])):

# find same rates and increase mulitplier for these rates
                if rrate[key][1][i] == rrate[key][1][j] and \
                    rrate[key][1][i] != None:
                    cm[crate.index(rrate[key][1][i])] += 1
# set second rrate entry to none to avoid double counts
                    rrate[key][1][j] = None

# Check occurrence of last entry of kinetic data in list
# as last entry is skipped in first loop
        if all([crate[k] != rrate[key][1][-1] \
            for k in range(len(crate))]) and rrate[key][1][-1] != None:
            crate.append(rrate[key][1][-1])
            cm.append(1)

# Reformat dictionary entry with kinetic data information
# from list of indidual kinetic rates to string of overall rate

# initialise with first
# use multiplier only when not 1
        if cm[0] == 1:
            rrate[key][1] = crate[0]
        else:
            rrate[key][1] = str(cm[0])+'*'+crate[0]

# add further rates with "+", then multiplier (if different from 1),
# then kinetic data
        for i in range(1,len(crate)):
            if cm[i] == 1:
                rrate[key][1] += '+'+crate[i]
            else:
                rrate[key][i] += '+'+str(cm[i])+'*'+crate[i]
