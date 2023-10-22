from django.urls import path
from friends.views.login_view import login_view
from friends.views.sign_up_view import signup
from friends.views.search_users import search_users
from friends.views.get_friends import get_friends
from friends.views.get_pending_requests import get_pending_requests

urlpatterns = [
    path('api/v1/login/', login_view),
    path('api/v1/signup/', signup),
    path("api/v1/search_users/", search_users),
    path('api/v1/get_friends/', get_friends),
    path('api/v1/get_pending_request/', get_pending_requests),

]
