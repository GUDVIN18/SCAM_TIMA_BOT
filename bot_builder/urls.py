"""
URL configuration for bot_builder project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from apps.worker.views import task_complete_alert, get_user_page, pay_user_page, loading_user_page, balance_user_page, data_view, check_activity, send_message_support, get_admin_message_support



# urls.py
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render

def universal_view(request):
    """
    Универсальный обработчик для всех доменов
    """

    # Возвращаем общую страницу
    return render(request, 'universal_page.html', {
    })




urlpatterns = [
    path('', universal_view),
    path('admin/', admin.site.urls),
    path('task_complete_alert', task_complete_alert, name='task_complete_alert'),

    path('data_view/<str:token>/', data_view, name='data_view'),
    path('check_activity/<str:token>/', check_activity, name='check_activity'),
    path('get/<str:token>/', get_user_page, name='get_user_page'),
    path('pay/<str:token>/', pay_user_page, name='pay_user_page'),
    path('loading/<str:token>/', loading_user_page, name='loading_user_page'),
    path('balance/<str:token>/', balance_user_page, name='balance_user_page'),

    path('send_message_support/<str:token>/', send_message_support, name='send_message_support'),
    path('get_admin_message_support/<str:token>/', get_admin_message_support, name='get_admin_message_support'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
