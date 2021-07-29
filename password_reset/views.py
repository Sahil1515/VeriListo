from django.shortcuts import render
from . import forms
from Login.forms import loginPage
import json

from django.http.response import HttpResponse, JsonResponse 

# Create your views here.
import os
import environ
import pyrebase

# Make .env file available globally
env_path = os.path.join(os.path.dirname(__file__), '../.env')
environ.Env.read_env(env_path)

firebaseConfig = {
    # Put your project's data.
    # Project->Settings->General->Firebase SDK snippet(config)->copy
    "apiKey": os.environ.get("APIKEY"),
    "authDomain": os.environ.get("AUTHDOMAIN"),
    "projectId": os.environ.get("PROJECTID"),
    "storageBucket": os.environ.get("STORAGEBUCKET"),
    "messagingSenderId": os.environ.get("MESSAGINGSENDERID"),
    "appId": os.environ.get("APPID"),
    "measurementId": os.environ.get("MEASUREMENTID"),
    "databaseURL": os.environ.get("DATABASEURL")
}



firebase = pyrebase.initialize_app(firebaseConfig)

authe = firebase.auth()


# Initial call to this route
def password_reset(request):
    print("password reset")
    form=forms.password_reset()
    return render(request,'password_reset.html',context={"form":form})


# Api
def send_password_reset_mail(request):
    print("password reset api")
    message="password reset mail sent!"
    flag=False
    email=request.POST['email']
    try:
        print("password reset api try")
        authe.send_password_reset_email(email)
        flag=True
    except Exception as e:
        print("password reset api except")
        message=json.loads(e.args[1])['error']['message']
    
    data={"message":message,"flag":flag}

    print(data)
    return JsonResponse(data)
