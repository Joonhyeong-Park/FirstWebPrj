"""chaekhwajeom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
import books.views
import accounts.views
import chat.views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',books.views.home,name="home"),
    path('mypage/',accounts.views.mypage,name="mypage"),
    path('registration/edit',accounts.views.edit,name="edit"),
    path('registration/pw_change',accounts.views.pw_change,name="pw_change"),
    path('registration/edit_address', accounts.views.edit_address,name='edit_address'),
    path('library/',books.views.user_library,name="library"),
    path('book_detail/<int:pk>/delete', books.views.delete, name="delete"),
    path('book_detail/<int:pk>/', books.views.book_detail, name="book_detail"),
    path('like', books.views.like, name='like'),

    path('book_search/',books.views.book_search,name="book_search"),
    path('book_register/',books.views.book_register,name="book_register"),
    
    path('tagadd/<int:pk>',books.views.tag_add,name="tag_add"),
    path('tagdetail/<int:pk>/',books.views.tag_detail,name="tag_detail"),
  
    path('registration/register/', accounts.views.register, name="register"),
    path('accounts/', include('allauth.urls')),
    path('registration/', include('django.contrib.auth.urls')),
    path('registration/login/', auth_views.LoginView.as_view(),{'template_name':'registration/login.html'},name="login"),
    path('registration/logout/', auth_views.LogoutView.as_view(),{'template_name':'registration/logout.html'},name="logout"),
    path('registration/set_address/',accounts.views.set_address,name="set_address"),
    path('registration/socialregister', accounts.views.socialregister, name="socialregister"),
    # path('recovery/pw/', accounts.views.RecoveryPwView.as_view(), name='recovery_pw'),
    path('recovery/recovery_pw', accounts.views.pw_recovery, name='recovery_pw'),
    path('recovery/sendmail', accounts.views.sendmail, name='sendmail'),
    # path('recovery/pw/find/', accounts.views.ajax_find_pw_view, name='ajax_pw'),
    # path('recovery/pw/auth/', accounts.views.auth_confirm_view, name='recovery_auth'),
    # path('recovery/pw/reset/', accounts.views.auth_pw_reset_view, name='recovery_pw_reset'),

    path('chat/',chat.views.chat,name="chat"),
    path('chat/done/<int:sharing_pk>',chat.views.set_sharing_state,name="set_sharing_state"),
    path('chat/chatroom/<int:sharing_pk>',chat.views.chatroom,name="chatroom"),
    path('chat/list_message/<int:pk>',chat.views.message,name="listMessage"),
    # path('chat/list_message/<char:neighbor_pk>/<int:book_pk>/',chat.views.list_message,name="listMessage"),
    path('sharing/<int:book_pk>/<uuid:neighbor_pk>',chat.views.sharing,name="sharing"),
    # re_path(r'^sharing/(?P<neighbor_pk>[0-9a-f\-]{32,})$/(?P<book_pk>[0-9]+)$',chat.views.sharing,name="sharing"),
    # url(r'^sharing/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/(?P<book_pk>[0-9]+)$',chat.views.sharing,name="sharing"),

    path('service/guideline',chat.views.service_guide,name="service_guide"),
    path('report/',chat.views.report,name="report"),
    path('books/service_manual', books.views.service_manual, name= "service_manual"),
    path('books/neighbor_library', books.views.neighbor_library, name = "neighbor_library"),
    path('books/user_library', books.views.user_library, name="user_library"),
    # path('books/search/newURL',books.views.search,name="pagination"),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)