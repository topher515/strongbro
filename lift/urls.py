from django.conf.urls import patterns, url

from lift.views import ExerciseDataView, WorkoutDataView, ExerciseDataView, WorkoutDataView

urlpatterns = patterns('',

	#url(r'^definitions/exercises\.json', ExerciseDef.as_view(), {}, name="exercises-defs-json"),
    #url(r'^definitions/workouts\.json$', WorkoutDefs.as_view(), {}, name="workout-defs-json"),

    url(r'^data/exercises\.json$', ExerciseDataView.as_view(), {}, name="exercise-list-data-json"),
    url(r'^data/exercises/(?P<exercise_id>[0-9]+)\.json$', ExerciseDataDetailView.as_view(), {}, name="exercise-data-detail-json"),
    url(r'^data/workouts\.json$', WorkoutDataView.as_view(), {}, name="workout-list-data-json"),
    url(r'^data/workouts/(?P<workout_id>[0-9]+)\.json$', WorkoutDataDetailView.as_view(), {}, name="workout-data-detail-json"),
)


# Maybe use:
# https://github.com/freshplum/django-simple-rest