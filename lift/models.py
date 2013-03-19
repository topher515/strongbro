from django.db import models
from django.conf import settings




class Weight(models.Model):
    value = models.DecimalField()
    unit = models.CharField(default="lbs")


weights = [
    1.25,1.25,
    2.5,2.5,
    5,5,
    10,10,
    25,25,
    35,35,
    45,45,45,45
]

barbells = [
    40,
]





class Set(models.Model):
    weight = models.DecimalField()
    try_reps = models.SmallInteger()
    success_reps = models.SmallInteger()


class ExerciseDef(models.Model):
    name = models.CharField()
    start_weight = models.DecimalField()
    
    def build_next_exercise(self, user):
        exercises = Exercise.object.filter(definition=self, 
                                            workout__user=user).order_by("-ts")
        if exercises.count() > 0:

        return 



class Exercise(models.Model):

    ts = models.DateTimeField(auto_now_add=True, index_db=True)

    previous = models.ForeignKey('self', null=True, blank=True)
    next = models.ForeignKey('self', null=True, blank=True)
    definition = models.ForeignKey(ExerciseDef)

    sets = models.ManyToManyField(Set)


class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    exercises = models.ManyToManyField(Exercise)

    
class Routine(models.Model):
    name = models.CharField()  # Day A
    exercises = models.ManyToManyField(ExerciseDef)

    def build_next_workout(self, user):
        for exercise_def in self.exercises.all():
            return Workout(user=user, exercises=exercise_def.build_next_exercise())


Routine {
    name: "day a",
    exercises: "bench press", "bar bell row", "squats"
}



class Workout(models.Model):

    generated_from = models.ForeignKey(routine)

    exercise_defs = models.