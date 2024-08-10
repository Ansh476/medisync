from tkinter import *
from tkinter import messagebox, ttk
from subprocess import Popen
import sys
from connection import con
import datetime

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')

def is_female_user(code_entry):
    try:
        cursor = con.cursor()

        # Retrieve gender from the userprofile table where codeuq matches code_entry
        select_query = '''SELECT gender FROM userprofile WHERE codeunq = %s'''
        cursor.execute(select_query, (code_entry,))
        gender_data = cursor.fetchone()

        return gender_data == 'Female'
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False

def on_enter(event):
    event.widget['bg'] = 'steelblue'

def on_leave(event):
    event.widget['bg'] = 'darkslategrey'

def open_dashboard(ucode):
    hide_current_window()
    Popen(['python', 'mini_project/dashboard.py'])

def open_reminder():
    # Display a message with OK and Cancel buttons
    response = messagebox.askquestion("Reminder", "Please fill in the details of the backup contact. Ignore if already filled.")
    
    if response == 'yes':  # If user clicks OK
        hide_current_window()
        Popen(['python', 'mini_project/contact.py'])
    else:  # If user clicks Cancel
        hide_current_window()
        Popen(['python', 'mini_project/reminder.py'])

def open_medtracker():
    hide_current_window()
    Popen(['python', 'mini_project/medtracker.py'])

def open_apschedule():
    hide_current_window()
    Popen(['python', 'mini_project/apschedule.py'])

def open_period_tracker():
    if is_female_user(code_entry.get()):
        hide_current_window()
        Popen(['python', 'mini_project/periodtracker.py'])
    else:
        messagebox.showinfo("Information", "Period tracker is only available for female users.")

def open_periodreports():
    if is_female_user(code_entry.get()):
        hide_current_window()
        Popen(['python', 'mini_project/periodreport.py'])
    else:
        messagebox.showinfo("Information", "Periods data is only available for female users.")

def open_reports():
    hide_current_window()
    Popen(['python', 'mini_project/reports.py'])

def open_consultancy():
    hide_current_window()
    Popen(['python', 'mini_project/consultant.py'])

def hide_current_window():
    dashboard_window.withdraw()

def on_link_enter(event):
    showprofile_label['fg'] = 'slategray'

def on_link_leave(event):
    showprofile_label['fg'] = 'black'

def open_profile_page(event):
    Popen(['python', 'mini_project/userprofile.py'])
    dashboard_window.withdraw()

def on_link_ent(event):
    logout_label['fg'] = 'slategray'

def on_link_leav(event):
    logout_label['fg'] = 'black'

def open_login_page(event):
    Popen(['python', 'mini_project/login.py'])
    dashboard_window.withdraw()

def retrieve_remind_data(code_entry):
    try:
        cursor = con.cursor()

        # Get the current day
        current_day = datetime.datetime.now().strftime("%A")

        # Retrieve data from the remind table based on the current day and code_entry value
        select_query = '''SELECT mdiname,sypname,syp,fdose, sdose, tdose, fodose 
                          FROM remind 
                          WHERE FIND_IN_SET(%s, dow) AND id = %s'''
        cursor.execute(select_query, (current_day, code_entry))
        remind_data = cursor.fetchall()

        return remind_data
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return []

def retrieve_schedule_data(code_entry):
    try:
        cursor = con.cursor()

        # Retrieve data from the schedule table where codeuqi matches code_entry
        select_query = '''SELECT docname, apdate, notes
                          FROM schedule 
                          WHERE codeuqi = %s'''
        cursor.execute(select_query, (code_entry,))
        schedule_data = cursor.fetchall()

        return schedule_data
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return []


quote_index = 0

def display_quote():
    global quote_index
    quote = quotes[quote_index]
    quote_canvas.itemconfig(quote_text, text=quote)
    quote_index = (quote_index + 1) % len(quotes)
    quote_canvas.after(5000, display_quote)  # Display each quote for 5 seconds

