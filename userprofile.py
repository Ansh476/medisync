from tkinter import *
from tkinter import messagebox, PhotoImage
from tkcalendar import Calendar
from subprocess import Popen
from connection import con
import sys

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
    profile_window.withdraw()

def get_date():
    def on_date_select():
        selected_date = cal.get_date()
        if selected_date:
            DOB_entry.delete(0, END)
            DOB_entry.insert(0, selected_date)
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

def validate_age(new_value):
    if new_value.isdigit() and len(new_value) <= 2 or new_value == "":
        return True
    else:
        messagebox.showerror("Error", "Invalid age! Please enter up to two digits.")
        return False

def validate_contact(new_value):
    if new_value.isdigit() and len(new_value) <= 10 or new_value == "":
        return True
    else:
        messagebox.showerror("Error", "Invalid phone number! Please enter only digits with a maximum length of 10.")
        return False

def select_gender(gender):
    gender_var.set(gender)
    
def on_entry_click(event):
    if height_entry.get() == "5'10''":
        height_entry.delete(0, END)
        height_entry.config(fg='black')

def on_entry_leave(event):
    if height_entry.get() == '':
        height_entry.insert(0, "5'10''")
        height_entry.config(fg='grey')
        
def validate_weight(new_value):
    if new_value.isdigit() and len(new_value) <= 3 or new_value == "":
        return True
    else:
        messagebox.showerror("Error", "Invalid weight! Please enter up to three digits.")
        return False
    
def populate_profile_fields(codeuq):
    try:
        cursor = con.cursor()
        # Retrieve profile information from the database based on codeuq
        select_query = "SELECT full_name, DOB, Age, Gender, Address, Phone, Height, Weight, Blood_group FROM userprofile WHERE codeunq = %s"
        cursor.execute(select_query, (codeuq,))
        profile_data = cursor.fetchone()  # Assuming only one row is returned

        if profile_data:
            # Populate the entry fields with the retrieved data
            fullname_entry.delete(0, END)
            fullname_entry.insert(0, profile_data[0])

            DOB_entry.delete(0, END)
            DOB_entry.insert(0, profile_data[1])

            age_entry.delete(0, END)
            age_entry.insert(0, profile_data[2])

            # Assuming gender_var is a global variable for Radiobutton selection
            gender_var.set(profile_data[3])

            address_entry.delete("1.0", END)
            address_entry.insert("1.0", profile_data[4])

            contact_entry.delete(0, END)
            contact_entry.insert(0, profile_data[5])

            height_entry.delete(0, END)
            height_entry.insert(0, profile_data[6])

            weight_entry.delete(0, END)
            weight_entry.insert(0, profile_data[7])

            blood_group_entry.delete(0, END)
            blood_group_entry.insert(0, profile_data[8])

        else:
            messagebox.showwarning("Profile Not Found", "No profile found for the provided code.")

        cursor.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {str(e)}")

def save_profile(email, fullname_entry, DOB_entry, age_entry, gender_var, address_entry, contact_entry, height_entry, weight_entry, blood_group_entry,codeuq):
    # Retrieve values from entry fields
    full_name = fullname_entry.get().strip()
    dob = DOB_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_var.get().strip()
    address = address_entry.get("1.0", "end-1c").strip()
    contact = contact_entry.get().strip()
    height = height_entry.get().strip()
    weight = weight_entry.get().strip()
    blood_group = blood_group_entry.get().strip()
    codeuq = codeuq_entry.get().strip()

    # Check if all fields are filled
    if not (full_name and dob and age and gender and address and contact and height and weight and blood_group):
        messagebox.showwarning("Incomplete Details", "Please fill in all the details.")
        return

    try:
        cursor = con.cursor()
        # Insert profile information into the profile table
        insert_query = "INSERT INTO userprofile (full_name, DOB, Age, Gender, Address, Phone, Height, Weight, Blood_group,codeunq, email_of_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (full_name, dob, age, gender, address, contact, height, weight, blood_group,codeuq, email))
        con.commit()
        cursor.close()
        messagebox.showinfo("Profile Saved", "Profile saved successfully.")
        open_dashboard()
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {str(e)}")

def open_dashboard():
    # Open the dashboard page here
    # For demonstration, let's assume opening dashboard.py using Popen
    Popen(['python', 'mini_project/dashboard.py'])
    profile_window.withdraw()

# GUI
profile_window = Tk()
profile_window.geometry('1300x680+350+150')
profile_window.configure(bg='ivory2')
center_window(profile_window, 1300, 680)
profile_window.resizable(0, 0)
profile_window.title("Profile Page")

bgImage = PhotoImage(file='mini_project/images/profile.png')

