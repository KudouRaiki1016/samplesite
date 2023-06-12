from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('old/<int:pk>/', views.old_ProfileDetail.as_view(), name='old-detail-profile'), #古いものだから後で消す
    path('<int:pk>/update/', views.profile_update, name='update-profile'),
    path('follow/', views.follow_view, name='follow'),
    path('<int:pk>/unfollow/', views.unfollow_view, name='unfollow'),
    path('<int:profile_id>/following/', views.followinglist_view, name='list-following'),
    path('<int:profile_id>/follower/', views.followerlist_view, name='list-follower'),
    path('<int:profile_id>/', views.profile_detail_view, name='detail-profile'),
    # path('signupview/', views.signup_view, name='signup-view'),
    # path('orderlist/', views.orderlist_view, name='orderlist-book'),
    # path('orderchange/', views.orderchange_view, name='orderchange-book'),
    # # path('bookorder_append/', views.bookorder_append, name='bookorder-append'),
    # path('bookorder_delete/<int:book_id>', views.bookorder_delete, name='bookorder-delete'),
]
# <slug:〇〇>で、文字列を受け取る