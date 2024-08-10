from tkinter import *
from tkinter import messagebox, PhotoImage
from tkcalendar import Calendar
from subprocess import Popen
from connection import con
from datetime import datetime, timedelta

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
    schedule_window.withdraw()

def save_to_database(docname, apdate, notes, codeuqi):
    try:
        cursor = con.cursor()

        # Define the SQL query to insert data into the table
        insert_query = "INSERT INTO schedule (docname, apdate, notes, codeuqi) VALUES (%s, %s, %s, %s)"

        # Execute the query with user inputs as parameters
        cursor.execute(insert_query, (docname, apdate, notes, codeuqi))

        # Commit changes
        con.commit()
        cursor.close()
        messagebox.showinfo("Success", "Appointment scheduled successfully.")
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Database Error", "An error occurred while saving data to the database.")

def get_ap_date():
    def on_date_select():
        selected_date = cal.get_date()
        if selected_date:
            apdate_entry.delete(0, END)
            apdate_entry.insert(0, selected_date)
            top.destroy()

    def close_calendar():
        top.destroy()

    top = Toplevel()
    top.title("Select Appointment Date")

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

def show_notification(docname, schedule_window):
    messagebox.showinfo("Notification", f"Reminder: Tomorrow is your appointment with {docname}.")


def set_tracker():
    docname = docname_entry.get()
    apdate = apdate_entry.get()
    notes = note_entry.get("1.0", "end-1c")  # Get notes from Text widget
    codeuqi = codeuq_entry.get()
    
    if not (docname and apdate and codeuqi):
        messagebox.showerror("Error", "Please fill all the required fields.")
        return

    # Save appointment details to the database
    save_to_database(docname, apdate, notes, codeuqi)

    # Calculate the appointment date as datetime object
    apdate_datetime = datetime.strptime(apdate, "%d-%m-%Y")

    # Calculate today's date
    today_date = datetime.today().date()

    # Calculate the notification date (one day before the appointment)
    notification_date = apdate_datetime - timedelta(days=1)

    # If the appointment date is tomorrow, show the notification today
    if apdate_datetime.date() == today_date + timedelta(days=1):
        schedule_window.after(5000, show_notification, docname, schedule_window)
    else:
        # Schedule the notification one day before the appointment
        schedule_notification(notification_date, docname)

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


def schedule_notification(notification_date, docname):
    # Get today's date
    today_date = datetime.today().date()

    # If the notification date is in the future, schedule it
    if notification_date.date() >= today_date:
        # Calculate the delay until the notification date
        delay = (notification_date - today_date).total_seconds() * 1000

        # Schedule the notification after the delay
        schedule_window.after(int(delay), show_notification, docname, schedule_window)
    else:
        messagebox.showwarning("Notification", "Notification date has passed.")


schedule_window = Tk()
schedule_window.geometry('1300x680+350+150')
schedule_window.configure(bg='ivory2')
center_window(schedule_window, 1300, 680)
schedule_window.resizable(0, 0)
schedule_window.title("Schedule Appointment")

# Background image
bgImage = PhotoImage(file='mini_project/images/schedule.png')
bgLabel = Label(schedule_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

codeuq_label = Label(schedule_window, text='ID:', font=('Roboto', 14,'bold'), bg='cadetblue', fg='white')
codeuq_label.place(x=160, y=60)
codeuq_entry = Entry(schedule_window, font=('Roboto', 14), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
codeuq_entry.place(x=200, y=60, width=70)
if initial_user_code:
    codeuq_entry.insert(0, initial_user_code)
    
codeuq_label.config(state='disabled')
codeuq_label.configure(bg=schedule_window['bg'], fg=schedule_window['bg'])  # Make label color same as background
codeuq_entry.config(state='disabled')
codeuq_entry.configure(bg=schedule_window['bg'], fg=schedule_window['bg']) 

docname_label = Label(schedule_window, text='Doctor name:', font=('Roboto', 18,'bold'), bg='cadetblue', fg='white')
docname_label.place(x=310, y=180)

docname_entry = Entry(schedule_window, font=('Roboto', 16), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
docname_entry.place(x=540, y=180, width=350)

apdate_label = Label(schedule_window, text='Appointment date:', font=('Roboto', 18,'bold'), bg='cadetblue', fg='white')
apdate_label.place(x=310, y=248)

apdate_entry = Entry(schedule_window, font=('Roboto', 16), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
apdate_entry.place(x=540, y=248, width=200)

apdate_button = Button(schedule_window, text="Select Date", command=get_ap_date)
apdate_button.place(x=770, y=248, width=100)

note_label = Label(schedule_window, text='Notes:', font=('Roboto', 18,'bold'), bg='cadetblue', fg='white')
note_label.place(x=310, y=320)

note_entry = Text(schedule_window, font=('Roboto', 14,), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2, height=4, wrap=WORD)
note_entry.place(x=410, y=320, width=500)

set_tracker_button = Button(schedule_window, text='Set Reminder', font=('Roboto', 15,'bold'), bg='cadetblue', fg='white', bd=0, command=set_tracker)
set_tracker_button.place(x=540, y=450, width=230)

back_button = Button(schedule_window, text='Back', font=('Roboto', 15,'bold'), bg='cadetblue', fg='white', bd=0, command=go_back)
back_button.place(x=1020, y=60, width=100)

schedule_window.mainloop()