# Resize the image
width = 691  # Adjust as needed
height = 600  # Adjust as needed
bgImage = bgImage.subsample(bgImage.width() // width, bgImage.height() // height)

bgLabel = Label(profile_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

fullname_label = Label(profile_window, text='Full Name:', font=('Roboto', 15), bg='white', fg='black')
fullname_label.place(x=360, y=95)

fullname_entry = Entry(profile_window, font=('Roboto', 14), bg='white', fg='black',
                      highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2)
fullname_entry.place(x=480, y=95, width=400)

DOB_label = Label(profile_window, text='DOB       :', font=('Roboto', 15), bg='white', fg='black')
DOB_label.place(x=360, y=145)

DOB_entry = Entry(profile_window, font=('Roboto', 14), bg='white', fg='black',
                  highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2)
DOB_entry.place(x=480, y=145, width=227)

DOB_button = Button(profile_window, text="Select Date", command=get_date)
DOB_button.place(x=740, y=145, width=100)

age_label = Label(profile_window, text='Age        :', font=('Roboto', 15), bg='white', fg='black')
age_label.place(x=360, y=195)

validate_age_command = profile_window.register(validate_age)
age_entry = Entry(profile_window, font=('Roboto', 14), bg='white', fg='black',
                  highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2,
                  validate="key", validatecommand=(validate_age_command, '%P'))
age_entry.place(x=480, y=195, width=227)

gender_label = Label(profile_window, text='Gender   :', font=('Roboto', 15), bg='white', fg='black')
gender_label.place(x=360, y=245)

gender_var = StringVar()
gender_radio_frame = Frame(profile_window, bg='white')

male_button = Radiobutton(gender_radio_frame, text="Male", variable=gender_var, value="Male", font=('Roboto', 12),
                          bg='white', fg='black', command=lambda: select_gender("Male"))
female_button = Radiobutton(gender_radio_frame, text="Female", variable=gender_var, value="Female", font=('Roboto', 12),
                            bg='white', fg='black', command=lambda: select_gender("Female"))
other_button = Radiobutton(gender_radio_frame, text="Other", variable=gender_var, value="Other", font=('Roboto', 12),
                           bg='white', fg='black', command=lambda: select_gender("Other"))

male_button.pack(side=LEFT, padx=5)
female_button.pack(side=LEFT, padx=5)
other_button.pack(side=LEFT, padx=5)

gender_radio_frame.place(x=480, y=245)

address_label = Label(profile_window, text='Address  :', font=('Roboto', 15), bg='white', fg='black')
address_label.place(x=360, y=295)

address_entry = Text(profile_window, font=('Roboto', 14), bg='white', fg='black',
                     highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2,
                     height=3, wrap=WORD)
address_entry.place(x=480, y=295, width=400)

contact_label = Label(profile_window, text='Phone     :', font=('Roboto', 15), bg='white', fg='black')
contact_label.place(x=360, y=390)

validate_contact_command = profile_window.register(validate_contact)
contact_entry = Entry(profile_window, font=('Roboto', 14), bg='white', fg='black',
                      highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2,
                      validate="key", validatecommand=(validate_contact_command, '%P'))
contact_entry.place(x=480, y=390, width=227)

height_label = Label(profile_window, text='Height(ft) :', font=('Roboto', 15), bg='white', fg='black')
height_label.place(x=360, y=442)

height_entry = Entry(profile_window, font=('Roboto', 14), bg='white', fg='grey',
                     highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2)
height_entry.place(x=480, y=442, width=227)

# Inserting the reference height and setting the color to grey
height_entry.insert(0, "5'10''")
height_entry.bind("<FocusIn>", on_entry_click)
height_entry.bind("<FocusOut>", on_entry_leave)

weight_label = Label(profile_window, text='Weight(kg) :', font=('Roboto', 15), bg='white', fg='black')
weight_label.place(x=360, y=495)

validate_weight_command = profile_window.register(validate_weight)
weight_entry = Entry(profile_window, font=('Roboto', 14),  bg='white', fg='black',
    highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2,validate="key", validatecommand=(validate_weight_command, '%P'))
weight_entry.place(x=480, y=495, width=227)

blood_group_label = Label(profile_window, text='Blood Group:', font=('Roboto', 15), bg='white', fg='black')
blood_group_label.place(x=360, y=550)

blood_group_entry = Entry(profile_window, font=('Roboto', 14),  bg='white', fg='black',
    highlightbackground='lightgrey', highlightcolor='darkslategray', highlightthickness=2)

blood_group_entry.place(x=480, y=550, width=227)

codeuq_label = Label(profile_window, text='ID:', font=('Roboto', 14), bg='white', fg='black')
codeuq_label.place(x=50, y=30)
codeuq_entry = Entry(profile_window, font=('Roboto', 14), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
codeuq_entry.place(x=100, y=30, width=70)


email = sys.argv[1] if len(sys.argv) > 1 else None  # Retrieve email from sys.argv if available

populate_button = Button(profile_window, text='Populate Profile', font=('Roboto', 12), bg='darkslategray', fg='white', command=lambda: populate_profile_fields(codeuq_entry.get()))
populate_button.place(x=1000, y=600, width=200)

# Button to save profile
submit_button = Button(profile_window, text='Submit', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0,
                       command=lambda: save_profile(fullname_entry, DOB_entry, age_entry, gender_var, address_entry, contact_entry, height_entry, weight_entry, blood_group_entry, codeuq_entry, email))
submit_button.place(x=530, y=600, width=230)

back_button = Button(profile_window, text='Back', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0, command=go_back)
back_button.place(x=1100, y=30, width=100)

profile_window.mainloop()


