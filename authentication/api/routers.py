from rest_framework import routers

from .viewsets import UserViewset, ProfileViewset, BranchViewset, InstituteViewset

router = routers.DefaultRouter()

router.register("users", UserViewset)
router.register("profiles", ProfileViewset)
router.register("branches", BranchViewset)
router.register("institutes", InstituteViewset)