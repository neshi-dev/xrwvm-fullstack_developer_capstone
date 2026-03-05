from django.urls import path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Lägg till / på slutet av namnen här:
    path(route='register/', view=views.registration, name='register'),
    path(route='login/', view=views.login_user, name='login'),
    path(route='logout/', view=views.logout_user, name='logout'),
]
