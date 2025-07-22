from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import profile_create
from django.contrib.auth import views as auth_views
from .views import article_create,article_list
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article/create/', article_create, name='article_create'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),  # ←追加
    path('article/<int:pk>/delete',views.article_delete, name='article_delete'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='article_list'), name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/create/', profile_create, name='profile_create'),
    path('user/<str:username>/', views.profile_detail, name='profile_detail'),
    path('user/<str:username>/articles/',views.user_article_list,name='user_Article_list'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)