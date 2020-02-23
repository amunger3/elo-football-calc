import epl
import SofaResults
import csv

def csv_view(view_type):
    master_dict = epl.build_ratings()
    views = {'ratings': 0, 'fixtures': 1, 'results': 2}
    if view_type not in views.keys():
        print("invalid view_type input")
        return
    

    file_name = view_type + '.csv'
    with open(file_name, "w") as f:
        writer = csv.writer(f)

        for team in master_dict.keys():
            tm_row = [team] + master_dict[team][view_type]
            writer.writerow(tm_row)
        f.close()
