import mpmath as mp
import numpy as np
import requests

class EloRatings:
    def __init__(self, tm_A = {}, tm_b = {}):
        self.tm_A = tm_A
        self.tm_B = tm_B

    def getData(self):
        print("{0}+{1}j".format(self.real,self.imag))

# Create a new ComplexNumber object
c1 = ComplexNumber(2,3)

# Call getData() function
# Output: 2+3j
c1.getData()


print((c1.real, c1.imag))
