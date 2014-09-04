from random import randint

def d6( x=1 ):
    total = 0
    for i in range(0,x):
        total = total + randint(1,6)
    return total

def d66():
    return d6() * 10 + d6();

def d6s( x=1 ):
    rolls = []
    for i in range(0,x):
        rolls.append( randint(1,6) )
    return rolls
