from django.shortcuts import render
import pyrebase
import json
from django.shortcuts import redirect
from django.http.response import HttpResponse

from Login.forms import loginPage

import environ
import os
# Initialise environment variables

# Firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


if not firebase_admin._apps:
    cred = credentials.Certificate(
        os.environ.get("TYPE"),
        os.environ.get("PROJECT_ID"),
        os.environ.get("PRIVATE_KEY_ID"),
        os.environ.get("PRIVATE_KEY"),
        os.environ.get("CLIENT_EMAIL"),
        os.environ.get("CLIENT_ID"),
        os.environ.get("AUTH_URI"),
        os.environ.get("TOKEN_URI"),
        os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
        os.environ.get("CLIENT_X509_CERT_URL")
    )
    firebase_admin.initialize_app(cred)

db = firestore.client()


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


def checkUser(email):
    print("check_user")
    allusers = db.collection("AllUsers").document(
        'allusers').get().to_dict()['allusers']
    if email not in allusers:
        return False
    return True


def login(request):
    form = loginPage()

    # Will be deleted once the user logs out
    if 'email' in request.session and 'username' in request.session and checkUser(request.session['email']):
        # //also check if the user is in the database
        print("\nif condition in login\n")
        print("\nRedirected when session is stored")
        return redirect('http://localhost:8000')

    return render(request, 'login.html', context={"form": form})


def login_api(request):
    print("login_api_function")
    username = ""
    message = "Login successful!"
    print(request.POST)

    flag = False

    email = request.POST['email']
    password = request.POST['password']
    # Else we dont have username
    for doc in db.collection("UserData").where('email', '==', email).stream():
        username = doc.to_dict()['username']
    print(email, username)
    # Validating user in Auth
    try:
        print("login_api_function try block")
        authe.sign_in_with_email_and_password(email, password)
        # With logout
        request.session['email'] = email
        request.session['username'] = username
        flag = True
        # return redirect('http://localhost:8000')
    except Exception as e:
        print("login_api_function except block")
        message = json.loads(e.args[1])['error']['message']
    return HttpResponse(json.dumps({"message": message, "flag": flag}))
