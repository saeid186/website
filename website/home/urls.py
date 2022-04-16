from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.all_product, name='product'),
    path('detail/<int:id>/', views.product_detail, name='detail'),
    path('category/<slug>/<int:id>/', views.all_product, name='category'),
    path('search/', views.product_search, name='product_search'),
    path('favoutit/<int:id>/', views.favourite_product, name='favourite'),
    path('contact/', views.contact, name='contact'),
    path('like/<int:id>/', views.product_like, name='product_like'),
    path('unlike/<int:id>/', views.product_unlike, name='product_unlike'),
    path('comment/<int:id>/', views.product_comment, name='product_comment'),
    path('reply/<int:id>/<int:comment_id>/', views.product_reply, name='product_reply'),
    path('test/', views.test, name='test'),
]
