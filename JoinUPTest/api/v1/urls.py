from django.urls import path
from rest_framework.authtoken import views
from JoinUPTest.views import UserDetailAPI, RegisterUserAPIView, ActivationView

urlpatterns = [
    path('login', views.obtain_auth_token,name="login"),
    path("profile", UserDetailAPI.as_view(), name="profile"),
    path("signup", RegisterUserAPIView.as_view(), name="signup"),
    path("activation/<str:code>", ActivationView.as_view(), name="activation"),
]
