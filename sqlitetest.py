import sqlite3

db = sqlite3.connect("test.db")
db.row_factory = sqlite3.Row

cur = db.cursor()
cur.execute("select first, last, age from people")

table = "<table>"
table += "<tr><th>First</th><th>Last</th><th>Age</th></tr>"
for row in cur.fetchall():
     table += "<tr><td>" + row['first'] + "</td>"
     table += "<td>" + row['last'] + "</td>"
     table += "<td>" + str(row['age']) + "</td></tr>"

table += "</table>"
