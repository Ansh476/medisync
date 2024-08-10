from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from subprocess import Popen
from connection import con 


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')


def open_login_page(event):
    Popen(['python', 'mini_project/login.py'])
    signup_window.withdraw()


def on_enter_signup(event):
    signup_button.config(bg='slategray')


def on_leave_signup(event):
    signup_button.config(bg='darkslategray')


def on_link_enter(event):
    backtologin_label['fg'] = 'slategray'


def on_link_leave(event):
    backtologin_label['fg'] = 'black'


def open_user_profile(email):
    # Open user profile page
    Popen(['python', 'mini_project/userprofile.py', email])
    signup_window.withdraw()
    
def open_user_profile(email):
    # Open user profile page and pass the email address
    Popen(['python', 'mini_project/userprofile.py', email])
    signup_window.withdraw()


def sign_up():
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    security_question = security_question_var.get().strip()
    security_answer = secquestion_entry.get().strip()

    if not (email and password and security_question and security_answer):
        messagebox.showwarning("Incomplete Details", "Please fill in all the details.")
    elif password != confirm_password_entry.get().strip():
        messagebox.showwarning("Password Mismatch", "Password and confirm password do not match.")
    else:
        try:
            cursor = con.cursor()

            # Fetch the current maximum value of uqcode
            cursor.execute("SELECT MAX(uqcode) FROM signup")
            max_uqcode = cursor.fetchone()[0]

            # Increment the uqcode by 1
            next_uqcode = max_uqcode + 1 if max_uqcode is not None else 1

            # Insert user's information into the signup table
            insert_query = "INSERT INTO signup (email, password, security_question, security_answer, uqcode) " \
                           "VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (email, password, security_question, security_answer, next_uqcode))
            con.commit()
            cursor.close()
            messagebox.showinfo("Signup Successful", "Sign up successful! Now heading to profile page.")
            open_user_profile(email)  # Pass the email to the profile window
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")




# GUI
signup_window = Tk()
signup_window.geometry('1300x680+350+150')
signup_window.configure(bg='ivory2')
center_window(signup_window, 1300, 680)
signup_window.resizable(0, 0)
signup_window.title("Signup Page")

bgImage = PhotoImage(file='mini_project/images/signupimg.png')
bgLabel = Label(signup_window, image=bgImage, bg='white')
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

titlepg_label = Label(signup_window, text='Sign up', font=('Roboto', 30, 'bold'), bg='white', fg='black')
titlepg_label.place(x=975, y=38)

email_label = Label(signup_window, text='Email:', font=('Roboto', 15), bg='white', fg='black')
email_label.place(x=875, y=100)

email_entry = Entry(signup_window, font=('Roboto', 15), bg='white', fg='black',
                    highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
email_entry.place(x=875, y=130, width=350)

password_label = Label(signup_window, text='Password:', font=('Roboto', 14), bg='white', fg='black')
password_label.place(x=875, y=200)

password_entry = Entry(signup_window, font=('Roboto', 15), bg='white', fg='black',
                       show='*',
                       highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
password_entry.place(x=875, y=230, width=350)

confirm_password_label = Label(signup_window, text='Confirm Password:', font=('Roboto', 14), bg='white', fg='black')
confirm_password_label.place(x=875, y=300)

confirm_password_entry = Entry(signup_window, font=('Roboto', 15), bg='white', fg='black',
                               show='*',
                               highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
confirm_password_entry.place(x=875, y=330, width=350)

security_question_label = Label(signup_window, text='Security Question:', font=('Roboto', 14), bg='white',
                                fg='black')
security_question_label.place(x=875, y=400)

security_questions = ["Which is your favorite place?", "What is your favorite food?",
                      "Which is your favorite movie?"]

security_question_var = StringVar()
security_question_var.set(security_questions[0])
security_question_menu = ttk.Combobox(signup_window, values=security_questions, textvariable=security_question_var,
                                      state='readonly')
security_question_menu.place(x=875, y=430, width=350)

secquestion_entry = Entry(signup_window, font=('Roboto', 15), bg='white', fg='black',
                          highlightbackground='lightgrey', highlightcolor='lightgrey', highlightthickness=2)
secquestion_entry.place(x=875, y=460, width=350)

signup_button = Button(signup_window, text='Sign up', font=('Roboto', 15), bg='darkslategray', fg='white', bd=0,
                       command=sign_up)
signup_button.place(x=938, y=540, width=230)


signup_button.bind('<Enter>', on_enter_signup)
signup_button.bind('<Leave>', on_leave_signup)

backtologin_label = Label(signup_window, text='Login', font=('Roboto', 14), fg='black', bg='white', cursor='hand2')
backtologin_label.place(x=1200, y=10)
backtologin_label.bind('<Button-1>', open_login_page)
backtologin_label.bind('<Enter>', on_link_enter)
backtologin_label.bind('<Leave>', on_link_leave)

signup_window.mainloop()

