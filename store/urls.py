from django.urls import path
from . import views
from rest_framework_nested import routers

# URLConf
router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")
router.register("collections", views.CollectionViewSet, basename="collection")
router.register("carts", views.CartViewSet, basename="cart")

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

urlpatterns = router.urls + products_router.urls
