from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('restaurants', views.RestaurantView)
router1 = DefaultRouter()
router1.register('menus', views.MenuView)
urlpatterns = [
    path('', include(router.urls)),
    path('menu/', include(router1.urls)),
]
