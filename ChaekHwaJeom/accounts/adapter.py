
from django.shortcuts import redirect, render, reverse
from django.conf import settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from .models import MyUser
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import login
from django.http import HttpResponseRedirect

class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self,request):
        return reverse('neighbor_library')

class SocialAccountAdapter(DefaultSocialAccountAdapter): 

    def pre_social_login(self, request, sociallogin):

        if sociallogin.user not in MyUser.objects.all():
            self.save_user(request,sociallogin,None)
            # print(MyUser.objects.all())
            user_login = login(request, sociallogin.user, 'django.contrib.auth.backends.ModelBackend')
            raise ImmediateHttpResponse(HttpResponseRedirect(reverse('socialregister')))
        else:
            user_login = login(request, sociallogin.user, 'django.contrib.auth.backends.ModelBackend')
            raise  ImmediateHttpResponse(HttpResponseRedirect(reverse("neighbor_library")))

    def get_connect_redirect_url(self, request, socialaccount):
        url = reverse("socialregister")
        return url


    def save_user(self,request,sociallogin,form=None):
        user = super(SocialAccountAdapter,self).save_user(request,sociallogin,form=form)
        platform = sociallogin.account.provider.upper() #debugging
        if platform == "GOOGLE":
            MyUser.objects.get_or_create_google_user(user_pk=user.pk)
        return user