from datetime import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from json_field.fields import JSONField

from algorithms import registry


# class Set(models.Model):
#     weight = models.DecimalField()
#     reps_todo = models.SmallInteger()
#     reps_done = models.SmallInteger(default=0)
#     type = models.CharField(max_length=16)
#     data = models.ForeignKey(ExerciseData, related_name="sets")

#     @property
#     def failed(self):
#         return self.reps_done >= self.reps_todo:

#     @property
#     def succeeded(self):
#         return not self.failed


class ExerciseData(models.Model):
    definition = models.ForeignKey('lift.ExerciseDef')
    ts = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    previous = models.OneToOneField('self', null=True, blank=True, related_name="next")

    notes = models.CharField(max_length=1024, blank=True)

    data = JSONField(default="{}", max_length=1000)

    def __unicode__(self):
        return "%s's %s on %s" % (self.user, self.definition.display_name, 
                datetime.strftime(self.ts, "%Y-%d-%m"))

    def get_exer_data(self):
        if not hasattr(self, '_exer_data_cache'):
            self._exer_data_cache = self.definition.get_algorithm_instance()\
                                            .wrap_data(self.data) 
        return self._exer_data_cache

    def set_exer_data(self, exer_data):
        self.data = exer_data.to_json()
        self._exer_data_cache = exer_data

    exer_data = property(get_exer_data, set_exer_data)



class ExerciseDef(models.Model):

    display_name = models.CharField(max_length=512)
    video_url = models.CharField(max_length=1024, blank=True)

    algorithm = models.CharField(max_length=256, choices=registry.choices)
    options = JSONField(default="{}", max_length=1000)

    def __unicode__(self):
        return u"%s (%s)" % (self.display_name, self.algorithm)

    def get_algorithm_instance(self):
        return registry[self.algorithm](**self.options) # TODO: Security hole!?!

    def build_first_exercise_data(self):
        return self.get_algorithm_instance().build_first_exercise_data()

    def build_next_exercise_data(self):
        return self.get_algorithm_instance().build_next_exercise_data()


# class ExerciseDefRoutine(models.Model):
    
#     exercise_def = models.ForeignKey(ExerciseDef)
#     routine = models.ForeignKey(Routine)
#     ordering = models.IntegerField()


# class Routine(models.Model):
#     name = models.CharField()  # Day A
#     exercise_defs = models.ManyToManyField(ExerciseDef, through=ExerciseDefRoutine)

#     def build_next_workout(self, user):
#         for exercise_def in self.exercise_defs.all():
#             return Workout(user=user, exercises=exercise_def.build_next_exercise())





# "What is today's workout?"
# - "answer is a list of exercises"

# "What weights should I use for this exercise?"
# - "answer is based on previous weights + available weights"





