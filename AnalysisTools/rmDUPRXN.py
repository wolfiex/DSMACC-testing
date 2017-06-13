"""
*********************
*                   *
* Function rmDUPRXN *
*                   *
*********************

PURPOSE:
    Remove duplicate reactions from kpp file and combine all reaction rates.
    Script is designed for DSMACC version DSMACC-testing available from:
    https://github.com/pb866/DSMACC-testing.git

INSTRUCTIONS:
    - Run kpp and write screen output to a file with:
      make kpp | tee <file name (default: make.tee)>
    - Run script with:
      python rmDUPRXN.py [<file name>]
      Script argument is optional and default value will be used,
      if obsolete.

IMPORTED PYTHON LIBRARIES:
    - sys

FURTHER LIBRARIES:
    - srchRXN (as sr) with functions duplicate reactions and save
                      necessary data to the dictionary rrate
    - frmtRXN (as fr) with a function to reformat the reaction rate string
                      with combined rate constants
    - fhandle (as fh) with a function to write the refined mechanims

VARIABLES:
    ftee:   file name of input tee file
    ll:     array with all lines from tee file
    duprxn: all lines from tee file with warnings about duplicate reactions
    rrate:  dictionary with:
            - key:      line number of first occurrence of duplicate reaction
            - entry 0:  kpp line of first occurrence up to colon
                        (excluding kinetic information)
            - entry 1:  cominded rate constants/j values
            - entry 2:  list of line numbers of all other occurrences of
                        this duplicate reaction
    fkpp:   path + name of kpp file retrieved from warnings
    f:      index for input file
"""

# import libraries
import sys
import srchRXN as sr
import frmtRXN as fr
import fhandle as fh
# specify system settings
reload(sys)
sys.setdefaultencoding('UTF8')

# Retrieve file name from script arguments
try:
    ftee = sys.argv[1]
except:
    ftee = '../make.tee'

# Assure input file is one folder level above:
if ftee[:3] != '../':
    ftee = '../'+ftee


# Open input file
with open(ftee, 'r')  as f:
# save all lines in an array
    ll = f.readlines()
# find warnings about duplicate reactions and save to array
    duprxn = [dr for dr in ll if ": Duplicate equation: " in dr]

# create library with line numbers of first duplicate entry as key
# - Reaction string up to colon (excluding rate constants) as first entry
# - List of strings of rate constants as second entry
# - List of line number with duplicate reactions (excluding first occurrence)
#   as third entry
rrate, fkpp = sr.retrRXN(duprxn)

# Reformat reaction rate constants and combine same rate constants
fr.cmbnRATES(rrate)
# Rewrite refined mechanism
fh.wrtKPP(rrate,fkpp)
