import sqlite3
import SofaResults


def db_init():
    db = sqlite3.connect("epl_elo.sqlite")

    db.execute('''CREATE TABLE IF NOT EXISTS team_ids
             (sofa_id INT PRIMARY KEY     NOT NULL,
             full_name      TEXT    NOT NULL,
             abbr_name         TEXT     NOT NULL);''')

    tm_dict = SofaResults.team_info()

    for team in tm_dict.keys():
        query_build = "INSERT INTO team_ids VALUES("+str(team)+","+tm_dict[team]['name']+","+tm_dict[team]['name3']+");"
        db.execute(query_build)

    return
