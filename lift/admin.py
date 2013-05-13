from django.contrib import admin
from django.contrib.admin import ModelAdmin

from lift.models import *


class DataMembershipInline(admin.TabularInline):
    model = DataMembership
    extra = 1

class WorkoutDataAdmin(ModelAdmin):
	inlines = (DataMembershipInline,)


class DefMembershipInline(admin.TabularInline):
    model = DefMembership
    extra = 1


class WorkoutDefAdmin(ModelAdmin):
	inlines = (DefMembershipInline,)


admin.site.register(ExerciseData)
admin.site.register(ExerciseDef)

admin.site.register(WorkoutData, WorkoutDataAdmin)
admin.site.register(WorkoutDef, WorkoutDefAdmin)