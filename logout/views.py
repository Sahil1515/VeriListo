from django.shortcuts import redirect

def logout(request):
    try:
        del request.session['email']
        del request.session['username']
    except:
        pass
    return redirect('http://localhost:8000/login')
    
