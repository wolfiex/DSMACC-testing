import re
import pandas as pd

 data = re.findall(r'fractional difference aim 0 :  (\d+\.\d+)',''.join(tuple(open('temp.txt'))))
