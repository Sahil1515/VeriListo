from django.http.response import HttpResponse
from django.shortcuts import render

import pyrebase
import json
from . import forms
import random
import os


import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import environ
# Initialise environment variables


from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin


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
    
# firebase_admin.initialize_app(cred)
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


print(firebaseConfig)

firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()


def SignUp(request):
    form = forms.signupPage()
    context = {'form': form, }
    return render(request, 'signup.html', context=context)


# Creating the user after verification starts/////////////////////////////////////////////
def checkUser(email):
    print("check_user")
    allusers = db.collection("AllUsers").document(
        'allusers').get().to_dict()['allusers']
    if email not in allusers:
        return False
    return True


def check_user_api(request):
    print("check_user_api")
    email = request.POST['email']
    return HttpResponse(checkUser(email))


def makeUserDocInDatabase(username, email):
    print("makeUserDocInDatabase")
    allusers = db.collection("AllUsers").document(
        'allusers').get().to_dict()['allusers']

    if email not in allusers:
        print('Username check')
        allusers.append(email)
        db.collection("AllUsers").document('allusers').set(
            {'allusers': allusers}, merge=True)
        data_to_set = {
            "username": username,
            "email": email,
        }
        db.collection("Profiles").document().set(data_to_set, merge=True)
        print('Username check return true')


def create_user_after_verification(request):
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']

    msg = "User Created in the database"

    user_exists = checkUser(email)

    if user_exists:
        msg = "Email already taken!"
    else:
        try:
            user = authe.create_user_with_email_and_password(email, password)
            makeUserDocInDatabase(username, email)
            # request.session['email']=email
            # request.session['username']=username

        except Exception as e:
            msg = json.loads(e.args[1])['error']['message']
    return HttpResponse(msg)
# Creating the user after verification ends\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


# OTP Part code starts here//////////////////////////////////////////////
def generate_otp():
    print("In generate OTP function")
    otp = random.random()
    otp = int(otp*1000000)
    print("Otp:"+str(otp))

    return otp


def send_mail(otp, user, email):
    sender_email = os.environ.get("SENDER_EMAIL")
    receiver_email = email
    password = os.environ.get("SENDER_PASS")

    message = MIMEMultipart("alternative")
    message["Subject"] = "VeriListo Verification Code"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    html = """\
    <html>

    <body>
        <p> Hi {0},</p>
        <p>We received a request to access your Google account {1} through your emial address. </p>
        <p>Your One-Time-Password is: <br> </p>
        <h2 style="padding-left: 20%;">{2}</h2>
        <p>Don't share it with anyone.</p>
        <p>Regards,</p>
        VeriListo
    </body>

    </html>
    """.format(user, email, otp)

    part2 = MIMEText(html, "html")

    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def send_otp(request):
    email = request.POST['email']
    username = request.POST['username']

    otp = generate_otp()
    # mail code here
    send_mail(otp, username, email)
    return HttpResponse(otp)

# OTP Part code ends here\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
