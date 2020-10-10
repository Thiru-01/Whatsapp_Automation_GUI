import json
from threading import Thread
import random
import time
import os
from tkinter.ttk import *
from tkinter import *
from googletrans import Translator
from ttkthemes import ThemedStyle
from tkinter import messagebox
import googletrans
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

root = Tk()
root.title("Whatsapp Automation")
root.geometry('800x600')
style = ThemedStyle(root)
style.set_theme("breeze")

textbox = Text(root, height=10, width=50)
textbox.insert(INSERT, 'None')
textbox.place(x=221, y=200)


def background_process_2(**data):
    thread_2 = Thread(target=Translation, daemon=True, args=(data,))
    return thread_2


def background_Process():
    return Thread(target=Whatsapp().Send_Msg, daemon=True)


def infoBox():
    messagebox.showinfo("showinfo", "Message Sent successfully")


def alertBox(msg):
    messagebox.showwarning("WARNING", str(msg))


class MainWindow:
    languages_set = StringVar()
    ConatctChossen = StringVar()
    Mess = StringVar()
    Buttonval = IntVar()
    count_num = IntVar()
    count_num.set(0)
    final_msg = []
    Flag = 0

    def __init__(self):

        self.languagesAvail = googletrans.LANGUAGES
        self.RandomCount = StringVar()
        self.Textbox = StringVar()
        self.Num = StringVar()
        self.val = Progressbar(root, length=200, orient='horizontal', mode='indeterminate')
        self.val.grid(row=1, column=1, padx=10, pady=5)

    def window(self):
        global ConatctChossen, Buttonval, count_num, Mess
        Mess = StringVar()
        count_num = IntVar()
        Buttonval = IntVar()
        Label(root, text="Enter the message :").grid(row=0, column=0,
                                                     padx=10,
                                                     pady=5, sticky=W)

        Entry(root, width=80, bg='white', textvariable=Mess).grid(row=0, column=1, padx=10,
                                                                  pady=5, ipady=4)

        Label(root, text="Select the contact name :").grid(row=1, column=0,
                                                           padx=10,
                                                           pady=5, sticky=W)
        # CONATCT
        values1 = []
        with open("Contact.json", 'r') as file:
            Contact = json.load(file)
            for i, j in Contact.items():
                values1.append(i)
        ConatctChossen = Combobox(root, width=20, height=15)
        ConatctChossen['values'] = values1
        ConatctChossen.place(x=350, y=38, anchor=NE)

        Label(root, text="Give count :").grid(row=3, column=0, padx=10, pady=5, sticky=W, ipady=15)
        Scale(root, from_=1, to=1000, orient=HORIZONTAL, variable=count_num, troughcolor='#7EB8FE', width=5,
              length=200,
              tickinterval=0.25, sliderlength=10).grid(row=3, column=1, padx=10, pady=5, sticky=NW)
        Radiobutton(root, text="Random language", value=1, variable=Buttonval, command=self.check).place(x=367,
                                                                                                         y=150,
                                                                                                         anchor=NE)
        Radiobutton(root, text="Selected language", value=2, variable=Buttonval, command=self.check).place(x=530,
                                                                                                           y=150,
                                                                                                           anchor=NE)

        Button(root, text="Translate",
               command=lambda: [background_process_2(Message=Mess.get(), Button=Buttonval.get(),
                                                     RandomCount=self.RandomCount.get(),
                                                     final_msg=self.final_msg,
                                                     single_msg=Mess).start()]).place(
            x=650,
            y=520,
            anchor=NE)
        Button(root, text="Send", command=lambda: [background_Process().start()]).place(x=740, y=520, anchor=NE)
        Button(root, text="Close", command=lambda: [exit(1)]).place(x=540, y=520, anchor=NE)

    def check(self):
        global Flag
        state = Buttonval.get()
        if state == 1:
            Flag = 1
            self.enteryRandomcount()
        elif state == 2:
            Flag = 2
            self.Combobox_language()

    def enteryRandomcount(self):
        Randomentery = Spinbox(root, from_=1, to=100, textvariable=self.RandomCount, width=16)
        Randomentery.place(x=553, height=28, y=152, )

    @staticmethod
    def Combobox_language():
        values = []

        with open("lang.json", 'r') as file:
            langdoc = json.load(file)
            for i, j in langdoc.items():
                values.append(j)
        languages_set = Combobox(root, textvariable=MainWindow.languages_set, width=15, height=15)
        languages_set['values'] = values
        languages_set.current(21)
        languages_set.place(x=680, y=150, anchor=NE)


