from django.shortcuts import render

# Create your views here.

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate('./file.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()



def getDocId(request):
    email=request.session['email']
    docs_ref=db.collection('Profiles').where('email','==',email).get()
    for doc in docs_ref:
        doc_id=doc.id
    return doc_id


# Returns all the habits of a person he has added currently
def get_all_habits(doc_id):
    doc_ref=db.collection("Habits").document(doc_id).get()
    habits_data=doc_ref.to_dict() # All habits
    return habits_data


# Main function that renders the page
def analytics(request):
    doc_id=getDocId(request)

    habits_data=get_all_habits(doc_id)

    completed_habits=[]
    if 'completed_habits' in habits_data:
        completed_habits=habits_data['completed_habits']

    return render(request,'analytics.html',context={'completed_habits':completed_habits})
