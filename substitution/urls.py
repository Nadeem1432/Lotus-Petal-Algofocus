from django.urls import path

from substitution.views import  GetSubstitution, Addsubstitution

urlpatterns = [
    path('get_substitution/',GetSubstitution.as_view(),name = 'get-substitution'),
    path('add_substitution/', Addsubstitution.as_view(), name='add-substitution')
            ]