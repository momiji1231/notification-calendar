# -*- coding:utf-8 -*-

import schedule
import time
import tkinter as tk
import datetime
import sqlite3

def job():
    dbfile = sqlite3.connect('schedule.db')
    sql = dbfile.cursor()

    now = datetime.datetime.now()
    print("now = {}".format(now))

    if now.month <= 9:
        month = "0{}".format(now.month)
    else:
        month = now.month

    if now.day <= 9:
        day = "0{}".format(now.day)
    else:
        day = now.day

    YYYYMMDD = "{}-{}-{}".format(now.year, month, day)

    if now.hour <= 9:
        hour = "0{}".format(now.hour)
    else:
        hour = now.hour

    if now.minute <= 9:
        minute = "0{}".format(now.hour)
    else:
        minute = now.minute

    time = "{}:{}".format(hour, minute)

    sql.execute("select * from cl_table where YYYYMMDD = ? and HHMMSS = ? ", (YYYYMMDD,time, ))
    print("select * from cl_table where YYYYMMDD = {} and HHMMSS = {} ORDER BY HHMMSS ASC".format(YYYYMMDD,time ))
    list = sql.fetchall()
    print(len(list))

    root = tk.Tk()
    root.title("通知")
    root.geometry("500x500")
    i = 0
    if not len(list) == 0:
        for out in list:
            ddmm = tk.Label(root, text="{}  {}  の時間です".format(out[1],out[2]))
            ddmm.place(x=180, y=i)
            i = i + 20
        root.mainloop()
    else:
        root.destroy()

schedule.every(30/60).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
