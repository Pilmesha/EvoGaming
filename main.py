import io
import re
import time
import calendar
import datetime
import numpy as np
import pandas as pd
import tkinter as tk
import seaborn as sns
from tkinter import ttk
from io import StringIO
import matplotlib_inline
from datetime import date
import matplotlib.pyplot as plt
import undetected_chromedriver as udc
from tkinter.messagebox import showerror
from tkcalendar import Calendar, DateEntry
from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta
from sklearn.linear_model import LinearRegression

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500")
        self.frame = tk.Frame(master=self.root, bg='#63d0ff', width=800, height=500)
        self.frame.pack()
        self.play_lbl = tk.Label(self.frame, text="Welcome to Evolution Data Analizer! ", fg='#33004f', bg='#63d0ff', font=("Arial Bold", 25)).place(x=130,y=100)
        self.username_txtbox = tk.Entry(self.frame, width=30)
        self.username_txtbox.place(x=200,y=180)
        self.username_login = tk.Label(self.frame, text='Enter your login', font=("Arial Bold", 10),bg='#63d0ff' ).place(x=370, y=180)
        self.password_txtbox = tk.Entry(self.frame, width=30, show='*')
        self.password_txtbox.place(x=200,y=210)
        self.password_login = tk.Label(self.frame, text='Enter your password', font=("Arial Bold", 10), bg='#63d0ff').place(x=370, y=210)
        self.login_butt = tk.Button(
            master = self.frame,
            text = 'Login',
            width = 15,
            height=1,
            command=self.get_data,
            font = ('Arial', 15)
        ).place(x=370,y=240)
        self.okta_butt = tk.Button(
            master=self.frame,
            text = 'Okta Login',
            width = 15,
            height=1,
            command= self.get_data_okta,
            font=('Arial', 15)
        ).place(x=370, y=280)
    def clearscreen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def newscreen(self):
        self.anallab = tk.Label(master = self.frame,text='Choose data and type to analyze', fg='#33004f',bg='#63d0ff' , font=("Arial Bold", 22)).place(x=130,y=100)
        self.choosedata = ttk.Combobox(master = self.frame, width=20, state='readonly')
        df = pd.read_csv('my_file.csv')
        self.data_clean(df)
        self.choosedata['values'] =df['Game and metric'].tolist()
        self.choosedata.place(x=150,y=150)
        self.choosanalize = ttk.Combobox(master=self.frame, width=20, state='readonly')
        self.choosanalize['values'] = ['Linear Regression', 'Diagrams', 'Prediction']
        self.choosanalize.place(x=150,y=180)
        self.choosanalize.bind('<<ComboboxSelected>>', self.addInfo)
        self.analizeButt = tk.Button(
            master = self.frame,
            text='Analize',
            width=15,
            height=1,
            command=self.analize,
            font=("Arial", 15)
        ).place(x=340, y=165)
    def addInfo(self, event = None):
        selection = self.choosanalize.get()
        dt1 = date.today()
        dt2 = dt1 + relativedelta(day=31)
        self.cal = (DateEntry(self.frame, width=20, background='darkblue', foreground='white', borderwidth=2,
                         mindate=dt1, maxdate=dt2))
        if selection == 'Prediction':
            self.cal.place(x=150,y=210)
    def get_data(self, event=None):
        #--authentification--
        username = self.username_txtbox.get()
        password = self.password_txtbox.get()

        #self.clearscreen()
        #self.newscreen()
        #username = 'nianozadze7@gmail.com'
        #password = '@Phokuznikaa1'
        #--connecting to chrome--
        chromeOptions = udc.ChromeOptions()
        chromeOptions.add_argument("--headless=new")
        driver = udc.Chrome(use_subprocess=True, options=chromeOptions)
        driver.get("https://helpdesk.evolutiongaming.com/user/login")
        #--passing an username--
        uname = driver.find_element(By.ID, "username")
        uname.send_keys(username)
        #--passing password--
        passwordF = driver.find_element(By.ID, "password")
        passwordF.send_keys(password)
        #--logging in--
        driver.find_element(By.NAME, "login-button").click()
        time.sleep(2)
        driver.get("https://helpdesk.evolutiongaming.com/gameMetric/personalList")
        driver.find_element(By.CLASS_NAME, 'icon-previous').click()
        #--converting data to csv--
        self.df = pd.read_html(io.StringIO(driver.find_element(By.ID, "mainBody").get_attribute("outerHTML")))
        self.df[0].to_csv('my_file.csv', index=False)
        print("Login successfull") #print statement
        driver.close() # closing operation
        self.clearscreen()
        self.newscreen()
    def get_data_okta(self, event=None):
        # --authentification--
        username = self.username_txtbox.get()
        password = self.password_txtbox.get()
        # --connecting to chrome--
        chromeOptions = udc.ChromeOptions()
        chromeOptions.add_argument("--headless=new")
        driver = udc.Chrome(use_subprocess=True, options=chromeOptions)
        driver.get("https://helpdesk.evolutiongaming.com/user/login")

        driver.find_element(By.XPATH,"//div[@class = 'd-grid'][2]").click()
        time.sleep(3)
        print('Success with okta redir')
        #--passing email--
        uname = driver.find_element(By.ID, 'input43')
        uname.send_keys(username)
        driver.find_element(By.CLASS_NAME, 'o-form-button-bar').click()
        time.sleep(5)
        print('Success with sending username')
        #--passing password--
        driver.find_element(By.XPATH, "//div[@class='authenticator-button'][@data-se = 'okta_password']").click()
        print('Success with entering password page')
        time.sleep(2)
        passwordF = (driver.find_element(By.ID, 'input103'))
        passwordF.click()
        passwordF.send_keys(password)
        print('Success with sending password')
        driver.find_element(By.CLASS_NAME, 'o-form-button-bar').click()
        time.sleep(2)
        driver.get("https://helpdesk.evolutiongaming.com/gameMetric/personalList")
        # --converting data to csv--
        df = pd.read_html(driver.find_element(By.ID, "mainBody").get_attribute("outerHTML"))
        df[0].to_csv('my_file.csv', index=False)

        print("Login successfull")  # print statement
        driver.close()  # closing operation
        self.clearscreen()
        self.newscreen()


    def data_clean(self,datafr):
        datafr.pop('Month')
        datafr.drop_duplicates(inplace=True)
        for x in datafr.keys():
            if datafr[x].isnull().all():
                datafr.pop(x)
        for i in datafr.keys():
            datafr[i] = datafr[i].astype(str).str.rstrip("%")

        datafr[datafr.columns[1::]] = datafr[datafr.columns[1::]].astype(float)
    def getIndex(self, datafr, key):
        return np.where(datafr['Game and metric'] == key)[-1][-1]
    def anal_data(self, datafr, searchval):
        return pd.DataFrame(
            {'Month': datafr.columns[1::].astype(int),
             searchval: datafr.values[self.getIndex(datafr,searchval)][1::].astype(float)})
    def analize(self, event=None):
        df = pd.read_csv('my_file.csv')
        self.data_clean(df)
        match self.choosanalize.get():
            case 'Linear Regression':
                sns.regplot(x = 'Month', y = self.choosedata.get(), data= self.anal_data(df, self.choosedata.get()))
                plt.show()
            case 'Diagrams':
                x_axis = self.anal_data(df, self.choosedata.get())['Month']
                y_axis = self.anal_data(df, self.choosedata.get())[self.choosedata.get()]
                plt.bar(x_axis, y_axis)
                plt.show()
            case 'Prediction':
                print(self.cal.get_date().day)
                linreg = LinearRegression()
                linreg.fit(self.anal_data(df, self.choosedata.get())['Month'], self.anal_data(df, self.choosedata.get())[self.choosedata.get()])
                print(linreg.predict([[self.cal.get_date().day]]))


if __name__ == '__main__':
    window = tk.Tk(className=" Your Bitch")
    App = GUI(window)
    window.mainloop()



