from django.urls import path
from .views import product_list, add_product,admin_products,admin_categories,add_category,edit_category,delete_category, edit_product, delete_product, product_detail, signup_view, login_view, logout_view

urlpatterns = [
   path('', product_list, name='product_list'),
    path('product_list/add/', add_product, name='add_product'),
    path('admin_products/', admin_products, name='admin_products'),
    path('product_list/edit/<int:pk>/', edit_product, name='edit_product'),
    path('admin_products/delete/<int:pk>/', delete_product, name='delete_product'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('categories/', admin_categories, name='admin_categories'),
    path('categories/add/', add_category, name='add_category'),
    path('categories/edit/<int:pk>/', edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', delete_category, name='delete_category'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
