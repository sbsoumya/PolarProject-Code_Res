from sympy import *
import numpy as np
x=Symbol('x')
#y=x**2+1
#y.diff(x)

R=Symbol('R')
T=Symbol('T')
e=Symbol('e')
f=Symbol('f')
p=Symbol('p')
x=Symbol('x')
a=Symbol('a')
b=Symbol('b')
c=Symbol('c')
tpt=(R-T)*(1-f-(e-f)*(1-p)**T)/(2-(1-p)**T)
tpt2=(R-ln(x)/p)*(1-f-(e-f)*x)/(2-x)
print tpt2
tptprime=tpt.diff(T)
tpt2prime=tpt2.diff(x)
print tpt2prime
#tsoln=solve(tpt2prime,x)
form= f*(p*R*x+x**2-3*x+2)+(-f+2*e-1)*x*ln(x)-2*e*p*R*x+p*R*x-e*x**2+2*e*x+x-2
form2= x*a+b+c*x*ln(x)
tsoln=solve(form2,x)
print tsoln
