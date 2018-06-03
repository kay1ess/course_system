"""course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from edu import views as e_views
from extra_app.DjangoUeditor import urls as DjangoUeditor_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('ueditor/', include(DjangoUeditor_urls)),

    path('e/index.html', e_views.index),
    path('e/pubCourse.html', e_views.pub_course),
    path('e/pubNews.html', e_views.pub_news),
    path('e/newNews.html', e_views.edit_news),
]
