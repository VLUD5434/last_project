from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('toggle-theme/', views.theme_toggle, name='theme-toggle'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('add-to-cart/<int:game_id>/', views.add_to_cart, name='add_to_cart'),
    path("cart/", views.cart_view, name="cart"),
    path("remove-from-cart/<int:game_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/buy/", views.buy_all, name="buy_all"),
    path("library/", views.library_view, name="library"),
    path("library/game/<int:game_id>/", views.library_detail, name="library_detail"),
    path("library/update-status/<int:game_id>/", views.update_status, name="update_status"),
    path("logout/", views.logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
