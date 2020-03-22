from SofaResults import SofaSeason
import elo
import mpmath as mp
import numpy as np
import pandas as pd


class LgDF:
    def __init__(self, league):
        self.league = SofaSeason(league)
        self.round_num = self.league.get_round()
        self.tminfo_dict = self.league.team_info()[1]

    def init_dict(self):
        sofa_lg = self.league
        tminfo_dict = self.tminfo_dict
        df_dict = {}
        for team_id in tminfo_dict.keys():
            df_dict[team_id] = {"ratings": [
                1500], "fixtures": [], "results": [], "elo_current": 1500}
        return df_dict

    def name_id_map(self):
        sofa_lg = self.league
        tminfo_dict = sofa_lg.team_info()[1]
        nmid_map = {}
        for team_id, data_dict in tminfo_dict.items():
            nmid_map[data_dict['name3']] = team_id
        return nmid_map

    def build_ratings(self):
        sofa_lg = self.league
        df_dict = self.init_dict()
        nmid_map = self.name_id_map()
        res_list = sofa_lg.comb_all()

        for res in res_list:
            team_1 = res[0][0]
            team_2 = res[0][1]
            score_1 = res[1][0]
            score_2 = res[1][1]
            id_1 = nmid_map[team_1]
            id_2 = nmid_map[team_2]

            df_dict[id_1]['fixtures'].append(id_2)
            df_dict[id_1]['results'].append(score_1)
            df_dict[id_2]['fixtures'].append(id_1)
            df_dict[id_2]['results'].append(score_2)

            cElo_1 = df_dict[id_1]['elo_current']
            cElo_2 = df_dict[id_2]['elo_current']

            nElos = elo.up_rating(cElo_1, cElo_2, score_1, score_2)

            nElo_1 = nElos[0]
            nElo_2 = nElos[1]

            df_dict[id_1]['ratings'].append(nElo_1)
            df_dict[id_1]['elo_current'] = nElo_1
            df_dict[id_2]['ratings'].append(nElo_2)
            df_dict[id_2]['elo_current'] = nElo_2

        return df_dict

    def agg_stats(self, df_comp):

        for team in df_comp.keys():
            mean = mp.fdiv(sum(df_comp[team]['results']), len(
                df_comp[team]['results']))
            df_comp[team]['calc_stats'] = {'mean': mean}

        return

    def df_ready(self):
        df_dict = self.build_ratings()
        df_agg = self.agg_stats(df_dict)
        return df_agg

    def ratings_frame(self, df_ratings):
        tminfo_dict = self.tminfo_dict
        # df_ratings = self.build_ratings()
        num_ratings = self.round_num + 1
        team_list = []
        ratings_nest = []
        for team, data in df_ratings.items():
            team_list.append(team)
            if len(data['ratings']) < num_ratings:
                for i in range(num_ratings - len(data['ratings'])):
                    data['ratings'].append(None)
            print(team, len(data['ratings']))
            ratings_nest.append(data['ratings'])
        rounds = [i for i in range(num_ratings)]
        TeamInfo = []
        for tm in team_list:
            tiSingle = [tm, tminfo_dict[tm]['name'], tminfo_dict[tm]['name3']]
            TeamInfo.append(tiSingle)
        tm_heads = ['id', 'name', 'abbr']
        TMi = pd.DataFrame(TeamInfo, columns=tm_heads)
        DFr = pd.DataFrame(ratings_nest, columns=rounds)
        nph = np.hstack((TMi, DFr))
        return nph


#e2 = LgDF('epl')
#e2.ratings_frame()
