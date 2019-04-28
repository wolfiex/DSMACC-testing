
import argparse,os,sys

parser = argparse.ArgumentParser(description='create an ics')

parser.add_argument('file', type=str)
parser.add_argument('timestep',type=int)

parser.add_argument('-r','--rmspinup', dest='rmspinup', action='store_true', default=False, help='remove spinup runs')

args = parser.parse_args()

print 'initialisation arguments:'
print args

from __init__ import * 

print ( newics( args.file, timestep=args.timestep, rmspinup = args.rmspinup, write =True, lump = False) )