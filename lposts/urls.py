from django.urls import path, include

from lposts import views

urlpatterns = [
    path('', views.LatestPostsView.as_view()),
]
