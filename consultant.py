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
    consultant_window.withdraw()

def display_doctors():
    selected_doctor = doctor_combobox.get()
    if selected_doctor:
        # Define the dictionary of doctors for each type
        doctors = {
            "Gynecologist": [("Dr. Pooja Gupta", "MBBS, MD (Obstetrics & Gynaecology)", "+91-98765-43210"),
                             ("Dr. Neha Sharma", "MBBS, MS (Obstetrics & Gynaecology)", "+91-87654-32109"),
                             ("Dr. Priya Singh", "MBBS, DGO", "+91-76543-21098")],
            "Neurologist": [("Dr. Rajesh Patel", "MBBS, MD (Neurology)", "+91-98765-43210"),
                            ("Dr. Anjali Desai", "MBBS, MS (Neurology)", "+91-87654-32109"),
                            ("Dr. Mohan Sharma", "MBBS, DM (Neurology)", "+91-76543-21098")],
            "Cardiologist": [("Dr. Manoj Kumar", "MBBS, MD (Cardiology)", "+91-98765-43210"),
                             ("Dr. Shalini Reddy", "MBBS, DM (Cardiology)", "+91-87654-32109"),
                             ("Dr. Vivek Singh", "MBBS, DCard", "+91-76543-21098")],
            "Dermatologist": [("Dr. Deepika Kapoor", "MBBS, MD (Dermatology)", "+91-98765-43210"),
                              ("Dr. Siddharth Verma", "MBBS, DVD", "+91-87654-32109"),
                              ("Dr. Priyanka Singh", "MBBS, DPD", "+91-76543-21098")],
            "Psychiatrist": [("Dr. Rahul Gupta", "MBBS, MD (Psychiatry)", "+91-98765-43210"),
                             ("Dr. Shikha Mehra", "MBBS, DPM", "+91-87654-32109"),
                             ("Dr. Vikram Singh", "MBBS, MD (Psychiatry)", "+91-76543-21098")],
            "Physician": [("Dr. Sunil Kumar", "MBBS", "+91-98765-43210"),
                          ("Dr. Nisha Singh", "MBBS", "+91-87654-32109"),
                          ("Dr. Ajay Verma", "MBBS", "+91-76543-21098")],
            "Allergist": [("Dr. Ananya Patel", "MBBS, MD (Allergy)", "+91-98765-43210"),
                          ("Dr. Rohit Sharma", "MBBS, DAll", "+91-87654-32109"),
                          ("Dr. Priyanka Gupta", "MBBS, MD (Allergy)", "+91-76543-21098")],
            "Dentist": [("Dr. Ramesh Gupta", "BDS", "+91-98765-43210"),
                        ("Dr. Preeti Singh", "BDS", "+91-87654-32109"),
                        ("Dr. Ankit Verma", "BDS", "+91-76543-21098")],
            "Surgeon": [("Dr. Neha Reddy", "MBBS, MS (Surgery)", "+91-98765-43210"),
                        ("Dr. Suresh Singh", "MBBS, MS (Surgery)", "+91-87654-32109"),
                        ("Dr. Manisha Sharma", "MBBS, MS (Surgery)", "+91-76543-21098")],
            "Pediatrician": [("Dr. Mohit Gupta", "MBBS, MD (Pediatrics)", "+91-98765-43210"),
                             ("Dr. Sneha Singh", "MBBS, MD (Pediatrics)", "+91-87654-32109"),
                             ("Dr. Rakesh Patel", "MBBS, MD (Pediatrics)", "+91-76543-21098")]
        }

        # Clear previous data
        for widget in data_frame.winfo_children():
            widget.destroy()

        # Column titles
        Label(data_frame, text="Doctor Name", font=('Roboto', 14, 'bold'), bg='white', fg='black').grid(row=0, column=0, padx=10, pady=5, sticky=W)
        Label(data_frame, text="Qualification", font=('Roboto', 14, 'bold'), bg='white', fg='black').grid(row=0, column=1, padx=10, pady=5, sticky=W)
        Label(data_frame, text="Phone Number", font=('Roboto', 14, 'bold'), bg='white', fg='black').grid(row=0, column=2, padx=10, pady=5, sticky=W)

        # Display doctors for the selected type
        for i, (doctor_name, qualifications, phone_number) in enumerate(doctors[selected_doctor], start=1):
            Label(data_frame, text=doctor_name, font=('Roboto', 14), bg='white', fg='black').grid(row=i, column=0, padx=10, pady=5, sticky=W)
            Label(data_frame, text=qualifications, font=('Roboto', 14), bg='white', fg='black').grid(row=i, column=1, padx=10, pady=5, sticky=W)
            Label(data_frame, text=phone_number, font=('Roboto', 14), bg='white', fg='black').grid(row=i, column=2, padx=10, pady=5, sticky=W)

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

consultant_window = Tk()
consultant_window.geometry('1300x680+350+150')
consultant_window.configure(bg='ivory2')
center_window(consultant_window, 1300, 680)
consultant_window.resizable(0, 0)
consultant_window.title("Period Tracker")


bgImage = PhotoImage(file='mini_project/images/reports.png')
bgLabel = Label(consultant_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)


doctor_combobox = Combobox(consultant_window, font=('Roboto', 16), state="readonly", values=[
    "Gynecologist", "Neurologist", "Cardiologist", "Dermatologist", "Psychiatrist",
    "Physician", "Allergist", "Dentist", "Surgeon", "Pediatrician"
])
doctor_combobox.place(x=400, y=100, width=300)


display_button = Button(consultant_window, text='Display Doctors', font=('Roboto', 15), bg='orchid', fg='white', bd=0, command=display_doctors)
display_button.place(x=720, y=100, width=200)

data_frame = Frame(consultant_window, bg='white')
data_frame.place(x=250, y=180, width=800, height=300)

back_button = Button(consultant_window, text='Back', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0, command=go_back)
back_button.place(x=1100, y=60, width=100)

codeuq_label = Label(consultant_window, text='ID:', font=('Roboto', 14), bg='white', fg='black')
codeuq_label.place(x=75, y=60)
codeuq_entry = Entry(consultant_window, font=('Roboto', 14), bg='white', fg='black', highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
codeuq_entry.place(x=126, y=60, width=70)
if initial_user_code:
    codeuq_entry.insert(0, initial_user_code)
    
codeuq_label.config(state='disabled')
codeuq_label.configure(bg=consultant_window['bg'], fg=consultant_window['bg'])  # Make label color same as background
codeuq_entry.config(state='disabled')
codeuq_entry.configure(bg=consultant_window['bg'], fg=consultant_window['bg']) 

consultant_window.mainloop()

