import elo
import json
import mpmath
import SofaResults
import numpy as np
import matplotlib.pyplot as plt
import SofaResults


def init_dict():
    tminfo_dict = SofaResults.team_info()
    master_dict = {}
    for key, val in tminfo_dict.items():
        master_dict[val['name3']] = {'tm_id': key, 'name': val['name']}
        
    team_abbrs = ["ARS", "AVL", "BHA", "BOU", "BUR", "CHE", "CRY", "EVE",
                  "LEI", "LIV", "MCI", "MUN", "NEW", "NOR", "SHU", "SOU",
                  "TOT", "WAT", "WHU", "WOL"]

    for i in range(20):
        tm_id = i + 10
        master_dict[team_abbrs[i]].update({"ratings": [1500],
                                      "fixtures": [], "results": [],
                                      "elo_current": 1500})
    return master_dict


def build_ratings():
    master_dict = init_dict()
    round_num =SofaResults.get_round() 
    res_list = SofaResults.comb_all(round_num)

    for res in res_list:
        
        team_1 = res[0][0]
        team_2 = res[0][1]
        score_1 = res[1][0]
        score_2 = res[1][1]
        master_dict[team_1]['fixtures'].append(team_2)
        master_dict[team_1]['results'].append(score_1)
        master_dict[team_2]['fixtures'].append(team_1)
        master_dict[team_2]['results'].append(score_2)

        curr_elo_1 = master_dict[team_1]['elo_current']
        curr_elo_2 = master_dict[team_2]['elo_current']

        new_ratings = elo.up_rating(curr_elo_1, curr_elo_2, score_1, score_2)

        new_elo_1 = new_ratings[0]
        new_elo_2 = new_ratings[1]

        master_dict[team_1]['ratings'].append(new_elo_1)
        master_dict[team_1]['elo_current'] = new_elo_1
        master_dict[team_2]['ratings'].append(new_elo_2)
        master_dict[team_2]['elo_current'] = new_elo_2


    return master_dict


def print_desc():
    master_dict = build_ratings()
    sort_dict = {}
    sort_list = []

    for team in master_dict.keys():
        elo_curr = master_dict[team]['elo_current']
        matches = len(master_dict[team]['fixtures'])
        sort_dict[elo_curr] = (team, matches)
        sort_list.append(elo_curr)

    sort_list.sort(reverse = True)

    for i in range(20):
        rating = sort_list[i]
        print(i+1, sort_dict[rating], int(rating))

    return master_dict


def ratings_plot(team_list):
    master_dict = build_ratings()
    round_num = [i+1 for i in range(25)]

    for team in team_list:
        plt.plot(round_num, master_dict[team]['ratings'])

    plt.show()

    return

def exp_json():
    master_dict = build_ratings()
    
    for team in master_dict.keys():
        
        mean = mpmath.fdiv(sum(master_dict[team]['results']), len(master_dict[team]['results']))
        master_dict[team]['calc_stats'] = {'mean': float(mean)}

        chrono_rat = []
        for match in master_dict[team]['ratings']:
            chrono_rat.append(float(match))
        
        master_dict[team]['ratings'] = chrono_rat
        
        master_dict[team]['elo_current'] = float(master_dict[team]['elo_current'])
        
    jmd = json.dumps(master_dict)
    f = open("epl.json","w")
    f.write(jmd)
    f.close()
    
    return
        
    
exp_json()
