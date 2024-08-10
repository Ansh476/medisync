from tkinter import *
from tkinter import messagebox, PhotoImage
from tkinter.ttk import Combobox
from tkinter import simpledialog
from subprocess import Popen
from connection import con
import sys
sys.path.append(r'C:\Users\admin\Desktop\python\mini_project\Lib\site-packages')
import pygame
import logging
from gtts import gTTS
import schedule
import time
import threading
import os
from datetime import datetime
import calendar

pygame.mixer.init()

cursor = con.cursor()

def on_enter(event):
    onemoremed_label['fg'] = 'darkturquoise'

def on_leave(event):
    onemoremed_label['fg'] = 'teal'

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')

import sys

def go_back():
    # Retrieve the codeuq from the entry field
    codeuq = codeuq_entry.get()
    if not codeuq:
        messagebox.showerror("Error", "Please enter the codeuq.")
        return
    hide_current_window()
    Popen(['python', 'mini_project/dashboard.py', codeuq])

    
def hide_current_window():
    reminder_window.withdraw()

def open_new_reminder_page():
    python_executable = sys.executable
    Popen([python_executable, 'mini_project/reminder.py'])
    reminder_window.withdraw()

dose_counter = 1 

scheduled_reminders = {}

def play_reminder_audio(medname, pills, syrupname, syrup, selected_days):
    global stop_reminder
    global user_interacted  # Declare user_interacted as global
    
    # Function to play the reminder audio
    def play_audio():
        global stop_reminder
        global user_interacted  # Declare user_interacted as global
        user_interacted = False 
        # Get the current day of the week
        current_day = calendar.day_name[datetime.now().weekday()]
        
        # Check if the current day matches any of the selected days
        if current_day in selected_days:
            # Text to Speech (TTS) using gTTS
            if syrupname and syrup:
                text = f"Reminder: Take {pills} pills of {medname} and {syrup} of {syrupname} syrup."
            else:
                text = f"Reminder: Take {pills} pills of {medname}."

            audio_filename = f'{medname}_reminder.mp3'

            # Check if the audio file already exists
            if not os.path.isfile(audio_filename):
                tts = gTTS(text=text, lang='en')
                tts.save(audio_filename)

            # Play the audio three times or until stop_reminder is True
            count = 0
            while count < 3 and not stop_reminder:
                pygame.mixer.music.load(audio_filename)
                pygame.mixer.music.play()
                time.sleep(1)  # Wait for one second before showing the message box
                show_message_box()  # Show the message box after one second
                while pygame.mixer.music.get_busy() and not stop_reminder:
                    time.sleep(1)
                count += 1

    # Function to show the message box
    def show_message_box():
        global stop_reminder, user_interacted
        if not stop_reminder:
            # Show the message box after one second of audio playback
            result = messagebox.askokcancel("Reminder", "Reminder: Take your medication!")
            if result:
                stop_reminder = True  # Stop the reminder if "OK" is clicked
                user_interacted = True # Set user_interacted to True if "OK" is clicked
                # Update count in the database
                try:
                    cursor = con.cursor()
                    # Reduce the count by the number of pills
                    cursor.execute("UPDATE medtracker SET count = count - %s WHERE medicinename = %s", (pills, medname))
                    con.commit()
                    cursor.close()
                except Exception as e:
                    print("Error:", e)

    # Function to be executed after 15 seconds if the user doesn't acknowledge the reminder
    def send_reminder_notification():
        global stop_reminder, user_interacted
        if not stop_reminder and not user_interacted:  # Check if user_interacted is False
            # Retrieve contact's name and phone number from the database
            try:
                cursor = con.cursor()
                cursor.execute("SELECT cname, cphone FROM contact LIMIT 1")  # Assuming only one contact for simplicity
                contact_info = cursor.fetchone()
                cursor.close()

                if contact_info:
                    cname, cphone = contact_info
                    messagebox.showinfo("Reminder Notification", f"Reminder notification sent to {cname} ({cphone}).")
            except Exception as e:
                print("Error:", e)

    # Reset stop_reminder variable
    stop_reminder = False

    # Schedule the reminder notification after 15 seconds
    timer = threading.Timer(15, send_reminder_notification)
    timer.start()

    # Play the audio
    play_audio()

    # After playing the audio, reset stop_reminder for the next reminder
    stop_reminder = False

    

