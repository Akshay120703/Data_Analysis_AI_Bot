# myproject/urls.py

from django.contrib import admin
from django.urls import include, path
from django.conf import settings  # Add this line to import settings
from django.conf.urls.static import static
from data_analysis import views  # Import the new view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Add this line for the root URL
    path('data_analysis/', include('data_analysis.urls')),
]

if settings.DEBUG:  # This line now correctly references settings
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
