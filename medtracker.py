from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from subprocess import Popen
from connection import con  # Assuming con is your database connection

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
    medtracker_window.withdraw()

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

def save_medicine_count():
    medname = medname_entry.get().strip()
    count = count_entry.get().strip()

    if not medname or not count:
        messagebox.showerror("Error", "Please enter both medicine name and count.")
        return

    try:
        cursor = con.cursor()
        cursor.execute("INSERT INTO medtracker (medicinename, count) VALUES (%s, %s)", (medname, count))
        con.commit()
        cursor.close()
        messagebox.showinfo("Success", "Medicine count saved successfully!")
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", "Failed to save medicine count.")
        
def display_present_count():
    medname = medname_entry.get().strip()

    if not medname:
        messagebox.showerror("Error", "Please enter the medicine name.")
        return

    try:
        cursor = con.cursor()
        cursor.execute("SELECT count FROM medtracker WHERE medicinename = %s", (medname,))
        present_count = cursor.fetchone()
        cursor.close()

        if present_count:
            pcount_entry.delete(0, END)
            # Displaying the updated count
            pcount_entry.insert(0, present_count[0])
        else:
            messagebox.showinfo("Information", f"No entry found for medicine '{medname}'.")

    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", "Failed to fetch present count.")


initial_user_code = fetch_user_code()

medtracker_window = Tk()
medtracker_window.geometry('1300x680+350+150')
medtracker_window.configure(bg='ivory2')
center_window(medtracker_window, 1300, 680)
medtracker_window.resizable(0, 0)
medtracker_window.title("Period Tracker")

bgImage = PhotoImage(file='mini_project/images/reports.png')
bgLabel = Label(medtracker_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

medname_label = Label(medtracker_window, text='Medicine name:', font=('Roboto', 15), bg='white', fg='black')
medname_label.place(x=360, y=200)

medname_entry = Entry(medtracker_window, font=('Roboto', 14), bg='white', fg='black',
                      highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2)
medname_entry.place(x=510, y=200, width=290)

count_label = Label(medtracker_window, text='Count:', font=('Roboto', 15), bg='white', fg='black')
count_label.place(x=360, y=280)

count_entry = Entry(medtracker_window, font=('Roboto', 14), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2)
count_entry.place(x=510, y=280, width=290)

pcount_label = Label(medtracker_window, text='present Count:', font=('Roboto', 15), bg='white', fg='black')
pcount_label.place(x=360, y=360)

pcount_entry = Entry(medtracker_window, font=('Roboto', 14), bg='white', fg='black',
                     highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2)
pcount_entry.place(x=510, y=360, width=290)

save_button = Button(medtracker_window, text='Save', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0, command=save_medicine_count)
save_button.place(x=560, y=438, width=200)

display_button = Button(medtracker_window, text='Display', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0, command=display_present_count)
display_button.place(x=560, y=510, width=200)

back_button = Button(medtracker_window, text='Back', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0, command=go_back)
back_button.place(x=1100, y=60, width=100)

codeuq_label = Label(medtracker_window, text='ID:', font=('Roboto', 14), bg='white', fg='black')
codeuq_label.place(x=75, y=60)

codeuq_entry = Entry(medtracker_window, font=('Roboto', 14), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
codeuq_entry.place(x=126, y=60, width=70)
if initial_user_code:
    codeuq_entry.insert(0, initial_user_code)

codeuq_label.config(state='disabled')
codeuq_label.configure(bg=medtracker_window['bg'], fg=medtracker_window['bg'])  # Make label color same as background
codeuq_entry.config(state='disabled')
codeuq_entry.configure(bg=medtracker_window['bg'], fg=medtracker_window['bg'])

medtracker_window.mainloop()

