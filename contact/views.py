from django.shortcuts import render


import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.http.response import HttpResponse

# Create your views here.

def contact(request):
    return render(request, 'contact.html')


def send_mail(name, email,message_user):
    print("\n\n\n")
    print(name)
    print(email)
    print(message_user)
    print("\n\n\n")

    sender_email = os.environ.get("SENDER_EMAIL")
    receiver_email = 'sahilsaini51671@gmail.com'
    password = os.environ.get("SENDER_PASS")

    message = MIMEMultipart("alternative")
    message["Subject"] = "VeriListo Feedback"
    message["From"] = sender_email
    message["To"] = 'sahilsaini51671@gmail.com'

    # Create the plain-text and HTML version of your message
    html = """\
    <html>

    <body>
        <p> Hey,</p>
        <p>Feedback message:  {0} </p>
        <p>Name: {1}</p>
        <p>Email: {2}</p>
        VeriListo
    </body>
    </html>
    """.format(message_user, name, email)

    part2 = MIMEText(html, "html")

    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def send_mail_by_user(request):
    print("send_mail_by_user\n")
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']

    # mail code here
    send_mail(name, email,message)

    print("mail sent!\n")

    return HttpResponse(True)


# OTP Part code ends here\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



# Hello Sahil! This website is awesome. I just love it!