from django.urls import path
from user import views

urlpatterns = [
    path("create_user/", views.UserRegister.as_view(), name="register"),
    path("login_user/", views.LoginUser.as_view(), name="login"),
    path("verify/", views.VerifyUser.as_view(), name="verify_user"),
    path("superuser/", views.VerifySuperuser.as_view(), name="super_user")
]