from django.urls import path
from .views import user_list, user_detail, options, login_user, register_user, add_friend, remove_friend, user_friends, all_users
from .views import MyProfileUpdateAPIView, PersonalInfoUpdateAPIView, UserProfileAPIView, UserProfileView, UserProfileUpdateAPIView, ProfileUpdateAPIView, PostCreateAPIView, PostListAPIView, UserPostListAPIView


urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('options/', options, name='options'),
    path('login', login_user, name='login'),
    path('register', register_user, name='register_user'),
    path('add_friend/<int:pk>/', add_friend, name='add-friend'),
    path('remove_friend/<int:pk>/', remove_friend, name='remove-friend'),
    path('users/<int:user_id>/friends/', user_friends, name='user-friends'),
    path('users', all_users, name='all-users'),
    path('api/my-profile/', MyProfileUpdateAPIView.as_view(), name='my-profile-update'),
    path('api/personal-info/', PersonalInfoUpdateAPIView.as_view(), name='personal-info-update'),
    path('user/profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('user/profiles/<str:username>/', UserProfileView.as_view(), name='user-profile'),

    path('user/profile/update/<str:username>/', UserProfileUpdateAPIView.as_view(), name='user-profile-update'),
    path('profile/update/<str:username>/', ProfileUpdateAPIView.as_view(), name='profile-update'),

    path('posts/user/<str:username>/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/all/', PostListAPIView.as_view(), name='post-list'),
    path('posts/user/<str:username>/', UserPostListAPIView.as_view(), name='user-post-list'),

]
