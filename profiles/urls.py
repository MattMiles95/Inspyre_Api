from django.urls import path
from profiles import views
from profiles.views import FollowersListView, FollowingListView

urlpatterns = [
    # Profiles
    path("profiles/", views.ProfileList.as_view()),
    path("profiles/<int:pk>/", views.ProfileDetail.as_view()),
    path("profiles/<int:pk>/followers/", FollowersListView.as_view()),
    path("profiles/<int:pk>/following/", FollowingListView.as_view()),

    # Profile Tags
    path("profile-tags/", views.ProfileTagListView.as_view()),
    
    # Account
    path("users/delete/", views.UserDeleteView.as_view(), name="user-delete"),
]
