import mysql.connector as mysql
from django.shortcuts import render,redirect
from . import views

#to insert data
def insert_data(username):

    mydb=mysql.connect(
    host='localhost',
    user='root',
    password='prasun12',
    database='scerectchat',
    auth_plugin='mysql_native_password',
    )
    mycursor=mydb.cursor()

    inbox='Hello from the creater'
    notifications=0
    replies='no replies yet'

    value='VALUES'+'("'+str(username)+'","'+str(notifications)+'","'+str(inbox)+'","'+str(replies)+'")'
    line='INSERT INTO clone_users (username, notifications, inbox, replies) '+value
    mycursor.execute(line)
    mydb.commit()
    mydb.close()
    return True


def update_data(username, message):
    #to update data
    mydb=mysql.connect(
    host='localhost',
    user='root',
    password='prasun12',
    database='scerectchat',
    auth_plugin='mysql_native_password',
    )
    mycursor=mydb.cursor()

    inbox=[]

    mycursor.execute("SELECT * from clone_users")
    datas=mycursor.fetchall()
    for data in datas:
        if data[1].upper()== username.upper():
            inbox=data[3]

    inbox=inbox.split('  ;,  ')
    inbox.insert(0,message)
    notifications=str(len(inbox))
    inbox='  ;,  '.join(inbox)


    line ="UPDATE clone_users SET inbox="+'"'+inbox+'"'+" WHERE username="+'"'+username+'"'
    mycursor.execute(line)
    mydb.commit()

    line ="UPDATE clone_users SET notifications="+'"'+notifications+'"'+" WHERE username="+'"'+username+'"'
    mycursor.execute(line)
    mydb.commit()
    mydb.close()
    return True

def msg_notif(username):
    mydb=mysql.connect(
    host='localhost',
    user='root',
    password='prasun12',
    database='scerectchat',
    auth_plugin='mysql_native_password',
    )
    mycursor=mydb.cursor()
    msg_notif=[]
    mycursor.execute("SELECT * from clone_users")
    datas=mycursor.fetchall()
    for data in datas:
        if data[1]==username:
            msg_notif=[data[3],data[2]]
            return msg_notif



