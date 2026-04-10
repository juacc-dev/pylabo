import logging

logger = logging.getLogger("pylabo.proc.maths")

def polynomial(x, *a):
    s = 0
    for n, a_n in enumerate(a):
        s += a_n * x ** n

    return s
