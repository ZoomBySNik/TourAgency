"""
URL configuration for TourAgency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as v
from django.urls import path
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_customer, name='register'),
    path('login/', v.LoginView.as_view(), name='login'),
    path('logout/', v.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home_view),
    path('news', views.news_view, name='news'),
    path('tours', views.tours_view, name='tours'),
    path('tour/<int:id>/', views.tour_detail, name='tour_detail'),
    path('book-request/<int:id>/', views.create_request_on_tour, name='create_request_on_tour')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
