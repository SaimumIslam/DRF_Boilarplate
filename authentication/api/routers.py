from rest_framework import routers

from .viewsets import UserViewset, ProfileViewset, BranchViewset, InstituteViewset, GroupViewset

router = routers.DefaultRouter()

router.register("users", UserViewset)
router.register("groups", GroupViewset)
router.register("profiles", ProfileViewset)
router.register("branches", BranchViewset)
router.register("institutes", InstituteViewset)