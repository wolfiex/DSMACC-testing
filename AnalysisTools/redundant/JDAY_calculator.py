''' Python program to calculate the JDAY form a set of inputs
Input format: month.day.hour.time
Summer solstice = june 21
Winter Solstace = december 21

D.Ellis, daniel.ellis.research Dec. 2016
'''

import datetime,sys
  
fmt = '%Y.%m.%d.%H.%M'
string = '2016.'+sys.argv[1]
dt = datetime.datetime.strptime(string, fmt)
print 'Selected Day:'
print dt



tt = dt.timetuple()
print 'Corresponding Julain Day:' 
print '%.3f' %( tt.tm_yday +  (dt.hour + dt.minute/60.)/24. )



