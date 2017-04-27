# xops URL Configuration

from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('dashboard.urls')),
    url(r'^alert/', include('alert.urls')),
    url(r'^cmdb/', include('cmdb.urls'))
]