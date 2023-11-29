from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_listing, name="create"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("watchlist/", views.view_watchlist, name="watchlist"),
    path("manage_watchlist/", views.manage_watchlist, name="manage_watchlist"),
    path("close_listing/", views.close_listing, name="close_listing"),
    path("comment/", views.leave_comment, name="comment"),
    path("category/", views.category, name="category"),
    path("category/<str:category_name>", views.filter, name="filter"),
]
