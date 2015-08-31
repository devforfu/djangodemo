from django.conf.urls import include, url
import welcome.views


urlpatterns = [
    url(r'^chart$', welcome.views.home_page),
    url(r'^chart/bar_chart$', welcome.views.bar_chart),
    url(r'^chart/users$', welcome.views.users),
    url(r'^chart/open_tickets$', welcome.views.open_tickets),
    url(r'^chart/avg_reply_time$', welcome.views.avg_reply_time),
    url(r'^chart/avg_ticket_close_time$', welcome.views.avg_ticket_close_time)
]
