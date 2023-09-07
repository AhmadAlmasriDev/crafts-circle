from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('about/', views.AboutPage.as_view(), name='about_page'),
    path('contact/', views.ContactPage.as_view(), name='contact_page'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='item'),
    path('like/<slug:slug>/', views.ItemLike.as_view(), name='item_like'),

]