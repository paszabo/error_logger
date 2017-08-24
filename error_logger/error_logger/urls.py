from django.conf.urls import include, url


urlpatterns = [
    url(r'^securities/', include('securities.urls')),
]
