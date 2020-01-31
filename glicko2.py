from mpmath import *

## mpmath init
mp.dps = 15; mp.pretty = True

def init_params():
    elo_r = 1500
    RD = 350
    sigma = 0.06
    conv_factor = 173.7178
    return [elo_r, RD, sigma, conv_factor]

def conv_params(init_list):
    cf = init_list[3]
    mu = fdiv((init_list[0] - 1500), cf)
    phi = fdiv(init_list[1], cf)
    return (mu, phi)

def g(phi):
    fdiv(1, sqrt(1 + 3*(phi**2 / pi**2)))


