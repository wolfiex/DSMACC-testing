"""
*******************
*                 *
* Library srchRXN *
*                 *
*******************

PURPOSE:
    Find all duplicate reactions in kpp file from kpp warnings. Combine
    all reaction rate constants as sum of individual constants (and
    product for several entries of same kind) and return a dictionary
    'rrate' with:
    - key:      line number of first occurrence of duplicate reaction
    - entry 0:  kpp line of first occurrence up to colon
                (excluding kinetic information)
    - entry 1:  cominded rate constants/j values
    - entry 2:  list of line numbers of all other occurrences of
                this duplicate reaction

FUNCTIONS:
    - retrRXN
    - fndDRXN
    - react
    - makeDICT

    (see help on individual functions for more information)
"""

########################################################################

def retrRXN(duprxn):

    """
    ********************
    *                  *
    * Function retrRXN *
    *                  *
    ********************

    PURPOSE:
        Retrieve line numbers of duplicate reactions in kpp file and
        generate dictionary rrate to return to main script rmDUPRXN.
        Also returns kpp file path + name needed to rewrite the re-
        fined kpp file.


    DESCRIPTION:
        retrRXN splits kpp warnings from screen output into segments
        and retrieves information about, which kpp file was used, the
        line numbers of the duplicate reaction, and then generates the
        dictionary rrate with information about the mechanistic and
        kinetic data of the combined reactions and all line numbers
        of the duplicate entries.
        Script files have to be stored in a folder 1 level below main.
        The designated folder is AnalysisTools.


    IMPORTED PYTHON LIBRARIES:
        - numpy (as np)


    VARIABLES:

    I/O:
        - duprxn:   list of kpp warnings about duplicate reactions
        - rrate:    dictionary with mechanistic and kinetic data of
                    combined duplicate reactions and line numbers of
                    all duplicate entries
        - fkpp:     path + name of kpp file retrieved from warnings

    internal:
        - l:        index for loop over warning messages
        - spl:      tempary array with warnings split into segments
                    separated by colon
        - dr:       index of line number of duplicate entry that is
                    to be kept and modified (i.e. actual line number - 1)
        - dl:       index of line number of duplicate entry that is
                    to be deleted (i.e. actual line number - 1)
        - RIND:     temporary memory of string with kpp equation
                    numbers of duplicate entries from kpp warning
        - rxn:      array with reaction numbers of duplicate entries
                    used to derive line numbers
        - i1/i2:    indices for string manipulation
        - ldup:     list of all lines from kpp file

    """

# Import python functions
    import numpy as np

# Initialise dictionary
    rrate  = {}

# Loop over all kpp warnings about duplicate reactions
    for l in range(len(duprxn)):

# Retrieve information about equation/line numbers and file path/name
# from warning messages
        spl = duprxn[l].split(':')
        fkpp = '.'+spl[1]
        dl = int(spl[2])-1
        RIND = spl[4]
        rxn = np.empty(2,int)
        i1 = RIND.index('<')+1
        i2 = RIND.index('>')
        rxn[0] = RIND[i1:i2]
        i1 = RIND.index('<',RIND.index('='))+1
        i2 = RIND.index('>',RIND.index('='))
        rxn[1] = RIND[i1:i2]

# Find line numbers of duplicate reactions from kpp warnings and
# search same educts products in kpp file and store all lines
# from kpp file
        dr, ldup = fndDRXN(dl, dl+1+rxn[0]-rxn[1], fkpp)

# Generate and return dictionary with mechanistic and kinetic
# data of combined reactions and line numbers of duplicate entries
        rrate = makeDICT(rrate, ldup, dl, dr)

    return rrate, fkpp

########################################################################

def fndDRXN(dl, rl, fkpp):

    """
    ********************
    *                  *
    * Function fndDRXN *
    *                  *
    ********************

    PURPOSE:
        Find line numbers of duplicate entries from line number and equation
        numbers given in kpp warning.

    NB:
        Line numbers differ from equation numbers due to comments/empty lines.

    VARIABLES:

    I/O:
        - rl:       index of line number of duplicate entry that is
                    to be kept and modified (i.e. actual line number - 1)
        - dl:       index of line number of duplicate entry that is
                    to be deleted (i.e. actual line number - 1)
        - fkpp:     path + name of kpp file retrieved from warnings
        - l:        counter for loop over lines in kpp file and return value
                    of refined dr variable
        - ll:       list of all lines from kpp file

    internal:
        - drxn/rrxn:array with educt and products of both duplicate entries
                    to find the correct lines of the duplicate entries
    """

