from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth

# Create your views here.

def register(request):
    if request.method=='GET':
        return render(request, 'registration.html',{'Username':'Your Username', 'email': 'Your Email','pass1':'Password','pass2':'Repeat Your password'})
    else:
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['password']
        pass2=request.POST['re_password']

        if pass1==pass2:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=username, password=pass1, email=email, first_name=fname, last_name=lname)
                    user.save()
                    return render(request, 'login.html', {'placeholder':'Username'})
                else:
                    return render(request, 'registration.html',{'Username':'Your Username', 'email': '-----Email already taken-----','pass1':'Password','pass2':'Repeat Your password'})
            else:
                return render(request, 'registration.html',{'Username':'-----Username already taken-----', 'email': 'Your Email','pass1':'Password','pass2':'Repeat Your password'}) 
        else:
            return render(request, 'registration.html',{'Username':'Your Username', 'email': 'Your Email','pass1':'-----Passwords doesnot match-----','pass2':'-----Passwords doesnot match-----'})

def login(request):
    if request.method=='GET':
        return render(request, 'login.html', {'placeholder':'Username'})
    else:
        username=request.POST['username']
        password=request.POST['pass']

        user=auth.authenticate(username=username, password=password)
        
        if user is not None:
            print(user.is_authenticated)
            auth.login(request, user)
            print(user.is_authenticated)
            return redirect('/travello')
        else:
            return render(request, 'login.html', {'placeholder':'-----User not found-----'})

def logout(request):
    auth.logout(request)
    return redirect('/travello')