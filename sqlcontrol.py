import sqlite3
dbfile = sqlite3.connect('schedule.db')

c = dbfile.cursor()

# テーブルの作成
c.execute("create table cl_table(YYYYMMDD, HHMMSS, memo)")

c.execute("INSERT INTO cl_table VALUES ('2020-09-15','08:00','会議')")

dbfile.commit()
dbfile.close()