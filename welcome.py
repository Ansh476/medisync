from tkinter import *
from tkinter import messagebox, PhotoImage
from subprocess import Popen

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')
 
def open_login_page():
    Popen(['python', 'mini_project/login.py'])
    welcome_window.withdraw() 
 
def on_enter(event):
    login_button.config(bg='lightslategrey')

def on_leave(event):
    login_button.config(bg='lightgrey')
    
welcome_window = Tk()
welcome_window.geometry('1300x680+350+150')
welcome_window.configure(bg='ivory2')
center_window(welcome_window, 1300, 680)
welcome_window.resizable(0, 0)
welcome_window.title("Dashboard Page")

bgImage = PhotoImage(file='mini_project/images/welcomepage.png')

# Resize the image
width = 691  # Adjust as needed
height = 600  # Adjust as needed
bgImage = bgImage.subsample(bgImage.width() // width, bgImage.height() // height)

bgLabel = Label(welcome_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

login_button_img = PhotoImage(file='mini_project/images/roundbutton.png')
login_button = Button(welcome_window, text='LOGIN', font=('Roboto', 16), bg='lightgrey', fg='midnightblue', bd=0, command=open_login_page, compound=CENTER, image=login_button_img)
login_button.place(x=157, y=553)

login_button.bind('<Enter>', on_enter)
login_button.bind('<Leave>', on_leave)

welcome_window.mainloop()
