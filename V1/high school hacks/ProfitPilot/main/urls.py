from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

#main/urls.py
urlpatterns = [
    #path('', . (), name="")
    path('', views.index, name='index'),

    path('stk/<str:symbol>/', views.search, name='stocks_detail'),

    path('usr/singup/', views.SignupPage, name='singup'),

    path('usr/login/', views.LoginPage, name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('reset_pass/', auth_views.PasswordResetView.as_view(template_name="main/email_pass_reset.html"), name="reset_password"),

    path('reset_pass_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path('reset_pass_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('candlestick-chart/', views.candlestick_chart, name='candlestick_chart'),
]   
