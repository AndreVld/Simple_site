from django.urls import path
from .views import HomeView, read_post, CreatePostView, UpdatePostView, send_email, Logout, user_login


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('read_post/<slug:slug>/', read_post, ),

    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('update_post/<slug:slug>/', UpdatePostView.as_view(), name='update_post'),

    path('send_email/', send_email, name='send_mail'),

    path('login/', user_login),
    path('logout', Logout.as_view(), name='logout'),

]