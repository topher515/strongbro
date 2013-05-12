from django.contrib import admin

from lift.models import ExerciseData, ExerciseDef, WorkoutData, WorkoutDef

admin.site.register(ExerciseData)
admin.site.register(ExerciseDef)
admin.site.register(WorkoutData)
admin.site.register(WorkoutDef)