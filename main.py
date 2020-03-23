import numpy as np
import pandas as pd
import mpmath as mp
from matplotlib import pyplot
from dfMake import LgDF


class MainApp():

    def __init__(self, refresh = True):

        if refresh:

            # Create storage object with filename `processed_data`
            self.data_store = pd.HDFStore('processed_data.h5')

            self.EPL_Lg = LgDF('epl')
            fetch_rem = self.EPL_Lg.build_ratings()
            npEPL = self.EPL_Lg.ratings_frame(fetch_rem)

            col_tm = ['id', 'name', 'abbr']
            col_matches = [i for i in range(len(npEPL[0]) - 3)]
            cols = col_tm + col_matches
            self.mainframe = pd.DataFrame(npEPL, columns = cols)
            self.mainframe.set_index('id')

            # Put DataFrame into the object setting the key as 'preprocessed_df'
            self.data_store['preprocessed_df'] = self.mainframe
            self.data_store.close()

        else:

            # Access data store
            data_store = pd.HDFStore('processed_data.h5')

            # Retrieve data using key
            self.mainframe = data_store['preprocessed_df']
            data_store.close()


    def get_df(self):

        return self.mainframe

    
    def write_html(self):

        self.mainframe.to_html('index.html', classes=['uk-table'], table_id='epl-main', float_format='{0:.1f}'.format)



if __name__ == '__main__':
    dfApp = MainApp(refresh = False)
    dfApp.write_html()
    DatFr = dfApp.get_df()



