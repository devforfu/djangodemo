import os

import MySQLdb
import pandas as pd


db = MySQLdb.connect(host='localhost', user='root',
                     passwd='reverse', db='welcome')
cursor = db.cursor()

for table in ('accounts', 'tickets', 'messages'):
    path = os.path.join('tables', table + '.csv')
    df = pd.read_csv(path, parse_dates=True)
    columns = ", ".join(list(df.columns))

    for _, row in df.iterrows():
        strings = [str(v) if type(v) == int else "'{}'".format(v)
                   for v in row.values]
        values = ["STR_TO_DATE({}, '%m/%d/%Y')".format(s) if '/' in s else s
                  for s in strings]

        query = ("INSERT INTO {} ({}) VALUES ({})"
                 .format(table, columns, ", ".join(values)))

        cursor.execute(query)

db.commit()
db.close()
