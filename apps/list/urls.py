from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^add_item$', views.add_item),
    url(r'^create$', views.create),
    url(r'^show/(?P<item_id>\d+)$', views.show),
    url(r'^(?P<item_id>\d+)/add_wishlist$', views.add_wishlist),
    url(r'^(?P<item_id>\d+)/remove_wishlist$', views.remove_wishlist),
    url(r'^(?P<item_id>\d+)/delete$', views.delete),
]
