from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("link", views.add_link, name="add-link"),
    path("<str:new_link>", views.redirect_website, name="redirect-website"),
    path("grouped-data/in-general", views.grouped_data_in_general, name="general-group"),
    path("grouped-data/each-client", views.grouped_data_each_client, name="each-group")
]
