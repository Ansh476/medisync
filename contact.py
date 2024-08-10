from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from subprocess import Popen
from connection import con

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
    contact_window.withdraw()

def validate_contact(new_value):
    if new_value.isdigit() and len(new_value) <= 10 or new_value == "":
        return True
    else:
        messagebox.showerror("Error", "Invalid phone number! Please enter only digits with a maximum length of 10.")
        return False

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

def save_contact():
    try:
        cname = fullname_entry.get().strip()
        cphone = contact_entry.get().strip()
        codeuq = codeuq_entry.get().strip()

        cursor = con.cursor()
        cursor.execute("INSERT INTO contact (cname, cphone, codeunqe) VALUES (%s, %s, %s)", (cname, cphone, codeuq))
        con.commit()
        cursor.close()

        messagebox.showinfo("Success", "Contact details saved successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Error occurred while saving contact: {str(e)}")

contact_window = Tk()
contact_window.geometry('1300x680+350+150')
contact_window.configure(bg='ivory2')
center_window(contact_window, 1300, 680)
contact_window.resizable(0, 0)
contact_window.title("Period Tracker")


bgImage = PhotoImage(file='mini_project/images/contact.png')
bgLabel = Label(contact_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)


fullname_entry = Entry(contact_window, font=('Roboto', 14), bg='white', fg='black',
                      highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2)
fullname_entry.place(x=530, y=262, width=260)

validate_contact_command = contact_window.register(validate_contact)
contact_entry = Entry(contact_window, font=('Roboto', 14), bg='white', fg='black',
                      highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2,
                      validate="key", validatecommand=(validate_contact_command, '%P'))
contact_entry.place(x=530, y=358, width=260)

save_button = Button(contact_window, text='Save', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0, command=save_contact)
save_button.place(x=560, y=458, width=150)

back_button = Button(contact_window, text='Back', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0, command=go_back)
back_button.place(x=1100, y=60, width=100)

codeuq_label = Label(contact_window, text='ID:', font=('Roboto', 14), bg='white', fg='black')
codeuq_label.place(x=75, y=60)
codeuq_entry = Entry(contact_window, font=('Roboto', 14), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
codeuq_entry.place(x=126, y=60, width=70)
if initial_user_code:
    codeuq_entry.insert(0, initial_user_code)
    
codeuq_label.config(state='disabled')
codeuq_label.configure(bg=contact_window['bg'], fg=contact_window['bg'])  # Make label color same as background
codeuq_entry.config(state='disabled')
codeuq_entry.configure(bg=contact_window['bg'], fg=contact_window['bg']) 

contact_window.mainloop()
