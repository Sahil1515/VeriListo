from django.shortcuts import render

# Create your views here.

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']

        print(name,email,message)
    return render(request, 'contact.html',context={})