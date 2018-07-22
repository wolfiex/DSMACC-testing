import re
eqns = re.findall(r'(A\(\d+\)\s+=\s+.*)\n' , '\n'.join(tuple(open('model_Function.f90'))).replace('V','C').replace('RCT','RCONST'))


print eqns

with open('model_ropa.f90','w') as f:
    f.write('''
    MODULE model_Flux
      IMPLICIT NONE

      CONTAINS

      subroutine writeflux(newtime)
            use model_global, ONLY: FLUX_UNIT,NREACT,C,RCONST,dp
            ! A - Rate for each equation
            REAL(kind=dp) :: A(NREACT),newtime  \n''')

    f.write('\n\t\t'.join(eqns))

    f.write('''
    WRITE (FLUX_UNIT) newtime, A
    end subroutine writeflux
    end module model_flux

      ''')
