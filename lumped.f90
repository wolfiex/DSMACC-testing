module lumpedrates
USE model_Precision, ONLY: dp
use constants
IMPLICIT NONE

contains
 FUNCTION ET(a)
    USE model_global, only: TEMP
    real(dp) :: ET
    INTEGER    :: a
    ET = EXP(a/TEMP)
 END FUNCTION



end module lumpedrates
