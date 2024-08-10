import mysql.connector
con = mysql.connector.connect(host='localhost', password ='Ansh@1607', user='root', database='medroutine_management')

if con.is_connected():
    print("Connection established")
    