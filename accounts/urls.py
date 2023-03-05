from unicodedata import name
from django.urls import path ,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name='accounts'


urlpatterns = [
    path('signup',views.signup ,name='signup'),
    path('signin',views.signin ,name='signin'),
    path('activate_account/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('log_out',views.log_out ,name='log_out'),
    path('profile/<slug:slug>',views.profile ,name='profile'),
    path('profile/<slug:slug>/editprofile',views.edit_profile ,name='edit'),
    path('productfavorites/<str:slug>',views.product_favorites ,name='product_favorites'),
    path('product-favorites',views.showproduct_favorites ,name='showproduct_favorites'),
]
