from rest_framework import routers

from .viewsets import UserViewset, ProfileViewset

router = routers.DefaultRouter()

router.register("users", UserViewset)
router.register("profiles", ProfileViewset)