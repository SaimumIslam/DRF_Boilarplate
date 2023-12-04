from django.urls import path

from .api.routers import router
from .api import views

app_name = "authentication"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]

urlpatterns += router.urls
