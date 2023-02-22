from tkinter import *
from tkinter import messagebox as ms
import requests, os

root = Tk()

###전원끄기 버튼 만들기
###1분 더 버튼 만들기

######Window Settings#######
root.title("컴퓨터펜스 라이트 COMPUTERFENCE LITE v1.0")
root.geometry("640x480")
root.attributes("-fullscreen", True, "-topmost", 1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

def Setting_UI():
    global setting_password_box, setting_window, setting_id_box
    setting_window = Toplevel()
    setting_title_label = Label(setting_window, text="컴퓨터펜스 라이트 로그인")
    setting_id_box = Entry(setting_window, width=40)
    setting_password_box = Entry(setting_window, width=40)
    setting_ok_button = Button(setting_window, text="확인", width=10, command=login)
    setting_title_label.pack()
    setting_id_box.pack()
    setting_password_box.pack()
    setting_ok_button.pack()

###
def do_exit():
    global pressed_f4
    print('Trying to close application')
    if pressed_f4:  # Deny if Alt-F4 is pressed
        print('Denied!')
        pressed_f4 = False  # Reset variable

def alt_f4(event):  # Alt-F4 is pressed
    global pressed_f4
    print('Alt-F4 pressed')
    pressed_f4 = True
    
def close(*event):  # Exit application
    root.destroy()

def power_off():
    os.system('shutdown -s -f -t 0')

def login():
    id = setting_id_box.get()
    password = setting_password_box.get()
    response = requests.post('https://ComFence-LiteAPI.seungwoohan0104.repl.co/login', {"id": id,"password": password})
    root.withdraw()
    if response.text == "로그인 성공":
        setting_window.destroy()
        root.deiconify()
        ms.showinfo("알림", "로그인에 성공했습니다")
        f = open('./windows.dll', 'w')
        f.write(f"true\n{id}")
        f.close()
    else:
        ms.showinfo("알림", "로그인 실패")
    #여기부터 로그인 성공하면 정보 받아와서 창 닫고 막는 창 켜기 코드 작성

root.bind('<Alt-F4>', alt_f4)
root.protocol("WM_DELETE_WINDOW",do_exit)

f = open('./windows.dll', 'r')
lines = f.readlines()
datas = []
for line in lines:
    line = line.strip()
    datas.append(line)

def getinfo():
    response = requests.get(f'https://ComFence-LiteAPI.seungwoohan0104.repl.co/getinfo/{datas[1]}')
    if response.text == "unlocked":
        root.withdraw()
    else:
        root.deiconify()
    root.after(1000, getinfo)

def OneMin():
    global onemin
    onemin = 1

######Root 위젯######
title = Label(root, text="<컴퓨터펜스 라이트>")
title.pack()
explain = Label(root, text="부모님이 컴퓨터 사용을 제한하셨습니다")
explain.pack()
OffBtn = Button(root, text="전원끄기", width=20, command=power_off)
OffBtn.pack()

if datas[0] == "false":
    root.withdraw()
    Setting_UI()

root.after(1000, getinfo)

root.mainloop()
