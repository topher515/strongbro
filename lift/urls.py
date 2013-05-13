from django.conf.urls import patterns, url

from lift.views import *

urlpatterns = patterns('',

	url(r'^exercises/defs/?$', ExerciseDefView.as_view(), {}),
	url(r'^exercises/defs/(?P<id>[0-9]+)/?$', ExerciseDefDetailView.as_view(), {}),

	url(r'^workouts/defs/?$', WorkoutDefView.as_view(), {}),
	url(r'^workouts/defs/(?P<id>[0-9]+)/?$', WorkoutDefDetailView.as_view(), {}),

    url(r'^exercises/data/?$', ExerciseDataView.as_view(), {}, name="exercise-list-data-json"),
    url(r'^exercises/data/(?P<id>[0-9]+)/?$', ExerciseDataDetailView.as_view(), {}, name="exercise-data-detail-json"),
    
    url(r'^workouts/data/?$', WorkoutDataView.as_view(), {}, name="workout-list-data-json"),
    url(r'^workouts/data/(?P<id>[0-9]+)\.json$', WorkoutDataDetailView.as_view(), {}, name="workout-data-detail-json"),
)


# GET /user/45/

# # Find and create a new workout data
# GET /workouts/defs/
# POST /workouts/data/?def=/workouts/defs/2/
# GET /workouts/data/56/
# ...
# which has references to
# ...
# GET /exercises/data/87/
# GET /exercises/data/182/
# GET /exercises/data/979/


# # Create a new workout





# Maybe use:
# https://github.com/freshplum/django-simple-rest