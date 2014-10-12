import math
import sys
def check(x, guess):
    return (abs(guess*guess - x) < 0.001)

def newton(x, guess):
    while not check(x, guess):
        guess = (guess + (x/guess)) / 2.0
    return guess

while(True):
	r = newton(sys.maxint, 1)
