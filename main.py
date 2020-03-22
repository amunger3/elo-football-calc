import numpy as np
import pandas as pd
import mpmath as mp
from matplotlib import pyplot
from dfMake import LgDF

def run():
    EPL_Lg = LgDF('epl')
    fetch_rem = EPL_Lg.build_ratings()
    npEPL = EPL_Lg.ratings_frame(fetch_rem)
    col_tm = ['id', 'name', 'abbr']
    col_matches = [i for i in range(len(npEPL[0]) - 3)]
    cols = col_tm + col_matches
    mainframe = pd.DataFrame(npEPL, columns = cols)
    mainframe.set_index('id')
    return mainframe
