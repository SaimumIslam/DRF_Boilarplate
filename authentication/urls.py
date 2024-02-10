from django.urls import path

from .api.routers import router
from .api import views

app_name = "authentication"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('permissions/', views.list_permissions, name='list_permissions'),
    path('content-types/', views.list_content_types, name='list_content_types'),
    path('user-groups/', views.UserGroupAPIView.as_view(),
         name='user_group_api_view'),
    path('user-permissions/', views.UserPermissionAPIView.as_view(),
         name='user_permission_api_view'),
    path('group-permissions/', views.GroupPermissionAPIView.as_view(),
         name='group_permission_api_view'),
    path('group-restrictions/', views.GroupRestrictionAPIView.as_view(),
         name='group_restrictions_api_view'),
    path('user-restrictions/', views.UserRestrictionAPIView.as_view(),
         name='user_restrictions_api_view'),
]

urlpatterns += router.urls