def schedule_reminders(medname, pills, syrupname, syrup, dose_times, selected_days):
    def job():
        for dose_time in dose_times:
            schedule.every().day.at(dose_time).do(play_reminder_audio, medname, pills, syrupname, syrup, selected_days)

        while True:
            schedule.run_pending()
            time.sleep(1)

    # If reminders were previously scheduled for this medicine, stop them
    if medname in scheduled_reminders:
        for job in scheduled_reminders[medname]:
            job.stop()
        scheduled_reminders[medname] = []

    # Create a new thread and start the job
    reminder_thread = threading.Thread(target=job)
    reminder_thread.start()

    # Store the scheduled job in the dictionary
    scheduled_reminders[medname] = schedule.get_jobs()


def select_time():
    def update_dose_entry(time):
        time_with_seconds = f"{time}:00" if ":" in time and len(time.split(":")) == 2 else time

        if dose_counter == 1:
            firstdose_entry.delete(0, END)
            firstdose_entry.insert(0, time_with_seconds)
        elif dose_counter == 2:
            seconddose_entry.delete(0, END)
            seconddose_entry.insert(0, time_with_seconds)
        elif dose_counter == 3:
            thirddose_entry.delete(0, END)
            thirddose_entry.insert(0, time_with_seconds)
        elif dose_counter == 4:
            fourthdose_entry.delete(0, END)
            fourthdose_entry.insert(0, time_with_seconds)

    current_time = datetime.now().strftime("%H:%M:%S")
    dose_time = simpledialog.askstring("Enter Time", "Enter the time for the dose (HH:MM:SS):", initialvalue=current_time)

    if dose_time:
        update_dose_entry(dose_time)

def select_all_days():
    for var in day_vars:
        var.set(1)

def validate_pills_input(event):
    value = event.widget.get()
    if value.strip():
        try:
            pills = int(value)
            if pills < 1:
                messagebox.showerror("Error", "Invalid entry. Please enter a value greater than or equal to 1.")
            elif pills > 4:
                messagebox.showwarning("Warning", "This is an overdose. Please consult your doctor.")
        except ValueError:
            messagebox.showerror("Error", "Invalid entry. Please enter an integer value.")

def validate_doses_entry():
    try:
        doses = int(dose_entry.get().strip())
        if doses < 1 or doses > 4:
            messagebox.showerror("Error", "Invalid number of doses. Enter a value between 1 and 4.")
            return False
        return True
    except ValueError:
        messagebox.showerror("Error", "Invalid entry for doses. Enter an integer value.")
        return False

def validate_dose_entries():
    try:
        doses = int(dose_entry.get().strip())
        if doses < 1 or doses > 4:
            messagebox.showerror("Error", "Invalid number of doses. Enter a value between 1 and 4.")
            return False
    except ValueError:
        messagebox.showerror("Error", "Invalid entry for doses. Enter an integer value.")
        return False

    if doses == 1 and not firstdose_entry.get().strip():
        messagebox.showerror("Error", "Enter the time for the first dose.")
        return False
    elif doses == 2 and (not firstdose_entry.get().strip() or not seconddose_entry.get().strip()):
        messagebox.showerror("Error", "Enter the time for both doses.")
        return False
    elif doses == 3 and (not firstdose_entry.get().strip() or not seconddose_entry.get().strip() or not thirddose_entry.get().strip()):
        messagebox.showerror("Error", "Enter the time for all three doses.")
        return False
    elif doses == 4 and (not firstdose_entry.get().strip() or not seconddose_entry.get().strip() or not thirddose_entry.get().strip() or not fourthdose_entry.get().strip()):
        messagebox.showerror("Error", "Enter the time for all four doses.")
        return False

    return True

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

