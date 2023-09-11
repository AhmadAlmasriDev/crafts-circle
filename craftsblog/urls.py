from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('filter_by_category/<int:category>', views.CategoryFilter.as_view(), name='category_filter'),
    path('about/', views.AboutPage.as_view(), name='about_page'),
    path('contact/', views.ContactPage.as_view(), name='contact_page'),
    path('favorite/', views.FavoritePage.as_view(), name='favorite_page'),
    path('add_item/', views.AddItem.as_view(), name='add_item'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='item'),
    path('like/<slug:slug>/', views.ItemLike.as_view(), name='item_like'),

]