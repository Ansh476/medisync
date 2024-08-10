from tkinter import *
from tkinter import messagebox, simpledialog
from subprocess import Popen
from connection import con 

# Assuming you have a connection module named 'connection.py'

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')

def open_registration_page(event):
    Popen(['python', 'mini_project/signup.py'])
    login_window.withdraw()

def on_link_enter(event):
    register_label['fg'] = 'darkturquoise'

def on_link_leave(event):
    register_label['fg'] = 'blue'

def on_link_enter_password(event):
    getpassword_label['fg'] = 'darkturquoise'

def on_link_leave_password(event):
    getpassword_label['fg'] = 'blue'

def on_enter(event):
    login_button['bg'] = 'slategray'

def on_leave(event):
    login_button['bg'] = 'darkslategray'

def open_password_recovery(event=None):
    if email_entry.get().strip():  # Check if email entry widget is not empty
        check_email_and_question()
    else:
        # If email entry widget is empty, proceed with asking the user to enter the email in a messagebox
        entered_email = simpledialog.askstring("Enter Email", "Please enter your email:")
        if entered_email:
            try:
                cursor = con.cursor()
                # Retrieve security question based on the entered email
                query = "SELECT security_question FROM signup WHERE email = %s"
                cursor.execute(query, (entered_email,))
                result = cursor.fetchone()
                if result:
                    security_question = result[0]
                    # Display the security question in a messagebox
                    answer = simpledialog.askstring("Security Question", security_question)
                    if answer is not None:
                        check_answer(entered_email, answer)
                else:
                    messagebox.showerror("Error", "Email not found.")
                cursor.close()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

def validate_entries():
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not (email and password):
        messagebox.showerror("Error", "Please fill all the details.")
    else:
        try:
            cursor = con.cursor()

            # Check if email and password exist in the signup table
            signup_query = "SELECT * FROM signup WHERE email = %s AND password = %s"
            cursor.execute(signup_query, (email, password))
            signup_result = cursor.fetchone()

            if signup_result:
                # Get the uqcode from the signup result
                uqcode = signup_result[4]  # Assuming the uqcode is at index 4 in the result tuple

                # Check if the user already exists in mylogin table
                login_query = "SELECT * FROM mylogin WHERE myemail = %s AND mypassword = %s"
                cursor.execute(login_query, (email, password))
                login_result = cursor.fetchone()

                if not login_result:
                    # Insert into mylogin table if the user doesn't exist
                    insert_query = "INSERT INTO mylogin (myemail, mypassword, ucode) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (email, password, uqcode))
                    con.commit()  # Commit the transaction

                # Fetch the ucode from the mylogin table
                cursor.execute("SELECT ucode FROM mylogin WHERE myemail = %s AND mypassword = %s", (email, password))
                ucode_result = cursor.fetchone()

                if ucode_result:
                    ucode = ucode_result[0]

                    # Insert code into database before opening dashboard if it doesn't already exist
                    if not check_code_existence(ucode):
                        insert_code_into_database(ucode)

                    messagebox.showinfo("Login Successful", "Login up successful!")
                    open_dashboard(ucode)
                else:
                    messagebox.showerror("Error", "Failed to retrieve ucode.")
            else:
                messagebox.showerror("Incorrect Details", "Incorrect email or password.")

            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

def open_dashboard(ucode):
    Popen(['python', 'mini_project/dashboard.py', ucode])
    login_window.withdraw()

def check_code_existence(ucode):
    try:
        cursor = con.cursor()
        query = "SELECT * FROM usercode12 WHERE usercodeinp = %s"
        cursor.execute(query, (ucode,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while checking code existence: {str(e)}")
        return False

def insert_code_into_database(ucode):
    try:
        cursor = con.cursor()
        query = "INSERT INTO usercode12 (usercodeinp) VALUES (%s)"
        cursor.execute(query, (ucode,))
        con.commit()
        cursor.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while inserting code into the database: {str(e)}")

def check_email_and_question():
    entered_email = email_entry.get().strip()
    if entered_email:
        try:
            cursor = con.cursor()
            # Retrieve security question based on the entered email
            query = "SELECT security_question FROM signup WHERE email = %s"
            cursor.execute(query, (entered_email,))
            result = cursor.fetchone()
            if result:
                security_question = result[0]
                # Display the security question in a messagebox
                answer = simpledialog.askstring("Security Question", security_question)
                if answer is not None:
                    check_answer(entered_email, answer)
            else:
                messagebox.showerror("Error", "Email not found.")
            cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def check_answer(email, answer):
    try:
        cursor = con.cursor()
        # Retrieve password based on the entered answer
        query = "SELECT password FROM signup WHERE email = %s AND security_answer = %s"
        cursor.execute(query, (email, answer))
        result = cursor.fetchone()
        if result:
            password_entry.delete(0, END)
            password_entry.insert(0, result[0])
            messagebox.showinfo("Password Recovery", "Your password has been successfully retrieved.")
        else:
            messagebox.showerror("Error", "Incorrect answer.")
        cursor.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# GUI
login_window = Tk()
login_window.geometry('1300x680+350+150')
login_window.configure(bg='ivory2')
center_window(login_window, 1300, 680)
login_window.resizable(0, 0)
login_window.title("Login Page")

bgImage = PhotoImage(file='mini_project/images/loginimg1.png')
bgLabel = Label(login_window, image=bgImage, bg='white')
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

logoImage = PhotoImage(file='mini_project/images/logoname.png')
logoLabel = Label(login_window, image=logoImage, bg='white')
logoLabel.place(x=160, y=100) 

email_label = Label(login_window, text='Email:', font=('Roboto', 15), bg='white', fg='black')
email_label.place(x=206, y=225)

email_entry = Entry(login_window, font=('Roboto', 14), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
email_entry.place(x=210, y=250, width=320)

password_label = Label(login_window, text='Password:', font=('Roboto', 14), bg='white', fg='black')
password_label.place(x=206, y=282)

password_entry = Entry(login_window, font=('Roboto', 15), bg='white', fg='black',
                       show='*', 
                       highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
password_entry.place(x=210, y=306, width=320)

login_button = Button(login_window, text='Login', font=('Roboto', 14), bg='darkslategray', fg='white', bd=0, command=validate_entries)
login_button.place(x=210, y=348, width=320)

login_button.bind('<Enter>', on_enter)
login_button.bind('<Leave>', on_leave)

register_label = Label(login_window, text="Don't have an account?", font=('Roboto', 12), bg='white', fg='black')
register_label.place(x=206, y=395)

register_label = Label(login_window, text='Register here', font=('Roboto', 12,), fg='blue', bg='white', cursor='hand2')
register_label.place(x=375, y=395)
register_label.bind('<Button-1>', open_registration_page)
register_label.bind('<Enter>', on_link_enter)
register_label.bind('<Leave>', on_link_leave)

getpassword_label = Label(login_window, text="Forgot Password?", font=('Roboto', 12), bg='white', fg='black')
getpassword_label.place(x=206, y=425)

getpassword_label = Label(login_window, text='Click Here', font=('Roboto', 12,), fg='blue', bg='white', cursor='hand2')
getpassword_label.place(x=342, y=425)
getpassword_label.bind('<Button-1>', open_password_recovery)
getpassword_label.bind('<Enter>', on_link_enter_password)
getpassword_label.bind('<Leave>', on_link_leave_password)

login_window.mainloop()
