from django.urls import path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Auth routes (with and without trailing slash)
    path(route='register', view=views.registration, name='register'),
    path(route='register/', view=views.registration, name='register_slash'),
    path(route='login', view=views.login_user, name='login'),
    path(route='login/', view=views.login_user, name='login_slash'),
    path(route='logout', view=views.logout_user, name='logout'),
    path(route='logout/', view=views.logout_user, name='logout_slash'),

    # Backend microservice proxy routes
    path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers_no_slash'),
    path(route='get_dealers/<str:state>/', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state_no_slash'),
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),
    path(route='reviews/dealer/<int:dealer_id>/', view=views.get_dealer_reviews, name='get_dealer_reviews'),
    path(route='add_review/', view=views.add_review, name='add_review'),
    path(route='add_review', view=views.add_review, name='add_review_no_slash'),
]
