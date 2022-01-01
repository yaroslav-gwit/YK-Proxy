from django.shortcuts import render, redirect

def home(request):
    redirect_url = 'dashboard/'
    return redirect(redirect_url, name="home")

def login(request):
    page_name = "Login"
        
        # if form.is_valid():
        #     
        #     userRole = response.POST.get('UserRole')

    context = {
        'page_name': page_name,
        'firstName': firstName,
        'userRole': userRole,
    }

    return render(request, "login.html", context)