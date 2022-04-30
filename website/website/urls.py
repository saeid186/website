"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from home.sitemaps import ProductViewSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'product': ProductViewSitemap,
}

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('home.urls', namespace='home')),
                  path('accounts/', include('accounts.urls', namespace='accounts')),
                  path('ckeditot/', include('ckeditor_uploader.urls')),
                  path('cart/', include('cart.urls', namespace='cart')),
                  path('order/', include('order.urls', namespace='order')),
                  path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
