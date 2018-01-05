from django.conf.urls import url
from graphqlendpoint.views import log_in, log_out, user_list, sign_up

app_name="eventsmanager"

urlpatterns = [
    url(r'^sign_up/$', sign_up, name='sign_up'),
    url(r'^log_in/$', log_in, name='log_in'),
    url(r'^log_out/$', log_out, name='log_out'),
    url(r'^$', user_list, name='user_list'),
]