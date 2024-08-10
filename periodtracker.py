from tkinter import *
from tkinter import messagebox, PhotoImage
from tkinter.ttk import Combobox
from tkinter import simpledialog
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
    periodtracker_window.withdraw()

# Function to handle the 'Set tracker' button click event
# Function to show the notification
def show_notification():
    messagebox.showinfo("Notification", "Your period is approaching in 5 days.")

# Function to handle the 'Set tracker' button click event
# Function to handle the 'Set tracker' button click event
def set_tracker():
    # Retrieve user inputs from entry fields
    avg_cycle_length = int(cyclelength_entry.get())
    last_period_date_str = lastperiod_entry.get()
    notes = periodnote_entry.get("1.0", "end-1c")  # Get notes from Text widget

    # Convert last period date string to datetime object
    last_period_date = datetime.strptime(last_period_date_str, "%d-%m-%Y")

    # Calculate the expected next period date
    next_period_date = last_period_date + timedelta(days=avg_cycle_length)

    # Calculate the notification date (5 days before the expected next period date)
    notification_date = next_period_date - timedelta(days=5)

    print("Notification Date:", notification_date)
    print("Today's Date:", datetime.today())

    # Save user inputs to the database
    save_to_database(avg_cycle_length, last_period_date, notes)

    # Show a message box to confirm the tracker has been set
    messagebox.showinfo("Tracker Set", "Period tracker has been set successfully.")

    # Check if the notification date is today
    if notification_date.date() == datetime.today().date():
        # If yes, schedule a notification after 5 seconds
        periodtracker_window.after(5000, show_notification)

    
# Function to save user inputs to the database
def save_to_database(avg_cycle_length, last_period_date, notes):
    try:
        cursor = con.cursor()

        # Define the SQL query to insert data into the table
        insert_query = "INSERT INTO period (avglength, lastpdate, notes) VALUES (%s, %s, %s)"

        # Execute the query with user inputs as parameters
        cursor.execute(insert_query, (avg_cycle_length, last_period_date.strftime("%Y-%m-%d"), notes))

        # Commit changes
        con.commit()
        cursor.close()
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Database Error", "An error occurred while saving data to the database.")
        
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

# Function to handle the selection of the last period date
def get_last_period_date():
    def on_date_select():
        selected_date = cal.get_date()
        if selected_date:
            lastperiod_entry.delete(0, END)
            lastperiod_entry.insert(0, selected_date)
            top.destroy()

    def close_calendar():
        top.destroy()

    top = Toplevel()
    top.title("Select Last Period Date")

    # Center the calendar window
    top.update_idletasks()
    x = (top.winfo_screenwidth() - top.winfo_reqwidth()) // 2
    y = (top.winfo_screenheight() - top.winfo_reqheight()) // 2
    top.geometry("+{}+{}".format(x, y))

    cal = Calendar(top, selectmode="day", date_pattern="dd-mm-yyyy")
    cal.pack(fill="both", expand=True)

    select_button = Button(top, text="Get Date", command=on_date_select)
    select_button.pack()

    close_button = Button(top, text="Close", command=close_calendar)
    close_button.pack(side=RIGHT)

    top.mainloop()

# Create the main window
periodtracker_window = Tk()
periodtracker_window.geometry('1300x680+350+150')
periodtracker_window.configure(bg='ivory2')
center_window(periodtracker_window, 1300, 680)
periodtracker_window.resizable(0, 0)
periodtracker_window.title("Period Tracker")

# Load and place background image
bg_image = PhotoImage(file='mini_project/images/periodtracker.png')
bg_label = Label(periodtracker_window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Define and place UI elements
cyclelength_label = Label(periodtracker_window, text='Average Cycle Length (days):', font=('Roboto', 18), bg='white', fg='black')
cyclelength_label.place(x=310, y=230)

cyclelength_entry = Entry(periodtracker_window, font=('Roboto', 16), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
cyclelength_entry.place(x=640, y=230, width=200)

lastperiod_label = Label(periodtracker_window, text='Start Date of Last Period:', font=('Roboto', 18), bg='white', fg='black')
lastperiod_label.place(x=310, y=280)

lastperiod_entry = Entry(periodtracker_window, font=('Roboto', 16), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
lastperiod_entry.place(x=640, y=280, width=200)

last_period_button = Button(periodtracker_window, text="Select Date", command=get_last_period_date)
last_period_button.place(x=870, y=280, width=100)

periodnote_label = Label(periodtracker_window, text='Notes:', font=('Roboto', 16), bg='white', fg='black')
periodnote_label.place(x=310, y=340)

periodnote_entry = Text(periodtracker_window, font=('Roboto', 14), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2, height=4, wrap=WORD)
periodnote_entry.place(x=410, y=340, width=500)

codeuq_label = Label(periodtracker_window, text='ID:', font=('Roboto', 14), bg='white', fg='black')
codeuq_label.place(x=160, y=60)

codeuq_entry = Entry(periodtracker_window, font=('Roboto', 14), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
codeuq_entry.place(x=200, y=60, width=70)
if initial_user_code:
    codeuq_entry.insert(0, initial_user_code)
    
codeuq_label.config(state='disabled')
codeuq_label.configure(bg=periodtracker_window['bg'], fg=periodtracker_window['bg'])  # Make label color same as background
codeuq_entry.config(state='disabled')
codeuq_entry.configure(bg=periodtracker_window['bg'], fg=periodtracker_window['bg']) 

back_button = Button(periodtracker_window, text='Back', font=('Roboto', 15), bg='orchid', fg='white', bd=0, command=go_back)
back_button.place(x=1100, y=30, width=100)

set_tracker_button = Button(periodtracker_window, text='Set Tracker', font=('Roboto', 15), bg='orchid', fg='white', bd=0, command=set_tracker)
set_tracker_button.place(x=540, y=500, width=230)

# Start the GUI event loop
periodtracker_window.mainloop()
