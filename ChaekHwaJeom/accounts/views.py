from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View
from .helper import send_mail, email_auth_num
from django.template.loader import render_to_string
# from django.core.urlresolvers import reverse_lazy
# from allauth.account.views import PasswordChangeView

from .models import MyUser, MyUserManager
from .forms import MyUserForm, MyUserEditForm, SocialAccountSignUpForm, SocialAccountUpdateForm,MyUserSetPasswordForm,RecoveryPwForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = MyUserForm(request.POST)

        if form.is_valid():
            MyUser.objects.create_user(**form.cleaned_data)

            # 생성한 user의 Pk를 'set_address' view로 넘겨야 한다
            return redirect('set_address')

    else:
        form = MyUserForm()
    return render(request, 'registration/register.html',{'form':form})

def set_address(request):
    if request.method == 'POST':
        # ajax를 사용하여 html에서 도로명 주소 받아오기
        sido = request.POST.get('sido','')
        sigungu = request.POST.get('sigungu','')
        dong = request.POST.get('dong','')
    
        # 방금 생성한 user 객체의 주소 정보 업데이트
        user = MyUser.objects.latest()

        user.sido = sido
        user.sigungu = sigungu
        user.dong = dong
        user.save()

        # login(request, user)
        return redirect('home')

    return render(request,'registration/address.html')

def edit_address(request):
    if request.method == 'POST':
        # ajax를 사용하여 html에서 도로명 주소 받아오기
        sido = request.POST.get('sido','')
        sigungu = request.POST.get('sigungu','')
        dong = request.POST.get('dong','')
    
        # 방금 생성한 user 객체의 주소 정보 업데이트
        user = request.user

        user.sido = sido
        user.sigungu = sigungu
        user.dong = dong
        user.save()

        # login(request, user)
        return redirect('edit')

    return render(request,'registration/edit_address.html')

def socialregister(request):
    profile = request.user
    if request.method=='POST':
        form=SocialAccountUpdateForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
        return redirect('set_address')
    else:
        form=SocialAccountUpdateForm(instance=profile)
    return render(request,'registration/socialregister.html',{'form':form})
    
def mypage(request):
    cur_user = MyUser.objects.get(email=request.user.email)
    return render(request,'books/base.html',{'cur_user':cur_user})


def edit(request):
    user = request.user
    # password_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        form = MyUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('mypage')
    else:
        form = MyUserEditForm(instance=request.user)

    return render(request,'registration/edit.html',{'user_form':form,'user':user})

def pw_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"비밀번호 변경 완료")

            return redirect('edit')
        else:
            messages.error(request,'에러를 수정해주세요.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request,'registration/passwordchange.html',{'password_form':form})

def pw_recovery(request):
    if request.method == "POST":
        form = RecoveryPwForm(None)
        if form.is_valid():
            post = form.save()
            # return redirect('pw_change')
    else:
        form = RecoveryPwForm(None)
    return render(request,'registration/recovery_pw.html',{'form':form})



def sendmail(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    target_user = MyUser.objects.get(username=username, email=email)

    if target_user:
        auth_num = email_auth_num()
        target_user.set_password(auth_num)
        target_user.save()
        messages.success(request, '메일을 발송했습니다!')
        send_mail(
            '비밀번호 찾기 인증메일입니다.',
            [email],
            html=render_to_string('registration/recovery_email.html', {
                'auth_num': auth_num,
            }),
        )
    else:
        messages.error(request,'해당 회원은 없습니다.')
    return redirect('home')
