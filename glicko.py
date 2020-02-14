import mpmath as mp
import numpy as np

## mpmath init
mp.dps = 15; mp.pretty = True

class Glicko:
    def __init__(self, a_tup = (1500, 350), b_tup = (1500, 350)):
        self.a_tup = a_tup
        self.b_tup = b_tup

    def RD_j(self):
        return {'a': (self.b_tup[1], self.a_tup[1]),
                'b': (self.a_tup[1], self.b_tup[1])}

    def g(self, RD):
        q = mp.fdiv(mp.log(10), 400)
        g_o = mp.fdiv(1, mp.sqrt(1 + mp.fdiv(3*(q**2)*(RD**2), mp.pi**2)))
        return g_o

    def exp_score(self):
        
        q = mp.fdiv(mp.log(10), 400)

        r_a = self.a_tup[0]
        RD_a = self.a_tup[1]
        r_b = self.b_tup[0]
        RD_b = self.b_tup[1]

        RD_norm = mp.sqrt(RD_a**2 + RD_b**2)
        g_a = self.g(RD_a)
        g_b = self.g(RD_b)
        delta_a = mp.fsub(r_a, r_b)
        delta_b = mp.fsub(r_b, r_a)
        exp_a = mp.fmul(-g_b, mp.fdiv(delta_a, 400))
        exp_b = mp.fmul(-g_a, mp.fdiv(delta_b, 400))

        E_a = mp.fdiv(1, 1 + mp.power(10, exp_a))
        E_b = mp.fdiv(1, 1 + mp.power(10, exp_b))
        
        return {'a': E_a, 'b': E_b}

    def d_sq(self, i):
        q = mp.fdiv(mp.log(10), 400)
        RD_j = self.RD_j()[i][0]
        E = self.exp_score()[i]
        d_sq = mp.fdiv(1, (q**2) * (self.g(RD_j)**2) * E * (1 - E))
        return d_sq

    def RD_new(self, i):
        RD_curr = self.RD_j()[i][1]
        RD_prime = mp.sqrt(mp.fdiv(1, mp.fdiv(1, RD_curr**2) + mp.fdiv(1, self.d_sq(i)**2)))
        return RD_prime


a = Glicko((1400, 350), (1500, 300))
print("d_sq", a.d_sq('a'), a.d_sq('b'))
print("RD_new", a.RD_new('a'), a.RD_new('b'))

