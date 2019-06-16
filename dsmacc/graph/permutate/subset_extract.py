import re
coeff = re.compile(r'(\d)([\d\w]+)')#mcm only have int coeffs
inorganics = 'O,O1D,H2O2,N2O5,HONO,HO2NO2,HSO3,H,O2,A,NA,SA,Cl,CL,SO2,SO3,H2,HNO3,O3,OH,HO2,NO,NO2,NO3'.split(',')
def split_eqn(eqns):
    '''
    split eqns and decoeffy
    '''
    e=[]
    for i in eqns:
        i = list(i)
        #reactants
        d=[]
        for j in i[0].split('+'):
            repeat=1
            test = coeff.match(j)
            if test:
                repeat,j= test.groups()

            for z in range(repeat):
                d.append(j)

        i[0] = d
        #products
        d=[]
        for j in i[1].split('+'):
            repeat=1
            test = coeff.match(j)
            if test:
                repeat,j= test.groups()

            for z in range(repeat):
                d.append(j)

        i[1] = d

        e.append(i)

    return e



def subset(eqn,species):
        '''
        get a subset
        input:
            species - set
            eqn - list or tuple
        '''
        gen = xrange(len(eqn))
        species = set(species) | set(inorganics)
        eq_split = [set(i[0]) for i in eqn]
        counter = 0
        while True:
            newlyfound = ''
            skipped = ''

            counter += 1 ;#print str(counter) + ["th", "st", "nd", "rd"][counter%10 if counter%10<4 and not (10<counter%100<14) else 0] + '\033[37m iteration'
            dummy = list(species)
            for i in gen:
                if eq_split[i].issubset(species):
                    dummy.extend(eqn[i][1])

            dummy = set(dummy)
            
            if dummy == species: break
            species = dummy

        eql=[]
        for i in gen:
            if eq_split[i].issubset(species):
                eql.append(eqn[i])

        return [species, eql]
