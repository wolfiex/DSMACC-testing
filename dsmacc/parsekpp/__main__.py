import argparse,sys
from __init__ import *

parser = argparse.ArgumentParser(description='Kpp preformatting')
parser.add_argument('-d','--dot', dest='dot', action='store_true', default=False, help='add a watch reload for dev')
parser.add_argument('-l','--last', dest='last', action='store_true', default=False, help='add a watch reload for dev')
parser.add_argument('-r','--reformat', dest='reformat', action='store_true', default=False, help='run with obs')
args = parser.parse_args()
print args,sys.argv
if args.dot:
            make_model_dot(args.last)
