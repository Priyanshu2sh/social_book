"""
URL configuration for social_book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from app import views
from app.views import UploadedFileList, UploadedFileDetail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),
    path('api/uploaded-files/', UploadedFileList.as_view(), name='uploaded-file-list'),
    path('api/uploaded-files/<int:pk>/', UploadedFileDetail.as_view(), name='uploaded-file-detail'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('authors/', views.authors, name='authors'),
    path('my_books/', views.my_books, name='my_books'),
    path('upload_books/', views.upload_books, name='upload_books'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
