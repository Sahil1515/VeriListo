from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse 

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate('./file.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()



def getDocId(email):
    docs_ref=db.collection('Profiles').where('email','==',email).get()
    for doc in docs_ref:
        doc_id=doc.id
    print(doc_id)
    return doc_id

def getItems(doc_id):
    arr={}
    print(doc_id)
    try:
        doc_ref=db.collection("Tasks").document(doc_id).get()
        arr=doc_ref.to_dict()
    except:
        print("Data not found in getItems()")

    print("Hello")
    print(arr)
    print("Hello")

    return arr

# @csrf_exempt
def index(request):

    flag=False
    if 'email' not in request.session and 'username' not in request.session:
        return redirect('/login')

    username=request.session['username']
    email=request.session['email']
    doc_id=getDocId(email)

    arr=[]
            
    items_data = []

    if request.method == "POST":
        print("Hey1")
        item = request.POST['item']

        insert_data={
            "tag":item,
            "class_name":"unchecked"
        }
        print("Hi")
        print(insert_data)
        # This is whole object containing tag and class
        # print(items_data)
        items_data=getItems(doc_id)
        print(items_data)
        if 'items' in items_data.keys() :
            arr=items_data['items']
        flag=True

        # This is only tags array
        arr_of_tags=[]
        if 'items' in items_data.keys() :
            for ele in items_data['items']:
                arr_of_tags.append(ele['tag'])
            
            if(insert_data['tag']!=""):
                if insert_data['tag'] not in arr_of_tags:
                    items_data['items'].append(insert_data)
                    items_data['total_tasks_added']=items_data['total_tasks_added']+1
        else:
            items_data['items']=[]
            items_data['items'].append(insert_data)
            items_data['total_tasks_added']=0

        print(items_data)
        data =items_data

        db.collection('Tasks').document(doc_id).set(data, merge=True)

    print('Getting arr from database')

    if flag is False:
        arr=getItems(doc_id)

    context={"data":arr,'email':email,'username':username}
    return render(request, 'index.html',context=context)







# Takes in class name and tag as input  

@csrf_exempt
def updateClass_api(request):
    email=request.session['email']

    class_name=str(request.POST.get('class_name')).strip()
    tag=str(request.POST.get('tag')).strip()
    print(class_name,tag)
    
    doc_id=getDocId(email)
    items=getItems(doc_id)
    items=items['items']
    
    for i in range(len(items)):
        if(tag==items[i]['tag']):
            print(items[i]['class_name'])
            items[i]['class_name']=class_name
            print(items[i]['class_name'])
            break
    data = {'items': items}
    db.collection("Tasks").document(doc_id).update(data)

    # There could be problem if the server is down , because the frontend will update but not updated in backend
    # context={"data":items}
    
    return_data={"items":items,"flag":True}
    return JsonResponse(return_data)


@csrf_exempt
def delete_api(request):
    email=request.session['email']
    value_of_li=request.POST.get('val')
    value_of_li=str(value_of_li).strip()

    doc_id=getDocId(email)
    items=getItems(doc_id)

    # removing the element from the list by checking if present
    for ele in items:
        if(ele['tag']==value_of_li):
            print("Yes")
            print(len(items))
            items.remove(ele)
            print(len(items))
            break
    print(items)

    data={"items":items}
    db.collection("Tasks").document(doc_id).set(data)

    return_data={"items":items,"flag":True}

    return JsonResponse(return_data)
