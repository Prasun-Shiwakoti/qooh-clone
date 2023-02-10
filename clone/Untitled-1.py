import mysql.connector as mysql
mydb=mysql.connect(
    host='localhost',
    user='root',
    password='prasun12',
    database='scerectchat',
    auth_plugin='mysql_native_password',
)
mycursor=mydb.cursor()

def insert_data():
    username='Prachi'
    inbox='Hello from the creater'
    notifications=0
    replies='no replies yet'

    value='VALUES'+'("'+str(username)+'","'+str(notifications)+'","'+str(inbox)+'","'+str(replies)+'")'
    print(value)
    line='INSERT INTO clone_users (username, notifications, inbox, replies) '+value
    mycursor.execute(line)
    mydb.commit()
    mydb.close()

insert_data()