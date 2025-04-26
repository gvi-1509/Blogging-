from django.urls import path
from .views import signup_view, login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static
from .views import profile_view, create_post, feed, like_post, add_comment


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

     path('profile/<str:username>/', profile_view, name='profile'),
    path('create/', create_post, name='create_post'),
    path('', feed, name='feed'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('comment/<int:post_id>/', add_comment, name='add_comment'),

]
