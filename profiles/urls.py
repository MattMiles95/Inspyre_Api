from django.urls import path
from profiles import views

urlpatterns = [
    path("profiles/", views.ProfileList.as_view()),
    path("profiles/<int:pk>/", views.ProfileDetail.as_view()),
    path("profile-tags/", views.ProfileTagListView.as_view()),
    path("users/delete/", views.UserDeleteView.as_view(), name="user-delete"),
]
