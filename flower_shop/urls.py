"""
URL configuration for flower_shop project.

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
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('contents.urls', 'contents'), namespace='contents')),
    path('', include('verifications.urls')),  # verifications
    path('', include('areas.urls')),  # areas
    path('', include(('goods.urls', 'goods'), namespace='goods')),  # goods
    path('', include(('carts.urls', 'carts'), namespace='carts')),  # carts
    path('', include(('orders.urls', 'orders'), namespace='orders')),
    path('', include(('payments.urls', 'payments'), namespace='pay')),
]
