from django.urls import path
from . import views

# Create your urls here.

app_name = "users"

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("register", views.UserCreateView.as_view(), name="register"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("user-dashboard", views.UserDashboard.as_view(), name="user_dashboard"),
    path('user-list', views.UserListView.as_view(), name="user_list"),
    path('user-friend_add', views.UserFriendAdd.as_view(), name="user_friend_add"),
    path('user-search-page', views.UserSearchPage.as_view(), name="user_search_page"),
    path('friends-page/<int:pk>/', views.FriendsPageView.as_view(), name="friends_page"),
]
