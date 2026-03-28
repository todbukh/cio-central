"""
URL configuration for project_a_17 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

urlpatterns = [
    path("", include('core.urls')),
    path("documents/", include('documents.urls')),
    path("executive/", include('exec_panel.urls')),
    path("admin/", admin.site.urls),
    path("profile/", include("profiles.urls")),
    # allauth urls:
    path('accounts/', include('allauth.urls')),
    path("", include("organization.urls")),
    path("s3demo/", include("s3_demo.urls")),  # TODO: remove this when done previewing demo
]
