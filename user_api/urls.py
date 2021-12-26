from django.urls import path

from user_api.views import LoginAPI , GoogleLoginAPI


urlpatterns = [
    path('login/', LoginAPI.as_view(), name = 'Login API'),
    path('google_login/', GoogleLoginAPI.as_view(), name = 'Google Login API'),

]