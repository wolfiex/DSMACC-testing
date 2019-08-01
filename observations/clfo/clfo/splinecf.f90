
subroutine spline (n, x, y,b,c,d)
      implicit none
      integer,intent(in):: n
      double precision,intent(in):: x(n), y(n)
      double precision,intent(out):: b(n), c(n), d(n)
      integer nm1, ib, i
      double precision t

      print*, 'F2PY: generating coefficients for spline'

      nm1 = n-1
      if ( n .lt. 2 ) return
      if ( n .lt. 3 ) go to 50

      d(1) = x(2) - x(1)
      c(2) = (y(2) - y(1))/d(1)
      do 10 i = 2, nm1
         d(i) = x(i+1) - x(i)
         b(i) = 2.*(d(i-1) + d(i))
         c(i+1) = (y(i+1) - y(i))/d(i)
         c(i) = c(i+1) - c(i)
  10  continue

      b(1) = -d(1)
      b(n) = -d(n-1)
      c(1) = 0.
      c(n) = 0.
      if ( n .eq. 3 ) go to 15
      c(1) = c(3)/(x(4)-x(2)) - c(2)/(x(3)-x(1))
      c(n) = c(n-1)/(x(n)-x(n-2)) - c(n-2)/(x(n-1)-x(n-3))
      c(1) = c(1)*d(1)**2/(x(4)-x(1))
      c(n) = -c(n)*d(n-1)**2/(x(n)-x(n-3))

   15 do 20 i = 2, n
         t = d(i-1)/b(i-1)
         b(i) = b(i) - t*d(i-1)
         c(i) = c(i) - t*c(i-1)
   20 continue

      c(n) = c(n)/b(n)
      do 30 ib = 1, nm1
         i = n-ib
         c(i) = (c(i) - d(i)*c(i+1))/b(i)
   30 continue

      b(n) = (y(n) - y(nm1))/d(nm1) + d(nm1)*(c(nm1) + 2.*c(n))
      do 40 i = 1, nm1
         b(i) = (y(i+1) - y(i))/d(i) - d(i)*(c(i+1) + 2.*c(i))
         d(i) = (c(i+1) - c(i))/d(i)
         c(i) = 3.*c(i)
   40 continue
      c(n) = 3.*c(n)
      d(n) = d(n-1)
      return

   50 b(1) = (y(2)-y(1))/(x(2)-x(1))
      c(1) = 0.
      d(1) = 0.
      b(2) = b(1)
      c(2) = 0.
      d(2) = 0.
      return
end subroutine

subroutine seval(n, u, x, y, b, c, d,s)

      integer n
      double precision  u, x(n), y(n), b(n), c(n), d(n)
      integer i, j, k
      double precision dx
      double precision,intent(out):: s
      data i/1/
      if ( i .ge. n ) i = 1
      if ( u .lt. x(i) ) go to 10
      if ( u .le. x(i+1) ) go to 30

   10 i = 1
      j = n+1
   20 k = (i+j)/2
      if ( u .lt. x(k) ) j = k
      if ( u .ge. x(k) ) i = k
      if ( j .gt. i+1 ) go to 20

   30 dx = u - x(i)
      s = y(i) + dx*(b(i) + dx*(c(i) + dx*d(i)))
      return
      end subroutine


subroutine writeobs (n,arr)
  implicit NONE
  INTEGER, PARAMETER :: dp = SELECTED_REAL_KIND(14,300)
  integer n
  Real(dp) arr(n,27)

  OPEN(unit = 10, FORM = 'unformatted', FILE = 'spline.obs')
    write(10) arr
  CLOSE(unit = 10)
  print*, 'WRITTEN: spline.obs ',n,'rows for species'


end subroutine


subroutine readobs (n,arr)
  implicit NONE
  INTEGER, PARAMETER :: dp = SELECTED_REAL_KIND(14,300)
  integer n
  Real(dp),intent(out):: arr(n,27)

  OPEN(unit = 10, FORM = 'unformatted', FILE = 'spline.obs')
    read(10) arr
  CLOSE(unit = 10)



end subroutine
