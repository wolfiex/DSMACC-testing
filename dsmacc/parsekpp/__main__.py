import argparse,sys
from .__init__ import *

parser = argparse.ArgumentParser(description='Kpp preformatting')

#kpp model.kpp
parser.add_argument('-m','--model', dest='dot', action='store_true', default=False, help='add a watch reload for dev')
parser.add_argument('-l','--last', dest='last', action='store_true', default=False, help='add a watch reload for dev')

#reformat data
parser.add_argument('-d','--depos', dest='depos', action='store_true', default=False, help='add deposition terms')
parser.add_argument('-i','--inorganics', dest='inorganics', action='store_true', default=False, help='include inorganics')
parser.add_argument('-r','--reformat', dest='reformat', action='store_true', default=False, help='run reformatting')


args = parser.parse_args()
print(args,sys.argv)


if args.reformat:
    from .reformat import * 
    reformat_kpp(args.inorganics, args.depos)

if args.dot:
            make_model_dot(args.last)

