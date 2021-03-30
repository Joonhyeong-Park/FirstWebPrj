from django import forms
from .models import MyUser,MyUserManager
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm ,SetPasswordForm,ReadOnlyPasswordHashField
from allauth.socialaccount.forms import SignupForm

# user model을 class로 반환
User = get_user_model()

# django user form
class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password','username', 'nickname','profileimage']

class MyUserEditForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username','nickname','profileimage']


# sociallogin form
class SocialAccountSignUpForm(SignupForm):
    class Meta():
        model = MyUser
        fields = ['username', 'nickname','profileimage']
        
    def save(self, request):
        user = super(SocialAccountSignUpForm,self).save(request)
        return user

class SocialAccountUpdateForm(forms.ModelForm):
    class Meta():
        model = MyUser
        fields = ['username', 'nickname', 'profileimage']

class RecoveryPwForm(forms.Form):
    class Meta:
        model = MyUser
        fields = ['username', 'email']
        
    username = forms.CharField(
        widget=forms.TextInput,)
    email = forms.EmailField(
        widget=forms.EmailInput,)

    def __init__(self, *args, **kwargs):
        super(RecoveryPwForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '이름'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_username',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_email',
        })

class MyUserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyUserSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })