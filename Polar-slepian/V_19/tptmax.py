from sympy import *
import numpy as np
x=Symbol('x')
#y=x**2+1
#y.diff(x)

R=Symbol('R')
T=Symbol('T')
F1=Symbol('F1')
F2=Symbol('F2')
p=Symbol('p')
x=Symbol('x')
pc=Symbol('pc')
tpt=(R-T)*(1-F2-(F1-F2)*(1-p)**T)/(2-(1-p)**T)
tpt2=(R-ln(x)/pc)*(1-F2-(F1-F2)*x)/(2-x)
print tpt2
tptprime=tpt.diff(T)
tpt2prime=tpt2.diff(x)
print tpt2prime
#tsoln=solve(tpt2prime,x)
tsoln=solve(x*ln(x),x)
print tsoln
