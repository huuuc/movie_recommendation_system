from django.shortcuts import render
from django.contrib import messages
from .models import User
import base64

# Create your views here.


# µÇÂ¼ÕËºÅ
def sign_in(request):
    if request.method == 'POST':
        account = request.POST.get('login_account')
        password = request.POST.get('login_password')
        if account is not None and password is not None:
            if account == '' or password == '':
                messages.warning(request, 'Account or password is empty')
                return render(request, 'login/index.html')
            user = User.objects.filter(account=account)
            if len(user) != 0 and user[0].password == password:
                messages.success(request, 'Success!')
                return render(request, 'login/index.html')
            else:
                messages.warning(request, 'Incorrect username or password')
                return render(request, 'login/index.html')
    return render(request, 'login/index.html')


# ×¢²áÐÂÕËºÅ
def sign_up(request):
    if request.method == 'POST':
        account = request.POST.get('reg_account')
        password = request.POST.get('reg_password')
        if account is not None and password is not None:
            if account == '' or password == '':
                messages.warning(request, 'Account or password is empty')
                return render(request, 'login/sign_up.html')
            user = User.objects.filter(account=account)
            if len(user) != 0:
                messages.warning(request, 'The account has exist!')
                return render(request, 'login/sign_up.html')
            user = User()
            user.account = account
            user.password = password
            user.save()
            messages.success(request, 'Success!')
            return render(request, 'login/sign_up.html')
    return render(request, 'login/sign_up.html')
