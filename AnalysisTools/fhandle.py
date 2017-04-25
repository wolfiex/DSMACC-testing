"""
*******************
*                 *
* Library fhandle *
*                 *
*******************

PURPOSE:
    Includes all routines concerned with reading/writing/manipulating files.

FUNCTIONS:
    - wrtKPP
"""

def wrtKPP(rrate,fkpp):

    """
    *******************
    *                 *
    * Function wrtKPP *
    *                 *
    *******************

    PURPOSE:
        Rewrite kpp file with revised duplicate reactions.

    IMPORTED PYTHON LIBRARIES:
        - system from os

    VARIABLES:

    I/O:
        - rrate:    dictionary with mechanistic and kinetic data of
                    combined duplicate reactions and line numbers of
                    all duplicate entries
        - fkpp:     path + name of kpp file retrieved from warnings

    internal:
        - key:      counter for loop over keys in rrate
        - i/d:      counter for loops
        - line:     list with lines of kpp file
        - f:        index for files
    """

# import python libraries
    from os import system

# Read in all lines from kpp file
    with open('../mechanisms/halfMCM1tchr.kpp','r+') as f:
        line = f.readlines()

# For duplicate reactions defined in rrate re-write reactions
# with refined kinetic data
        for key in rrate:
            line[key] = rrate[key][0]+"  "+rrate[key][1]+" ;\n"

# Delete all other lines with duplicate reactions
            for d in range(len(rrate[key][2])):
                line[rrate[key][2][d]] = ""

# Write output to temporary file
    with open('../mechanisms/temp.kpp','w+') as f:
        for i in range(len(line)):
            f.write(line[i])

# Use Unix to replace original kpp file with corrected file
    system("mv -f ../mechanisms/temp.kpp "+fkpp)