class Whatsapp(MainWindow):
    def __init__(self):
        super().__init__()
        self.Url = "https://web.whatsapp.com/"
        try:
            self.Driver = r"Path to chromedriver.exe"
        except Exception as e:
            raise e
        self.Options = webdriver.ChromeOptions()
        if os.path.isdir(os.getcwd() + r'\\Web_Data'):
            if not os.listdir(r'Web_Data\\'):
                self.Options.add_argument(r'--user-data-dir=' + os.getcwd() + r'\\Web_Data\\')
            self.Options.add_argument(r'--user-data-dir=' + os.getcwd() + r'\\Web_Data\\')
            pass
        else:
            os.makedirs(os.getcwd() + r"\\Web_Data")
            self.Options.add_argument(r'--user-data-dir=' + os.getcwd() + r'\\Web_Data\\')

    def Send_Msg(self):


        global input_box
        try:
            flag = Flag
        except NameError:
            flag = 0
            pass
        Count = count_num.get()
        Name = ConatctChossen.get()
        mess = Mess.get()
        finalMess = self.final_msg
        ProgressBar = self.val
        navigator = webdriver.Chrome(executable_path=self.Driver, options=self.Options)
        wait = WebDriverWait(navigator, 60)
        navigator.get(self.Url)
        count_v = 1 if Count == 0 else Count
        ct = 0
        while ct != 5:
            try:
                input_ = wait.until((EC.element_to_be_clickable((By.XPATH, "//div[@class='_3FRCZ copyable-text selectable-text']"))))
                input_.clear()
                input_.send_keys(Name)
                time.sleep(1)
                input_.send_keys(Keys.ENTER)
                time.sleep(2)
                inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'  # "//div[@contenteditable='true']"
                input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
                break
            except Exception as e:
                print(e)
                ct += 1
                break

        ProgressBar.start(5)
        if flag == 1:
            for x in range(count_v):
                for data in finalMess:
                    input_box.send_keys(data + Keys.ENTER)
                    input_box.send_keys("\n" + Keys.ENTER)
                    time.sleep(1)
            ProgressBar.stop()

        elif flag == 2:
            for x in range(count_v):
                input_box.send_keys(finalMess[0] + Keys.ENTER)
                time.sleep(1)
                input_box.send_keys("\n")
            ProgressBar.stop()

        else:
            for x in range(count_v):
                input_box.send_keys(mess[0] + Keys.ENTER)
                time.sleep(1)
                input_box.send_keys("\n")
            ProgressBar.stop()

        infoBox()
        navigator.__exit__()


class Translation(MainWindow):

    def __init__(self, Data):
        super().__init__()

        self.Buttonval = Data["Button"]
        self.RandomCount = Data["RandomCount"]
        self.final_msg = Data["final_msg"]
        self.ProgressBar = self.val
        self.textbox = textbox
        self.base_word = Data["Message"]
        self.single_language = self.languages_set
        self.translate()

    def translate(self):
        self.textbox.delete(1.0, END)
        translate = Translator()
        if self.Buttonval == 1:
            self.ProgressBar.start(10)
            self.final_msg.clear()
            with open("lang.json") as file:

                languages = json.load(file)
                language_des = random.sample(list(languages.items()), k=int(self.RandomCount))
            for lan, language_name in language_des:
                try:
                    translated_word = translate.translate(self.base_word, dest=lan)
                    self.textbox.insert(INSERT, "{}\n".format(translated_word.text))
                    self.final_msg.append(translated_word.text)

                except Exception:
                    alertBox("Check your Internet Connection and try again")
                    exit()
            self.ProgressBar.stop()
        elif self.Buttonval == 2:
            self.ProgressBar.start(10)
            self.final_msg.clear()
            try:

                translated_word = translate.translate(self.base_word, dest=self.single_language.get())
                self.textbox.insert(INSERT, "{}\n".format(translated_word.text))
                self.final_msg.append(translated_word.text)

            except Exception as e:
                alertBox(e)
                exit()
            self.ProgressBar.stop()


if os.path.isfile('Contact.json'):
    if os.path.isfile("lang.json"):
        MainWindow().window()
    else:
        languagesAvail = googletrans.LANGUAGES
        json_object = json.dumps(languagesAvail, indent=4)
        with open("lang.json", 'w') as file:
            file.write(json_object)
        MainWindow().window()
        pass
else:
    import Contact_json

root.mainloop()
