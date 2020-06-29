import tkinter as tk
import tkinter.filedialog as fl
import tkinter.messagebox as mb
from time import sleep
from PIL import Image ,ImageTk
import time
import speech_recognition as sr

global list_y
global memo_y
global num_list
global num_time
global flag
list_y = 10
memo_y = 10
num_list = []
num_time = []
flag = 0

class Timer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.label = tk.Label(self, text="", width=20)
        self.label.place(x=40,y=40)
        self.label.pack()

    def count_step(self,time):
        self.remaining = 0
        self.countdown(time)

    def countdown(self, remaining = None):

        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="Time's Up!")
           
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)
        
def flag_count():
    global flag
    flag = 1
    task_voice

def task_voice(event):
    global list_y
    global num_list
    global num_time
    global flag

    r = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            r.adjust_for_ambient_noise(source) #雑音対策
            audio = r.listen(source)
        try:
            if r.recognize_google(audio, language='ja-JP') != "ストップ":
                if flag == 0:
                    num_list.append(r.recognize_google(audio, language='ja-JP'))
                    txt = tk.Entry(width = 23)
                    txt.insert(tk.END,r.recognize_google(audio, language='ja-JP'))
                    txt.place(x = 20,y = (180 + list_y))
    
                    flag_count()
                elif flag == 1:
                    num_time.append(int(r.recognize_google(audio, language='ja-JP')))
                    txt = tk.Entry(width = 15)
                    txt.insert(tk.END,r.recognize_google(audio, language='ja-JP'))
                    txt.place(x = 500,y = (180 + list_y))   
                    flag = 0
                    list_y += 20
                    break
                                  
            print(r.recognize_google(audio, language='ja-JP'))
            
            # "ストップ" と言ったら音声認識を止める
            if r.recognize_google(audio, language='ja-JP') == "ストップ":
                flag = 0
                print('終了します')
                break

        # 認識できなかったときに止まらないようにする処理
        except sr.UnknownValueError:
            print("could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    


def complete(event):
    global num_list
    global num_time
    txt_complete = int(txt_select.get()) #タスク番号
    num_comp = txt_complete - 1
    num_complete = 180 + num_comp * 20 
    txt = tk.Label(text = u'Complete')
    txt.place(x = 120,y = num_complete)


def timer(event):
    global num_list
    global num_time
    txt_num = int(txt_select.get()) #タスク番号
    a = num_time[txt_num - 1] * 60  # *60に設定で分に変換
    app = Timer()
    app.count_step(a)



def todoList(event):
    global list_y
    global num_list
    global num_time
    txt_list = txt_todo.get()
    txt = tk.Entry(width = 23)
    txt.insert(tk.END,txt_list)
    txt.place(x = 20,y = (180 + list_y))
    txt_list1 = int(txt_time.get())
    txt1 = tk.Entry(width = 15)
    txt1.insert(tk.END,txt_list1)
    txt1.place(x = 500,y=(180+list_y))
    num_list.append(txt_list)
    num_time.append(txt_list1)
    list_y += 20


    

def memo(event):
    global memo_y
    txt_List = txt_memo.get()
    txt = tk.Entry(width = 23)
    txt.insert(tk.END,txt_List)
    txt.place(x = 240,y = (180 + memo_y))
    memo_y += 20


if __name__ == "__main__":  
    root = tk.Tk()
    root.resizable(width = False,height = False)
    root.title(u"TODO LIST")
    root.geometry("700x700")
    f_todo = tk.LabelFrame(root, text = 'TODO LIST', width = 200, height = 400, relief = 'ridge', borderwidth = 9)
    f_todo.pack(padx = 10, pady = 10, side = 'left')

    f_memo = tk.LabelFrame(root,text = 'Memo',width = 200,height = 400,relief = 'ridge',borderwidth = 9)
    f_memo.pack(padx = 10,pady = 10,side = 'left')

    f_watch = tk.LabelFrame(root,text = 'Timer',width = 200,height = 400,relief = 'ridge',borderwidth = 9)
    f_watch.pack(padx = 10,pady = 10,side = 'left')

    #TODOLISTのテキスト
    lbl_todo = tk.Label(text = 'Task Input')
    lbl_todo.place(x=10,y= 560)
    txt_todo = tk.Entry(width = 23)
    txt_todo.place(x = 10,y = 580)

    #TODOLISTの時間テキスト
    lbl_time = tk.Label(text = 'Time Input(Minute)')
    lbl_time.place(x = 10,y = 610)
    txt_time = tk.Entry(width = 15)
    txt_time.place(x = 10,y = 630)



    #Memoのテキスト
    lbl_memo = tk.Label(text = 'Memo Input')
    lbl_memo.place(x = 240,y = 560)
    txt_memo = tk.Entry(width = 23)
    txt_memo.place(x = 240,y = 580)

    #TODOLISTの送信ボタン
    btn_todo = tk.Button(root,text = u'送信')
    btn_todo.place(x = 150,y=650)
    btn_todo.bind("<Button-1>",todoList)

    #Memoの送信ボタン
    btn_memo = tk.Button(root,text = u'送信')
    btn_memo.place(x = 380,y = 650)
    btn_memo.bind("<Button-1>",memo)

    #タスクの選択テキスト
    lbl_select = tk.Label(text = 'Select Task Number')
    lbl_select.place(x = 150,y = 30)
    txt_select = tk.Entry(width = 15)
    txt_select.place(x = 300,y = 30)
    #タスクの選択ボタン
    btn_select = tk.Button(root,text = u'OK')
    btn_select.place(x = 280,y = 60)
    btn_select.bind("<Button-1>",timer)

    #タスクの完了ボタン
    btn_complete = tk.Button(root,text = u'Complete')
    btn_complete.place(x = 340,y = 60)
    btn_complete.bind("<Button-1>",complete)

    #音声認識のテキスト
    lbl_voice = tk.Label(text = 'Voice Input Button')
    lbl_voice.place(x = 500,y=600)
    #音声認識ボタン
    btn_voice = tk.Button(root,text = u'Voice')
    btn_voice.place(x = 550,y = 630)
    btn_voice.bind("<Button-1>",task_voice)


    root.mainloop()
