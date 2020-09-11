# -*- coding:utf-8 -*-

import tkinter as tk
import datetime
import re
import sqlite3


class mycalendar(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        now = datetime.datetime.now()

        self.year = now.year
        self.month = now.month
        self.today = now.day
        global YEAR, MONTH
        YEAR = str(self.year)
        MONTH = str(self.month)

        frame_top = tk.Frame(self)
        frame_top.pack(pady=5)

        self.current_year = tk.Label(frame_top, text="{}年".format(self.year), font=("", 18))
        self.current_year.pack(side="left")
        self.current_month = tk.Label(frame_top, text="{}月".format(self.month), font=("", 18))
        self.current_month.pack(side="left")

        frame_week = tk.Frame(self)
        frame_week.pack()
        button_mon = d_button(frame_week, text="月")
        button_mon.grid(column=0, row=0)
        button_tue = d_button(frame_week, text="火")
        button_tue.grid(column=1, row=0)
        button_wed = d_button(frame_week, text="水")
        button_wed.grid(column=2, row=0)
        button_thu = d_button(frame_week, text="木")
        button_thu.grid(column=3, row=0)
        button_fri = d_button(frame_week, text="金")
        button_fri.grid(column=4, row=0)
        button_sta = d_button(frame_week, text="土", fg="blue")
        button_sta.grid(column=5, row=0)
        button_san = d_button(frame_week, text="日", fg="red")
        button_san.grid(column=6, row=0)

        self.frame_calendar = tk.Frame(self)
        self.frame_calendar.pack()

        self.create_calendar(self.year, self.month)

    def create_calendar(self, year, month):

        try:
            for key, item in self.day.items():
                item.destroy()
        except:
            pass

        import calendar
        cal = calendar.Calendar()
        days = cal.monthdayscalendar(year, month)

        self.day = {}
        for i in range(0, 42):
            c = i - (7 * int(i / 7))
            r = int(i / 7)
            try:
                if days[r][c] != 0:
                    if days[r][c] == self.today:
                        self.day[i] = d_button(self.frame_calendar, text=days[r][c], fg="magenta")
                    else:
                        self.day[i] = d_button(self.frame_calendar, text=days[r][c])
                    self.day[i].grid(column=c, row=r)
                    self.day[i].bind("<ButtonPress>", self.createNewWindow)
            except:
                """
                月によっては、i=41まで日付がないため、日付がないiのエラー回避が必要
                """
                break

    def change_month(self, event):
        if event.widget["text"] == "<":
            self.month -= 1
        else:
            self.month += 1
        if self.month == 0:
            self.year -= 1
            self.month = 12
        elif self.month == 13:
            self.year += 1
            self.month = 1
        self.current_year["text"] = self.year
        self.current_month["text"] = self.month
        self.create_calendar(self.year, self.month)

    def createNewWindow(self,event):
        self.newWindow = tk.Toplevel(root)
        self.app = Win2(self.newWindow,event)

class d_button(tk.Button):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Button.__init__(self, master, cnf, **kw)
        self.configure(font=("", 14), height=2, width=4, relief="flat")

class Win2(tk.Frame):
    def __init__(self,master,event):
        super().__init__(master)
        self.pack()
        self.master.geometry("500x500")
        self.master.title("{}日".format(event.widget["text"]))
        self.day = event.widget["text"]
        self.today_schedule()
        self.create_text()
        self.create_addbtn()
        self.create_delbtn()
        self.create_clsbtn()

    def today_schedule(self):
        now = datetime.datetime.now()
        self.year = now.year
        self.month = now.month if len(str(now.month)) == 2 else "0{}".format(now.month)
        self.yymmdd = "{}-{}-{}".format(self.year, self.month, self.day)
        self.dbfile = sqlite3.connect('schedule.db')
        self.sql = self.dbfile.cursor()
        self.sql.execute("select * from cl_table where YYYYMMDD = ? ORDER BY HHMMSS ASC", (self.yymmdd, ))
        list = self.sql.fetchall()
        i = 0
        self.list_chk = []
        self.list_time = []
        self.list_memo = []
        bln = tk.BooleanVar()
        bln.set(False)
        if not len(list) == 0:
            for out in list:
                self.ddmm = tk.Checkbutton(self.master, text="{}  {}".format(out[1],out[2]), variable=bln)
                self.list_chk.append(bln)
                self.ddmm.place(x=180, y=i)
                i = i + 20
                self.list_time.append(out[1])
                self.list_memo.append(out[2])
        else:
            self.notinfo = tk.Label(self.master, text="今日の予定はありません")
            self.notinfo.pack()

    def create_text(self):
        self.time_label = tk.Label(self.master, text="時刻")
        self.time_input = tk.Entry(self.master, width=20)
        self.schedule_label = tk.Label(self.master, text="予定")
        self.schedule_input = tk.Entry(self.master, width=40)
        self.time_label.place(x=50, y=250)
        self.time_input.place(x=100, y=250)
        self.schedule_label.place(x=50, y=300)
        self.schedule_input.place(x=100, y=300)

    def create_addbtn(self):
        self.button_commit = tk.Button(self.master, text="登録", fg="green", command=self.schedule_adding)
        self.button_commit.place(x=420, y=450)

    def schedule_adding(self):
        self.time = self.time_input.get()
        self.memo = self.schedule_input.get()
        self.result = self.time_invalid()
        self.msg_label = tk.Label(self.master, text="                                                                 ")
        self.msg_label.place(x=200, y=350)

        if self.result and not len(self.memo) == 0:
            self.sql.execute("INSERT INTO cl_table VALUES (?,?,?)",[self.yymmdd, self.time, self.memo])
            self.dbfile.commit()
            self.msg_label = tk.Label(self.master, text="予定が登録されました", fg="green")
            self.msg_label.place(x=150, y=350)
        else:
            self.worning_message()

    def time_invalid(self):
        if re.fullmatch(r'\d{2}:\d{2}', self.time):
            return True
        else:
            return False

    def worning_message(self):
        if self.result:
            self.msg_label = tk.Label(self.master, text="予定を入力してください", fg="red")
        else:
            self.msg_label = tk.Label(self.master, text="時刻は 「XX:XX」の形式で入力してください", fg="red")
        self.msg_label.place(x=150, y=350)

    def create_delbtn(self):
        # Button
        self.button_quit = tk.Button(self.master, text="削除", command=self.schedule_deleting, fg="red")
        self.button_quit.place(x=290, y=450)

    def schedule_deleting(self):
        self.delete_tergets = self.list_chk
        self.delete_times = self.list_time
        self.delete_memos = self.list_memo
        self.msg_label = tk.Label(self.master, text="                                                                 ")
        self.msg_label.place(x=200, y=350)
        i = 0
        for terget, time, memo in zip(self.delete_tergets, self.delete_times, self.delete_memos):
            if terget.get() == True:
                self.sql.execute("delete from cl_table where YYYYMMDD = ? and HHMMSS = ? and memo = ?",(self.yymmdd, time, memo))
                i = i + 1
                self.dbfile.commit()
            else:
                continue
        else:
            if i == 0:
                self.msg_label = tk.Label(self.master, text="削除したい予定にチェックを入れてください", fg="red")
            else:
                self.msg_label = tk.Label(self.master, text="削除が完了しました", fg="green")
            self.msg_label.place(x=150, y=350)

    def create_clsbtn(self):
        self.button_quit = tk.Button(self.master, text="閉じる", command=self.quit_window)
        self.button_quit.place(x=350, y=450)

    def quit_window(self):
        self.master.destroy()

root = tk.Tk()
root.title("カレンダー")
mycal = mycalendar(root)
mycal.pack()
root.mainloop()