def store_reminder(medname_entry, selected_days, pills_entry, syrup_combo, dose_entry, dose_times_entries, syrupname_entry, codeuq_entry):
    try:
        cursor = con.cursor()
        provided_codeuq = codeuq_entry.get().strip()

        dose_times = [entry.get().strip() for entry in dose_times_entries if entry.get().strip()]

        if not validate_doses_entry():
            return

        if not validate_dose_entries():
            return

        selected_days = ','.join([days[i] for i, var in enumerate(day_vars) if var.get()])

        medname = medname_entry.get().strip()
        pills = pills_entry.get().strip()
        syrupname = syrupname_entry.get().strip()
        syrup = syrup_combo.get().strip()
        dose = dose_entry.get().strip()

        for dose_time in dose_times:
            insert_query = '''INSERT INTO reminder 
                            (medname, daysofweek, pills, syrupname, syrup, dose, codeuq) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(insert_query, (medname, selected_days, pills, syrupname, syrup, dose, provided_codeuq))

        con.commit()

        cursor.close()

        if dose_times:
            schedule_reminders(medname, pills, syrupname, syrup, dose_times, selected_days)

        messagebox.showinfo("Success", "Reminder stored successfully!")

    except Exception as e:
        logging.error(f"Error occurred while storing reminder: {str(e)}")
        messagebox.showerror("Error", f"Error occurred: {str(e)}")

def store_reminder_data(medname, selected_days_str, pills, syrupname, syrup, doses, first_dose, second_dose, third_dose, fourth_dose, codeuq):
    try:
        cursor = con.cursor()

        # Convert selected days from indices to day names
        selected_days_names = [days[i] for i, var in enumerate(day_vars) if var.get()]
        selected_days_str = ','.join(selected_days_names)

        # Insert reminder data into the "remind" table
        insert_query = '''INSERT INTO remind 
                        (mdiname, dow, pill, sypname, syp, dos, fdose, sdose, tdose, fodose, id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(insert_query, (medname, selected_days_str, pills, syrupname, syrup, doses, first_dose, second_dose, third_dose, fourth_dose, codeuq))

        con.commit()
        cursor.close()

        messagebox.showinfo("Success", "Reminder data stored successfully!")

    except Exception as e:
        logging.error(f"Error occurred while storing reminder data: {str(e)}")
        messagebox.showerror("Error", f"Error occurred while storing reminder data: {str(e)}")


def apply_reminder():
    store_reminder(medname_entry, ','.join([str(var.get()) for var in day_vars]), pills_entry, syrup_combo, dose_entry, [firstdose_entry, seconddose_entry, thirddose_entry, fourthdose_entry], syrupname_entry, codeuq_entry)
    store_reminder_data(medname_entry.get().strip(), ','.join([str(var.get()) for var in day_vars]), pills_entry.get().strip(), syrupname_entry.get().strip(), syrup_combo.get().strip(), dose_entry.get().strip(), firstdose_entry.get().strip(), seconddose_entry.get().strip(), thirddose_entry.get().strip(), fourthdose_entry.get().strip(), codeuq_entry.get().strip())


reminder_window = Tk()
reminder_window.geometry('1300x680+350+150')
reminder_window.configure(bg='ivory2')
center_window(reminder_window, 1300, 680)
reminder_window.resizable(0, 0)
reminder_window.title("Reminder Page")

bgImage = PhotoImage(file='mini_project/images/rem.png')
width = 691
height = 600
bgImage = bgImage.subsample(bgImage.width() // width, bgImage.height() // height)

bgLabel = Label(reminder_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

reminder_label = Label(reminder_window, text='REMINDERS', font=('Roboto', 25, 'bold'), bg='powderblue', fg='black')
reminder_label.place(x=560, y=20)

medname_label = Label(reminder_window, text='Name of the Medicine:', font=('Roboto', 18), bg='powderblue', fg='black')
medname_label.place(x=325, y=120)

medname_entry = Entry(reminder_window, font=('Roboto', 16), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
medname_entry.place(x=595, y=120, width=415)

DOW_label = Label(reminder_window, text='Select the days of week:', font=('Roboto', 18), bg='powderblue', fg='black')
DOW_label.place(x=325, y=180)

day_vars = [IntVar() for _ in range(7)]
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
checkboxes = []
for i, day in enumerate(days):
    checkbox = Checkbutton(reminder_window, text=day, variable=day_vars[i], font=('Roboto', 15), bg='powderblue', fg='black')
    checkbox.place(x=325, y=220 + i * 40)

select_all_checkbox = Checkbutton(reminder_window, text="Select All", command=select_all_days, font=('Roboto', 14), bg='powderblue', fg='black')
select_all_checkbox.place(x=325, y=218 + len(days) * 40)

pills_label = Label(reminder_window, text='Number of pills:', font=('Roboto', 18), bg='powderblue', fg='black')
pills_label.place(x=625, y=180)

pills_entry = Entry(reminder_window, font=('Roboto', 16), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
pills_entry.place(x=900, y=180, width=110)
pills_entry.bind("<KeyRelease>", validate_pills_input)

syrupname_label = Label(reminder_window, text='Name of syrup:', font=('Roboto', 18), bg='powderblue', fg='black')
syrupname_label.place(x=625, y=230)

syrupname_entry = Entry(reminder_window, font=('Roboto', 16), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
syrupname_entry.place(x=900, y=230, width=110)

syrup_label = Label(reminder_window, text='Amount of syrup:', font=('Roboto', 18), bg='powderblue', fg='black')
syrup_label.place(x=625, y=270)

syrup_options = ['2.5ml', '5ml', '7.5ml', '10ml']
syrup_combo = Combobox(reminder_window, values=syrup_options, font=('Roboto', 16))
syrup_combo.place(x=900, y=270, width=110)

dose_label = Label(reminder_window, text='Doses per day:', font=('Roboto', 18), bg='powderblue', fg='black')
dose_label.place(x=625, y=330)

dose_entry = Entry(reminder_window, font=('Roboto', 18), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
dose_entry.place(x=900, y=330, width=110)

firstdose_label = Label(reminder_window, text='1', font=('Roboto', 18), bg='powderblue', fg='black')
firstdose_label.place(x=886, y=390)

firstdose_button = Button(reminder_window, text="Click here to select time", font=('Roboto', 18), bg='powderblue', fg='black', command=select_time)
firstdose_button.grid(row=1, column=0, columnspan=2, pady=10)
firstdose_button.place(x=625, y=390, width=260)

firstdose_entry = Entry(reminder_window, font=('Roboto', 18), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
firstdose_entry.place(x=900, y=390, width=110)

seconddose_label = Label(reminder_window, text='2:', font=('Roboto', 18), bg='powderblue', fg='black')
seconddose_label.place(x=625, y=460)

seconddose_entry = Entry(reminder_window, font=('Roboto', 18), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
seconddose_entry.place(x=643, y=460, width=110)

thirddose_label = Label(reminder_window, text='3 ', font=('Roboto', 18), bg='powderblue', fg='black')
thirddose_label.place(x=753, y=460)

thirddose_entry = Entry(reminder_window, font=('Roboto', 18), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
thirddose_entry.place(x=775, y=460, width=110)

fourthdose_label = Label(reminder_window, text='4 ', font=('Roboto', 18), bg='powderblue', fg='black')
fourthdose_label.place(x=878, y=460)

fourthdose_entry = Entry(reminder_window, font=('Roboto', 18), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
fourthdose_entry.place(x=897, y=460, width=110)

firstdose_button = Button(reminder_window, text="Apply Reminder", font=('Roboto', 18), bg='slategrey', fg='black', command=apply_reminder)
firstdose_button.grid(row=1, column=0, columnspan=2, pady=10)
firstdose_button.place(x=525, y=550, width=260)

onemoremed_label = Label(reminder_window, text='Click Here to add more reminders', font=('Roboto', 14), fg='teal', bg='powderblue', cursor='hand2')
onemoremed_label.place(x=670, y=620, width=350)
onemoremed_label.bind('<Button-1>', lambda event: open_new_reminder_page())
onemoremed_label.bind('<Enter>', on_enter)
onemoremed_label.bind('<Leave>', on_leave)

codeuq_label = Label(reminder_window, text='ID:', font=('Roboto', 15), bg='powderblue', fg='black')
codeuq_label.place(x=160, y=60)

codeuq_entry = Entry(reminder_window, font=('Roboto', 18), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
codeuq_entry.place(x=200, y=60, width=70)
if initial_user_code:
    codeuq_entry.insert(0, initial_user_code)
    
codeuq_label.config(state='disabled')
codeuq_label.configure(bg=reminder_window['bg'], fg=reminder_window['bg'])  # Make label color same as background
codeuq_entry.config(state='disabled')
codeuq_entry.configure(bg=reminder_window['bg'], fg=reminder_window['bg']) 

back_button = Button(reminder_window, text='Back', font=('Roboto', 15), bg='cadetblue', fg='white', bd=0, command=go_back)
back_button.place(x=1100, y=30, width=100)


reminder_window.mainloop()

