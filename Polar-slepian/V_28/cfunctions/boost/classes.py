import classes
t = classes.World()
t.set("bom dia!")
print (t.greet())

t.many(['Good Morning', 'Buon giorno', 'Kali mera'])
print (t.greet())

t.setvector([1,0,1,1,0,0,1])
print (t.getvector())

