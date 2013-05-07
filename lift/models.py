from django.db import models
from django.db.models import Q
from django.conf import settings
from jsonfield import JSONField

from exercises import registry


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
    definition = models.ForeignKey(ExerciseDef)
    ts = models.DateTimeField(auto_now_add=True, index_db=True)

    previous = models.ForeignKey('self', null=True, blank=True)
    next = models.ForeignKey('self', null=True, blank=True)

    notes = models.CharField(max_length=1024)

    data = JSONField()

    class Meta:
        abstract = True

    # def get_instance(self):

    # @property
    # def failed(self):
    #     return any([x.failed in self.sets.all()])

    # @property
    # def succeeded(self):
    #     return not self.failed

    def get_data_wrapper_instance():
        return self.definition.get_algorithm_instance().get_data_wrapper()(**data)


class StrongliftExerciseData(ExerciseData):
    sets_to_attempt = models.SmallIntegerField()
    set_attempts = JSONField() # Array
    set_attempts_weight = 
    [
        {"weight":"145lbs",'cnt':'15'}
    ]


class ExerciseDef(models.Model):

    display_name = models.CharField()
    video_url = models.CharField(max_length=1024)

    algorithm = models.CharField(max_length=256, choices=registry.choices)
    options = JSONField()


    def get_algorithm_instance(self):
        return registry[self.algorithm](**self.options) # TODO: Security hole!?!

    def build_first_exercise_data(self):
        return self.get_algorithm_instance().build_first_exercise_data()

    def build_next_exercise_data(self):
        return self.get_algorithm_instance().build_next_exercise_data()


class ExerciseDefRoutine(models.Model):
    
    exercise_def = models.ForeignKey(ExerciseDef)
    routine = models.ForeignKey(Routine)
    ordering = models.IntegerField()


class Routine(models.Model):
    name = models.CharField()  # Day A
    exercise_defs = models.ManyToManyField(ExerciseDef, through=ExerciseDefRoutine)

    def build_next_workout(self, user):
        for exercise_def in self.exercise_defs.all():
            return Workout(user=user, exercises=exercise_def.build_next_exercise())





# "What is today's workout?"
# - "answer is a list of exercises"

# "What weights should I use for this exercise?"
# - "answer is based on previous weights + available weights"





