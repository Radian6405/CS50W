from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="create_listing"),
    path("listings/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment", views.comment, name="comment"),
    path("bid", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.categoryPage, name="category page")
]
