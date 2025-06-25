from django.urls import path
from .views import RegisterView, ActivateView, EmailSentView, LoginView, LogoutView
app_name = 'accounts'

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('email/sent/', EmailSentView.as_view(), name='email_sent'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
