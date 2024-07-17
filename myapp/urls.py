from django.urls import path
from . import views

urlpatterns = [

 path('', views.chatPage, name='chatPage'),
 # path('login/', views.loginuser(), name='loginuser'),
 path('base/', views.base, name='base'),
 # path('signup/', views.signup, name='signup'),
 path('contactus/', views.contactus, name='contactus'),
 path('', views.userPortfolio, name='userPortfolio'),
 path('<int:project_id>/', views.detailp, name='detailp'),
 path('create/', views.createPortfolio, name='createPortfolio'),
 path('signup/', views.signup_view, name='signupuser'),
 path('login/', views.login_view, name='loginuser'),
 path('logout/', views.logoutuser, name='logoutuser'),

 # Home

 # Contactus

 # contactAdmin

 # Personal area
 path('personalArea/', views.personalArea, name='personalArea'),
 path('userSettings/', views.userSettings, name='userSettings'),
 path('editProject/', views.editProject, name='editProject'),
 # app portfolio

 # app blog


 # search
 # scholarship
]
