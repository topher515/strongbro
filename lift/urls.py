from django.conf.urls import patterns, url

from lift.views import Exercises

urlpatterns = patterns('',
    url(r'^exercises\.json$', Exercises.as_view(), {}, name="exercises-json"),
)