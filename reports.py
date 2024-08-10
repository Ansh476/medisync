from tkinter import *
from tkinter import messagebox, filedialog
from subprocess import Popen
import os
import platform
import pickle
from connection import con  # Importing the connection object

def center_window(window, width, height): 
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')

def go_back():
    codeuq = codeuq_entry.get()
    if not codeuq:
        messagebox.showerror("Error", "Please enter the codeuq.")
        return
    hide_current_window()
    Popen(['python', 'mini_project/dashboard.py', codeuq])
    
def hide_current_window():
    report_window.withdraw()

def open_pdf(file_path):
    if platform.system() == 'Windows':
        os.startfile(file_path)
    else:
        opener = 'open' if platform.system() == 'Darwin' else 'xdg-open'
        Popen([opener, file_path])

def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        user_code = codeuq_entry.get()
        if user_code not in pdf_files:
            pdf_files[user_code] = []
        pdf_files[user_code].append(file_path)
        save_pdf_files()

def display_reports():
    user_code = codeuq_entry.get()
    if user_code in pdf_files:
        for widget in report_frame.winfo_children():
            widget.destroy()

        for i, pdf_file in enumerate(pdf_files[user_code], start=1):
            label = Label(report_frame, text=f"{i}. {os.path.basename(pdf_file)}", bg='white', cursor='hand2', font=('Arial', 18))
            label.place(x=0, y=(i-1) * 40)
            label.bind('<Button-1>', lambda event, file_path=pdf_file: open_pdf(file_path))
    else:
        messagebox.showinfo("No Reports", "No reports found for the entered code.")

def save_pdf_files():
    with open('pdf_files.pickle', 'wb') as file:
        pickle.dump(pdf_files, file)

def load_pdf_files():
    global pdf_files
    try:
        with open('pdf_files.pickle', 'rb') as file:
            pdf_files = pickle.load(file)
    except FileNotFoundError:
        pdf_files = {}

def fetch_user_code():
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT u.usercodeinp 
            FROM usercode12 u
            JOIN mylogin m ON u.passwrd = m.mypassword
        """)
        user_code = cursor.fetchone()
        cursor.close()
        return user_code[0] if user_code else None
    except Exception as e:
        print("Error:", e)
        return None

initial_user_code = fetch_user_code()

report_window = Tk()
report_window.geometry('1300x680+350+150')
report_window.configure(bg='ivory2')
center_window(report_window, 1300, 680)
report_window.resizable(0, 0)
report_window.title("Period Tracker")

bgImage = PhotoImage(file='mini_project/images/reports.png')
bgLabel = Label(report_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

pdf_files = {}
load_pdf_files()

report_frame = Frame(report_window, bg='ivory2', width=600, height=400)  
report_frame.place(relx=0.25, rely=0.55, anchor=W) 

upload_button = Button(report_window, text='Upload', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0,
                       command=upload_pdf)
upload_button.place(x=320, y=90, width=230)

codeuq_label = Label(report_window, text='ID:', font=('Roboto', 14), bg='white', fg='black')
codeuq_label.place(x=75, y=60)
codeuq_entry = Entry(report_window, font=('Roboto', 14), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
codeuq_entry.place(x=126, y=60, width=70)
if initial_user_code:
    codeuq_entry.insert(0, initial_user_code)

# Hide codeuq_label and codeuq_entry
codeuq_label.config(state='disabled')
codeuq_label.configure(bg=report_window['bg'], fg=report_window['bg'])  # Make label color same as background
codeuq_entry.config(state='disabled')
codeuq_entry.configure(bg=report_window['bg'], fg=report_window['bg']) 


show_reports_button = Button(report_window, text='Show reports', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0,
                       command=display_reports)
show_reports_button.place(x=670, y=90, width=230)

back_button = Button(report_window, text='Back', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0, command=go_back)
back_button.place(x=1100, y=60, width=100)

report_window.mainloop()







