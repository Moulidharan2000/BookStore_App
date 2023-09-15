from django.urls import path
from user import views

urlpatterns = [
    path("create_user/", views.UserRegister.as_view(), name="register"),
    path("login_user/", views.LoginUser.as_view(), name="login"),
    path("forgot_password/", views.ForgotPassword.as_view(), name="forgot_pass"),
    path("reset_password/", views.PasswordReset.as_view(), name="reset_pass"),
    path("verify/", views.VerifyUser.as_view(), name="verify_user")
]
