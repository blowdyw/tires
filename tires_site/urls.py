"""
URL configuration for tires_site project.

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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),  # Подключаем urls для корзины
    path('product/', include('product.urls')),  # Пример для других приложений
    path('reg/', include('reg.urls')),
   # Пример для других приложений
]

# Добавляем маршруты для медиафайлов
if settings.DEBUG:  # Убедитесь, что это только в режиме отладки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


