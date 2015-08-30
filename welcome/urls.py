from django.conf.urls import include, url
import welcome.views


urlpatterns = [
    url(r'^chart$', welcome.views.home_page)
]