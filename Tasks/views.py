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
    arr=[]
    print(doc_id)
    try:
        doc_ref=db.collection("Tasks").document(doc_id).get()
        arr=doc_ref.to_dict()['items']
    except:
        print("Data not found in getItems()")

    return arr

# @csrf_exempt
def index(request):
    if 'email' not in request.session and 'username' not in request.session:
        return redirect('/login')

    username=request.session['username']
    email=request.session['email']
    doc_id=getDocId(email)
            
    items = []       

    if request.method == "POST":
        print("Hey")
        item = request.POST['item']

        insert_data={
            "tag":item,
            "class_name":"unchecked"
        }
        
        # This is whole object containing tag and class
        items=getItems(doc_id)

        # This is only tags array
        arr_of_tags=[]
        for ele in items:
            arr_of_tags.append(ele['tag'])
            
        if(insert_data['tag']!=""):
            if insert_data['tag'] not in arr_of_tags:
                items.append(insert_data)
        
        print(items)
        data = {'items': items}

        db.collection('Tasks').document(doc_id).set(data, merge=True)

    print('Getting arr from database')
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





























# @csrf_exempt
# def updateClass(request):

#     email=request.session['email']
#     doc_id=getDocId(email)

#     if request.method=="POST":
#         username=request.session['username']
#         # email=request.session['email_from_fe']
#         class_name=str(request.POST.get('class_name')).strip()
#         tag=str(request.POST.get('tag')).strip()

#         print(class_name,tag)
        
#         arr=getItems(doc_id)

#         for i in range(len(arr)):
#             if(tag==arr[i]['tag']):
#                 print(arr[i]['class_name'])
#                 arr[i]['class_name']=class_name
#                 print(arr[i]['class_name'])
#                 break

#         data = {'items': arr}
#         db.collection("Tasks").document(doc_id).update(data)
#         context={"data":arr}
        
#     return render(request, 'index.html',context=context)
    


# @csrf_exempt
# def delete(request):
#     doc_id=getDocId(request)
#     if request.method=="POST":
#         username=request.session['username']
#         # email=request.session['email_from_fe']
#         value_of_li=request.POST.get('val')
#         value_of_li=str(value_of_li).strip()

#         arr=getItems(doc_id)

#         # removing the element from the list by checking if present
#         for ele in arr:
#             if(ele['tag']==value_of_li):
#                 print("Yes")
#                 print(len(arr))
#                 arr.remove(ele)
#                 print(len(arr))
#                 break

#         print(arr)
#         data={"items":arr}
#         db.collection("Tasks").document(doc_id).set(data)
#         context={"data":arr}
#     return render(request, 'index.html',context=context)


# # @csrf_exempt
# def index(request):
#     if 'email' not in request.session and 'username' not in request.session:
#         return redirect('/login')

#     username=request.session['username']
#     email=request.session['email']
#     doc_id=getDocId(request)
            
#     items = []       

#     if request.method == "POST":
#         print("Hey")
#         item = request.POST['item']

#         insert_data={
#             "tag":item,
#             "class_name":"unchecked"
#         }
        
#         # This is whole object containing tag and class
#         items=getItems(doc_id)

#         # This is only tags array
#         arr_of_tags=[]
#         for ele in items:
#             arr_of_tags.append(ele['tag'])
            
#         if(insert_data['tag']!=""):
#             if insert_data['tag'] not in arr_of_tags:
#                 items.append(insert_data)
        
#         print(items)
#         data = {'items': items}

#         db.collection('Tasks').document(doc_id).set(data, merge=True)

#     print('Getting arr from database')
#     arr=getItems(doc_id)

#     context={"data":arr,'email':email,'username':username}
#     return render(request, 'index.html',context=context)





# # @csrf_exempt
# def index(request):
#     if 'email' not in request.session and 'username' not in request.session:
#         return redirect('/login')

#     username=request.session['username']
#     email=request.session['email']
#     doc_id=getDocId(email)
#     items=getItems(doc_id)
            
#     print('Getting arr from database')

#     context={"data":items,'email':email,'username':username}
#     return render(request, 'index.html',context=context)


# # This API adds the requested element to the database
# @csrf_exempt
# def insert_task_api(request):
#     email=request.session['email']
#     username=request.session['username']

#     doc_id=getDocId(email)
    
#     items = []       
#     tag = request.POST['tag'] #tag i.e name of the item
#     insert_data={
#         "tag":tag,
#         "class_name":"unchecked"
#     }
    
#     # This is whole object containing tag and class
#     items=getItems(doc_id)
#     # This is only tags array
#     arr_of_tags=[]
#     for ele in items:
#         arr_of_tags.append(ele['tag'])
        
#     if(insert_data['tag']!=""):
#         if insert_data['tag'] not in arr_of_tags:
#             items.append(insert_data)
    
#     print(items)
#     data = {'items': items}
#     db.collection('Tasks').document(doc_id).set(data, merge=True)

#     # return_data={"items":items,"flag":True}

#     # return JsonResponse(return_data)

#     context={"data":items,'email':email,'username':username}
#     return render(request, 'index.html',context=context)
