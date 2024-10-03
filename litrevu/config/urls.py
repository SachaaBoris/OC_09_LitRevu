"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.views.generic import RedirectView

from users.views import LoginView
from users.views import SignupView
from users.views import LogoutUserView
from users.views import FollowUserView
from users.views import FollowedUsersView
from users.views import UnfollowUserView

from feed.views import FeedView
from feed.views import PostView
from feed.views import TicketCreateView
from feed.views import TicketUpdateView
from feed.views import TicketDeleteView
from feed.views import CreateTicketAndReviewView
from feed.views import ReviewCreateView
from feed.views import ReviewUpdateView
from feed.views import ReviewDeleteView

from config import settings

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    
    # Explicit login, signup, and logout paths
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path('follow/', FollowUserView.as_view(), name='follow-user'),
    path('follow/<int:pk>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('subscriptions/', FollowedUsersView.as_view(), name='subscriptions'),
    
    # Explicit tickets & feed paths
    path("feed/", FeedView.as_view(), name="feed"),
    path("posts/", PostView.as_view(), name="posts"),
    path("tickets/create/", TicketCreateView.as_view(), name="ticket-create"),
    path("tickets/create/with-review/", CreateTicketAndReviewView.as_view(), name="ticket-review-create"),
    path("tickets/<int:pk>/update/", TicketUpdateView.as_view(), name="ticket-update"),
    path("tickets/<int:pk>/delete/", TicketDeleteView.as_view(), name="ticket-delete"),
    path("reviews/create/<int:ticket_id>/", ReviewCreateView.as_view(), name="review-create"),
    path("reviews/<int:pk>/update/", ReviewUpdateView.as_view(), name="review-update"),
    path("reviews/<int:pk>/delete/", ReviewDeleteView.as_view(), name="review-delete"),
    
    # Redirect root to login
    path("", RedirectView.as_view(pattern_name='login', permanent=False), name="root-redirect"),
    
    # Catch-all route for any non-matching URLs
    re_path(r'^.*/$', RedirectView.as_view(pattern_name='login', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
