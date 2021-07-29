from django.shortcuts import render

# Create your views here.



def keeprecord(request):
    return render(request, 'keeprecord.html', context={})