# read all lines from kpp file
    with open(fkpp,'rw') as f:
        ll = f.readlines()
# find educts/products of second duplicate entry
        drxn = react(ll[dl])

# find line number of first duplicate entry
# search starts at line number of second duplicate entry retrieved from
# kpp warning minus the equation number of second duplicate entry plus
# the equation number of the first duplicate entry.
# Due to empty/comment lines a loop has to be performed from the starting
# line to the top of the file.
        for l in reversed(xrange(rl)):
# find educts/products of first duplicate entry
            rrxn = react(ll[l])

# If educts/products are equal, exit loop and return loop index
# as refined index for line number of first duplicate entry
            if drxn == rrxn:
                break
    return l,ll

########################################################################

def react(line):

    """
    ******************
    *                *
    * Function react *
    *                *
    ******************

    PURPOSE:
        Retrieve all educts and products from from a kpp reaction.

    NB:
        To find all duplicate reactions, educts and products have to be
        compared rather than comparing reaction strings directly as species
        can appear in different order in the duplicate reactions.
        Educt/product arrays are sorted for direct comparison.

    VARIABLES:

    I/O:
        line:   string of kpp line with reaction
        edct:   sorted array of all educts
        prod:   sorted array of all products

    internal:
        e/p:    counter for loops over educts/products
    """

# Retrived string with mechanistic data of educts from kpp line
    edct = line[line.index('}')+1:line.index('=')].split('+')
# Split into separate educts using '+' as separator and sort list
    edct = sorted([e.strip() for e in edct])
# Retrived string with mechanistic data of products from kpp line
    prod = line[line.index('=')+1:line.index(':')].split('+')
# Split into separate products using '+' as separator and sort list
    prod = sorted([p.strip() for p in prod])

# return educt and product list
    return edct,prod

########################################################################

def makeDICT(rrate, ldup, dl, dr):

    """
    *********************
    *                   *
    * Function makeDICT *
    *                   *
    *********************

    PURPOSE:
        Generate dictionary with mechanistic and kinetic data of refined
        reaction from duplicate entries and retrieve line numbers of all
        duplicate entries.
        Dictionary 'rrate':
        - key:      line number of first occurrence of duplicate reaction
        - entry 0:  kpp line of first occurrence up to colon
                    (excluding kinetic information)
        - entry 1:  cominded rate constants/j values
        - entry 2:  list of line numbers of all other occurrences of
                    this duplicate reaction


    VARIABLES:

    I/O:
        - rrate:    dictionary with mechanistic and kinetic data of
                    combined duplicate reactions and line numbers of
                    all duplicate entries
        - ldup:     list of all lines from kpp file
        - dr:       index of line number of duplicate entry that is
                    to be kept and modified (i.e. actual line number - 1)
        - dl:       index of line number of duplicate entry that is
                    to be deleted (i.e. actual line number - 1)
    """

# append existing key (i.e. already found first line number of duplicate reaction)
# by line number and kinetic data of second (or further) duplicate entry
    if rrate.has_key(dr):
        rrate[dr][1].append(ldup[dl][ldup[dl].index(':')+1:ldup[dl].index(';')].strip())
        rrate[dr][2].append(dl)
    else:
# If no key found generate key using line number of first duplicate entry
# and specify kinetic data of first and second entry as well as line number of second entry
        rrate[dr] = [ldup[dr][:ldup[dr].index(':')+1]]
        rrate[dr].append([ldup[dr][ldup[dr].index(':')+1:ldup[dr].index(';')].strip()])
        rrate[dr][1].append(ldup[dl][ldup[dl].index(':')+1:ldup[dl].index(';')].strip())
        rrate[dr].append([dl])

    return rrate

########################################################################
