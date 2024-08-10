from tkinter import *
from tkinter import messagebox, PhotoImage
from tkinter.ttk import Combobox
from connection import con
from datetime import datetime, timedelta
from tkcalendar import Calendar
from subprocess import Popen

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')
    
def go_back():
    # Retrieve the codeuq from the entry field
    codeuq = codeuq_entry.get()
    if not codeuq:
        messagebox.showerror("Error", "Please enter the codeuq.")
        return
    hide_current_window()
    Popen(['python', 'mini_project/dashboard.py', codeuq])

    
def hide_current_window():
    periodreport_window.withdraw()

# Function to retrieve data from the database based on the entered month and display it on the window
def retrieve_and_display_data():
    # Get the month entered by the user
    month = month_entry.get().lower().capitalize()  # Convert to lowercase and capitalize the first letter

    try:
        cursor = con.cursor()

        # Define the SQL query to retrieve data based on the month
        select_query = "SELECT avglength, lastpdate, notes FROM period WHERE MONTHNAME(lastpdate) = %s"

        # Execute the query with the month parameter
        cursor.execute(select_query, (month,))

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Display the retrieved data in the text widget
        data_text.delete(1.0, END)  # Clear previous data
        for row in rows:
            data_text.insert(END, f"Average Length: {row[0]}\n")
            data_text.insert(END, f"Last Period Date: {row[1]}\n")
            data_text.insert(END, f"Notes: {row[2]}\n")
            data_text.insert(END, "-" * 50 + "\n")

        cursor.close()
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Database Error", "An error occurred while retrieving data from the database.")
        
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


periodreport_window = Tk()
periodreport_window.geometry('1300x680+350+150')
periodreport_window.configure(bg='ivory2')
center_window(periodreport_window, 1300, 680)
periodreport_window.resizable(0, 0)
periodreport_window.title("Period Tracker Reports")

# Background image
bgImage = PhotoImage(file='mini_project/images/reports.png')
bgLabel = Label(periodreport_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

# Label and entry for entering the month
month_label = Label(periodreport_window, text='Enter Month:', font=('Roboto', 18), bg='white', fg='black')
month_label.place(x=310, y=120)

month_entry = Entry(periodreport_window, font=('Roboto', 16), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
month_entry.place(x=480, y=120, width=200)

# Button to retrieve data and display on the window
retrieve_button = Button(periodreport_window, text='Retrieve Data', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0, command=retrieve_and_display_data)
retrieve_button.place(x=700, y=120, width=200)

# Text widget to display the retrieved data
data_text = Text(periodreport_window, font=('Roboto', 14), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2, wrap=WORD)
data_text.place(x=290, y=170, width=650, height=200)

codeuq_label = Label(periodreport_window, text='ID:', font=('Roboto', 14), bg='white', fg='black')
codeuq_label.place(x=75, y=60)
codeuq_entry = Entry(periodreport_window, font=('Roboto', 14), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
codeuq_entry.place(x=126, y=60, width=70)
if initial_user_code:
    codeuq_entry.insert(0, initial_user_code)
    
codeuq_label.config(state='disabled')
codeuq_label.configure(bg=periodreport_window['bg'], fg=periodreport_window['bg'])  # Make label color same as background
codeuq_entry.config(state='disabled')
codeuq_entry.configure(bg=periodreport_window['bg'], fg=periodreport_window['bg']) 

back_button = Button(periodreport_window, text='Back', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0, command=go_back)
back_button.place(x=1100, y=60, width=100)

periodreport_window.mainloop()

