from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account


# Create your views here.
def register(request):
    if request =='POST':
        form = RegistrationForm(request.POST)
        print(f"&&&&&&&&&&&, {form.is_valid()}")
        print(f"Cleaned data: {form.cleaned_data}")
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            phone_number = form.cleaned_data['phone_number']
            user = Account.objects.create_user(
                first_name="first_name", last_name="last_name",
                email="test@example.com", username="username", password="password")
            user.phone_number = phone_number
            user.save()
    else:
        form = RegistrationForm()
    context = {
        'form' : form, 
    }
    return render (request, 'accounts/register.html', context)


def login(request):
    return render (request, 'accounts/login.html')


def logout(request):
    return