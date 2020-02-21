import mpmath as mp
import numpy as np

mp.dps = 15
mp.pretty = True


class Elo:
    def __init__(self, A={'elo_current': 1500, 'score': 0.5}, B={'elo_current': 1500, 'score': 0.5}):
        self.R_a = A['elo_current']
        self.R_b = B['elo_current']
        self.S_a = A['score']
        self.S_b = B['score']

    def exp_score(self):
        R_a = self.R_a
        R_b = self.R_b
        Q_a = mp.power(10, (R_a/400))
        Q_b = mp.power(10, (R_b/400))
        E_a = mp.fdiv(Q_a, mp.fadd(Q_a, Q_b))
        E_b = mp.fdiv(Q_b, mp.fadd(Q_a, Q_b))
        print(E_a, E_b)
        return (E_a, E_b)

    def up_rating(self):
        K = 32
        E_scores = self.exp_score()
        E_a = E_scores[0]
        E_b = E_scores[1]
        Rnew_a = self.R_a + K*(self.S_a - E_a)
        Rnew_b = self.R_b + K*(self.S_b - E_b)
        print(Rnew_a, Rnew_b)
        return (Rnew_a, Rnew_b)


# Create a new Elo object
c1 = Elo({'elo_current': 1600, 'score': 0.5},
         {'elo_current': 1400, 'score': 0.5})

c1.exp_score()
c1.up_rating()