# Motivational Quotes
quotes = [
    "Take care of your body. It's the only place you have to live.",
    "The greatest wealth is health.",
    "Healthy is an outfit that looks different on everybody.",
    "An apple a day keeps the doctor away.",
    "Your body hears everything your mind says. Stay positive.",
    "Good health is not something we can buy. However, it can be an extremely valuable savings account.",
    "The groundwork of all happiness is health.",
    "Healthy doesn't mean perfect. It means you're taking care of yourself.",
    "Health is not about the weight you lose, but about the life you gain.",
    "Invest in your health today to enjoy the benefits tomorrow.",
    "Health is not simply the absence of sickness.",
    "The only bad workout is the one that didn't happen.",
    "Exercise is a celebration of what your body can do, not a punishment for what you ate.",
    "To keep the body in good health is a duty... otherwise we shall not be able to keep our mind strong and clear.",
    "He who has health has hope, and he who has hope has everything.",
    "Invest in your health today for a better tomorrow." ,
    "Health is the foundation of happiness and success.",
    "Take care of your body. It's the only place you have to live.",
]

dashboard_window = Tk()
dashboard_window.geometry('1300x680+350+150')
dashboard_window.configure(bg='ivory2')
center_window(dashboard_window, 1300, 680)
dashboard_window.resizable(0, 0)
dashboard_window.title("Dashboard Page")

bgImage = PhotoImage(file='mini_project/images/dashboard.png')

