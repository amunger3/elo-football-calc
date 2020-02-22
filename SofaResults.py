from bs4 import BeautifulSoup
import urllib.request
import json

def team_info(lg3):
    lg_info = open('sofa_cfg.json', 'r')
    lg_json = json.load(lg_info)
    tminfo_dict = lg_json[lg3]
    return tminfo_dict


def fetch_json(api_endpoint):

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"

    req = urllib.request.Request(api_endpoint, headers = headers)
    json_response = urllib.request.urlopen(req).read()

    res_j = json.loads(json_response)

    return res_j

def get_round():
    json_season_url = "https://www.sofascore.com/u-tournament/17/season/23776/json"
    json_response = fetch_json(json_season_url)
    current_round = json_response['standingsTables'][0]['round']
    return current_round


def parse_json(api_round):

    tm_byid = team_info('epl')

    epl_19_20 = "https://www.sofascore.com/u-tournament/17/season/23776/matches/round/"
    round_num = [i+1 for i in range(38)]

    round_json = epl_19_20 + str(api_round)

    json_response = fetch_json(round_json)

    fixture_list = json_response['roundMatches']['tournaments'][0]['events']

    fix_res = []
    for event in fixture_list:
        roundInfo = event['roundInfo']
        winnerCode = event['winnerCode']
        
        if winnerCode != 0:
            homeTeam = event['homeTeam']
            awayTeam = event['awayTeam']

            home_n3 = tm_byid[str(homeTeam['id'])]['name3']
            away_n3 = tm_byid[str(awayTeam['id'])]['name3']

            codeTup = {1: (1, 0),
                       2: (0, 1),
                       3: (0.5, 0.5)}

            fix_res.append( ( ( home_n3 , away_n3 ) , codeTup[winnerCode] ) )
        

    return fix_res


def comb_all(season_round):

    master_list = []

    end_iter = [i+1 for i in range(season_round)]

    for r in end_iter:
        sub_list = parse_json(r)
        master_list = master_list + sub_list
        print("Round",r,"added.","(",len(sub_list),"games)")

    return master_list


