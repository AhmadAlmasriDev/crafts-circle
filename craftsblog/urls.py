from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='item'),
    path('like/<slug:slug>/', views.ItemLike.as_view(), name='item_like'),

]