# Resize the image
width = 691  # Adjust as needed
height = 600  # Adjust as needed
bgImage = bgImage.subsample(bgImage.width() // width, bgImage.height() // height)

bgLabel = Label(dashboard_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

logoImage = PhotoImage(file='mini_project/images/logo2.png')
logoLabel = Label(dashboard_window, image=logoImage, bg='white')
logoLabel.place(x=70, y=12)

dashboard_label = Label(dashboard_window, text='Welcome To Medisync', font=('Roboto', 30, 'bold'), bg='lightgray', fg='black')
dashboard_label.place(x=350, y=95)

dashboard_button = Button(dashboard_window, text='Dashboard', font=('Roboto', 18, 'bold'), bg='darkslategrey', fg='gold', command=open_dashboard)
dashboard_button.place(x=31, y=70, width=299, height=60)
dashboard_button.bind('<Enter>', on_enter)
dashboard_button.bind('<Leave>', on_leave)

reminder_button = Button(dashboard_window, text='Reminder', font=('Roboto', 18, 'bold'), bg='darkslategrey', fg='gold', highlightbackground='gold', highlightcolor='gold', highlightthickness=2, command=open_reminder)
reminder_button.place(x=31, y=130, width=299, height=60)
reminder_button.bind('<Enter>', on_enter)
reminder_button.bind('<Leave>', on_leave)

medtracker_button = Button(dashboard_window, text='Medicine Tracker', font=('Roboto', 18, 'bold'), bg='darkslategrey', fg='gold', highlightbackground='gold', highlightcolor='gold', highlightthickness=2, command=open_medtracker)
medtracker_button.place(x=31, y=190, width=299, height=60)
medtracker_button.bind('<Enter>', on_enter)
medtracker_button.bind('<Leave>', on_leave)

schedule_button = Button(dashboard_window, text='Schedule', font=('Roboto', 18, 'bold'), bg='darkslategrey', fg='gold', highlightbackground='gold', highlightcolor='gold', highlightthickness=2, command=open_apschedule)
schedule_button.place(x=31, y=250, width=299, height=60)
schedule_button.bind('<Enter>', on_enter)
schedule_button.bind('<Leave>', on_leave)

periodtrack_button = Button(dashboard_window, text='Periods Tracker', font=('Roboto', 18, 'bold'), bg='darkslategrey', fg='gold', highlightbackground='gold', highlightcolor='gold', highlightthickness=2, command=open_period_tracker)
periodtrack_button.place(x=31, y=310, width=299, height=60)
periodtrack_button.bind('<Enter>', on_enter)
periodtrack_button.bind('<Leave>', on_leave)

period_data = Button(dashboard_window, text='Periods Data', font=('Roboto', 18, 'bold'), bg='darkslategrey', fg='gold', highlightbackground='gold', highlightcolor='gold', highlightthickness=2, command=open_periodreports)
period_data.place(x=31, y=370, width=299, height=60)
period_data.bind('<Enter>', on_enter)
period_data.bind('<Leave>', on_leave)

report_button = Button(dashboard_window, text='Reports', font=('Roboto', 18, 'bold'), bg='darkslategrey', fg='gold', highlightbackground='gold', highlightcolor='gold', highlightthickness=2, command=open_reports)
report_button.place(x=31, y=430, width=299, height=60)
report_button.bind('<Enter>', on_enter)
report_button.bind('<Leave>', on_leave)

consult_button = Button(dashboard_window, text='Consultancy', font=('Roboto', 18, 'bold'), bg='darkslategrey', fg='gold', highlightbackground='gold', highlightcolor='gold', highlightthickness=2, command=open_consultancy)
consult_button.place(x=31, y=490, width=299, height=60)
consult_button.bind('<Enter>', on_enter)
consult_button.bind('<Leave>', on_leave)

consult_button = Button(dashboard_window, text='Contact', font=('Roboto', 18, 'bold'), bg='darkslategrey', fg='gold', highlightbackground='gold', highlightcolor='gold', highlightthickness=2, command=open_consultancy)
consult_button.place(x=31, y=550, width=299, height=60)
consult_button.bind('<Enter>', on_enter)
consult_button.bind('<Leave>', on_leave)

showprofile_label = Label(dashboard_window, text='Profile', font=('Roboto', 18), fg='black', bg='white', cursor='hand2')
showprofile_label.place(x=1150, y=18)
showprofile_label.bind('<Button-1>', open_profile_page)
showprofile_label.bind('<Enter>', on_link_enter)
showprofile_label.bind('<Leave>', on_link_leave)

logout_label = Label(dashboard_window, text='Log out', font=('Roboto', 18), fg='black', bg='white', cursor='hand2')
logout_label.place(x=110, y=630)
logout_label.bind('<Button-1>', open_login_page)
logout_label.bind('<Enter>', on_link_ent)
logout_label.bind('<Leave>', on_link_leav)

code_label = Label(dashboard_window, text='ID:', font=('Roboto', 15), bg='white', fg='black')
code_label.place(x=1000, y=18)

code_entry = Entry(dashboard_window, font=('Roboto', 18), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
code_entry.place(x=1050, y=18, width=70)

remindert_label = Label(dashboard_window, text='Reminder Table', font=('Roboto', 20), bg='lightgrey', fg='black')
remindert_label.place(x=630, y=210)

schedulet_label = Label(dashboard_window, text='Appointments', font=('Roboto', 20), bg='lightgrey', fg='black')
schedulet_label.place(x=640, y=492)

# Create the Treeview widget for the table
tree = ttk.Treeview(dashboard_window, columns=("medname","sypname","syp", "1st dose", "2nd dose", "3rd dose", "4th dose"), show="headings")

# Define column headings
tree.heading("medname", text="Medicine Name")
tree.heading("sypname", text="Syrup Name")
tree.heading("syp", text="Syrup")
tree.heading("1st dose", text="1st Dose")
tree.heading("2nd dose", text="2nd Dose")
tree.heading("3rd dose", text="3rd Dose")
tree.heading("4th dose", text="4th Dose")

# Set column widths
tree.column("medname", width=125)
tree.column("sypname", width=125)
tree.column("syp", width=110)
tree.column("1st dose", width=110)
tree.column("2nd dose", width=110)
tree.column("3rd dose", width=110)
tree.column("4th dose", width=110)

# Place the Treeview widget
tree.place(x=350, y=245)

schedule_tree = ttk.Treeview(dashboard_window, columns=("doctor_name", "date", "notes"), show="headings", height =5)

# Define column headings
schedule_tree.heading("doctor_name", text="Doctor Name")
schedule_tree.heading("date", text="Date")
schedule_tree.heading("notes", text="Notes")

# Set column widths
schedule_tree.column("doctor_name", width=266)
schedule_tree.column("date", width=266)
schedule_tree.column("notes", width=266)

# Place the Treeview widget
schedule_tree.place(x=350, y=530)

try:
    ucode = sys.argv[1]
except IndexError:
    messagebox.showerror("Error", "UCODE not provided.")
    sys.exit(1)

code_entry.insert(0, ucode)

# Retrieve and insert data into the Treeview
remind_data = retrieve_remind_data(code_entry.get())
for data in remind_data:
    tree.insert("", "end", values=data)

schedule_data = retrieve_schedule_data(code_entry.get())
for data in schedule_data:
    schedule_tree.insert("", "end", values=data)

# Create canvas for displaying quotes
quote_canvas = Canvas(dashboard_window, bg='white', width=810, height=80)
quote_canvas.place(x=350, y=100)

# Display the first quote
quote_text = quote_canvas.create_text(10, 10, anchor='nw', text=quotes[0], font=('Arial', 18), fill='red', width=800)

# Start displaying quotes
display_quote()

dashboard_window.mainloop()
