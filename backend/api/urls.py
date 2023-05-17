from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("recipess", views.RecipeViewSet, basename="recipes1")
router.register("tags", views.TagViewSet, basename="tags")
router.register("users", views.UserViewSet, basename="users")
router.register("ingredients", views.IngredientViewSet, basename="ingredients")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
