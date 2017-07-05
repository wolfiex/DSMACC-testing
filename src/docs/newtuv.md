


## Using different TUV hard-wiring 
To use a different tuv mapping for your mechanism (e.g. MCM or GEOSCHEM), insert the following into your mechanism file. The default is 1 for the MCM3.3.1 using tuv5. 

                #INLINE F90_INIT
                  TUVvers = 1
                #ENDINLINE

Currently the switches correspond to 

| tuv_old | tuv5_mcm3 | tuv5_mcm4 | tuv5_geoschem |
| :---         |     :---:      |     :---:      |         ---: |
| 0 | 1 | 2 | 3 |   



