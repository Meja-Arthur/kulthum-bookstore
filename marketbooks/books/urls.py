from django.contrib.auth.forms import PasswordResetForm
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm, PasswordResetForm


app_name = 'books'

urlpatterns = [
    path('', views.Homepage, name='index'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('download_book/<slug:slug>/', views.download_book, name='download_book'),
    path('payment-success/<slug:slug>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<slug:slug>/', views.paymentFailed, name='payment-failed'),
    path('shop/', views.Shop, name='shop'),
    
    path('shop/category/<int:category_id>/', views.Shop, name='shop_category'),
    
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.Address, name='address'),
    path('search/', views.search_results, name='search'),

  # Login authentications
    # path('registration/', views.registration, name='registration'),
    path('register/', views.CustomRegistrationView.as_view(), name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('password-reset/', auth_view.PasswordResetView.as_view(
        template_name='password_reset.html', form_class=PasswordResetForm), name='password_reset'),
    path('logout/', views.logout_view, name='logout'),






    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog-single/', views.blogSingle, name='blog-single'),
    path('cart/', views.Cart, name='cart'),
    path('checkout/', views.Checkout, name='checkout'),

    # path('product-single/', views.ProductSingle, name='product-single')

]