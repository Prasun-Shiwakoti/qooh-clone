from django.shortcuts import render,redirect
from django.contrib.auth.models import auth, User
import mysql.connector
from . import database

username=''
hellouser=''
loggedin=False
searched_user=''
notif_no=[]
msgs=[]
#setup to extract data from database
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='prasun12',
    database='scerectchat',
    auth_plugin='mysql_native_password',
)

mycursor=mydb.cursor()

def user_authenticate(username):
    mycursor.execute("SELECT username from auth_user")
    usernames=mycursor.fetchall()
    print()
    print()
    print(usernames,username)
    for user in usernames:
        if user.count(username)!=0:
            print('duplicate')
            return False
    return True


def email_authenticate(email):    
    mycursor.execute("SELECT email from auth_user")
    emails=mycursor.fetchall()
    print(emails,email)
    for email in emails:
        if email.count(email)!=0:
            return False
    return True


# Login and logout stuffs
def login(request):
    global loggedin, notif_no, msgs
    if request.method=='GET':
        return render(request, 'login.html', {'username':'Username'}) 
    else:
        global hellouser
        username=request.POST['username']
        password=request.POST['pass']
        hellouser=username
        user= auth.authenticate(username=username, password=password)
        if user is not None:
            loggedin=True
            #to show msgs and notification when user logs in 
            msg_notif=database.msg_notif(username)
            msgs=msg_notif[0].split('  ;,  ')
            if msg_notif[1]<5:
                notif=msg_notif[1]
            else:
                notif=5
            notif_no=[]
            for i in range(notif):
                notif_no.append(i)
            return render(request, 'home.html', {'user':hellouser, 'not_homepage':False, 'msgs':msgs, 'notifications':notif_no})
        else:
            return render(request, 'login.html', {'username':'--User Not Found--'})


def register(request):
    if request.method=='GET':
        return render(request, 'registration.html', {'username':'Username', 'email':'Email', 'pass1':'Password', 'pass2':'Retype your password'})
    else:
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['password']
        pass2=request.POST['re_password']

        if pass1==pass2:
            if user_authenticate(username):
                if email_authenticate(email):
                    user=User.objects.create_user(username=username, password=pass1, email=email, first_name=fname, last_name=lname)
                    user.save()
                    database.insert_data(username)
                    return redirect('/')
                else:
                    return render(request, 'registration.html',{'email':'-----Email already taken-----','username':'Username', 'pass1':'Password', 'pass2':'Retype your password'})
            else:
                return render(request, 'registration.html',{'username':'-----Username already taken-----','email':'Email', 'pass1':'Password', 'pass2':'Retype your password'})
        else:
            return render(request,'registration.html',{'pass1':'-----Passwords doesnot match-----','pass2':'-----Passwords doesnot match-----','username':'Username', 'email':'Email'})

def logout(request):
    auth.logout(request)
    return redirect('/')

#Inside the actual app stuffs

def find_user(request):
    global searched_user
    searched_user=request.POST['username']
    
    if not user_authenticate(searched_user):
        return render(request, 'home.html', { 'user':hellouser,'user_found':True, 'not_homepage':True, 'found_user':searched_user, 'notifications':notif_no, 'msgs':msgs, 'inbox':False})
    else:
        return render(request, 'home.html', {'user':hellouser, 'user_found':False, 'not_homepage':True, 'notifications':notif_no, 'msgs':msgs})

def send_message(request):
    if loggedin:
        username=searched_user
        message=request.POST['message']
        database.update_data(username, message)
        return render(request, 'home.html', {'user':hellouser, 'not_homepage':False, 'notifications':notif_no, 'msgs':msgs})

    else:
        return redirect('/')

def inbox(request):
    if loggedin:
        global msgs
        if database.msg_notif(username) == None:
            pass
        else: 
            msgs=database.msg_notif(username)
        #msg=msgs[0].split('  ;,  ')
        return render(request, 'home.html', {'user':hellouser, 'not_homepage':False, 'notifications':notif_no, 'msgs':msgs, 'inbox':True, 'user_found':False})

    else:
        return redirect('/')

