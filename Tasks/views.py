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
    # print(doc_id)
    return doc_id

def getItems(doc_id):
    data={}
    # print(doc_id)
    try:
        doc_ref=db.collection("Tasks").document(doc_id).get()
        data=doc_ref.to_dict()
        return data
    except:
        print("Data not found in getItems()")

    print("Hello")
    print(data)
    print("Hello")

    return {}

# @csrf_exempt
def index(request):

    flag=False
    # If already logged in then take directly to the login page
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
        print(insert_data)
        # This is whole object containing tag and class
        # print(items_data)
        # print(doc_id)
        items_data=getItems(doc_id)


        if (items_data is not None) and len(items_data)>0  :
            arr=items_data['items']
            flag=True

        # This is only tags array
        arr_of_tags=[]
        if len(arr)>0 :
            for ele in arr:
                arr_of_tags.append(ele['tag'])
            
            if(insert_data['tag']!=""):
                if insert_data['tag'] not in arr_of_tags:
                    items_data['items'].append(insert_data)
                    items_data['total_tasks_added']=items_data['total_tasks_added']+1
        else:
            items_data={
                'items':[insert_data],
                'total_tasks_added':1
            }

        print(items_data)
        data =items_data

        db.collection('Tasks').document(doc_id).set(data, merge=True)

    
    arr=getItems(doc_id)
    print(arr)

    context={"data":arr['items'],'email':email,'username':username}
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
    
    for i in range(len(items['items'])):
        print(i)
        if(tag==items[i]['tag']):
            items[i]['class_name']=class_name
            break

    db.collection("Tasks").document(doc_id).update(items)

    # There could be problem if the server is down , because the frontend will update but not updated in backend, so will have to use multithreading
    # context={"data":items}
    
    return_data={"items":items['items'],"flag":True}
    return JsonResponse(return_data)




@csrf_exempt
def delete_api(request):
    print("\n\n\nHey delete_api")
    email=request.session['email']
    value_of_li=request.POST.get('val')
    value_of_li=str(value_of_li).strip()
    print(value_of_li)

    doc_id=getDocId(email)
    data=getItems(doc_id)

    # removing the element from the list by checking if present
    print(data)
    for ele in data['items']:
        if(ele['tag']==value_of_li):
            data['items'].remove(ele)
            data['total_tasks_added']=data['total_tasks_added']-1
            print("Removed")
            print(data)
            break

    db.collection("Tasks").document(doc_id).set(data)

    return_data={"items":data['items'],"flag":True}

    return JsonResponse(return_data)
