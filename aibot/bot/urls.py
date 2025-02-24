from django.urls import path
from .views import chatbot_view, chat_response,payment_view,home,login_view,sign_up,logout_view,success,admin_view,handle_yes,admin_login_view

urlpatterns = [
    path('chatbot/', chatbot_view, name='chatbot_view'),
    path('chat/', chat_response, name='chat_response'),
    path('payment',payment_view,name="payment"),
    path('',home,name="home"),
    path("login",login_view,name="login"),
    path('signup',sign_up,name="signup"),
    path('logout',logout_view,name="logout"),
    path('success', success, name='success'),
    path('admin_view',admin_view,name="admin_view"),
    path('yes_view_payment/',handle_yes,name="handle_yes"),
    path("admin_login_view",admin_login_view,name="admin_login_view"),
]
