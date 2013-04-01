from django.db import models
from django.db.models import Q
from django.conf import settings




class Set(models.Model):
    weight = models.DecimalField()
    reps_todo = models.SmallInteger()
    reps_done = models.SmallInteger(default=0)
    type = models.CharField(max_length=16)

    @property
    def failed(self):
        return self.reps_done >= self.reps_todo:

    @property
    def succeeded(self):
        return not self.failed

class ExerciseData(models.Model):

    exercise_def
    ts = models.DateTimeField(auto_now_add=True, index_db=True)

    previous = models.ForeignKey('self', null=True, blank=True)
    next = models.ForeignKey('self', null=True, blank=True)
    definition = models.ForeignKey(ExerciseDef)

    sets = models.ManyToManyField(Set)

    def did_fail_last_three(self):
        if self.failed:
            for exer in self.objects.filter(Q(next=self) & Q(next__next=self)):
                if not exer.failed:
                    return False
            else:
                return True
        else:
            return False

    @property
    def failed(self):
        return any([x.failed in self.sets.all())

    @property
    def succeeded(self):
        return not self.failed


class BarbellSquat():






class ExerciseDef(models.Model):
    display_name = models.CharField()


    set_count = models.SmallInteger()

    weight_start = models.DecimalField()
    weight_increment = models.DecimalField()

    video_url = models.CharField(max_length=256)


    def build_first_exercise(self):



    def build_next_exercise(self, user):
        exercises = Exercise.object.filter(definition=self, 
                                            workout__user=user).order_by("-ts")
        if exercises.count() > 0:

        




class Routine(models.Model):
    name = models.CharField()  # Day A
    exercise_defs = models.ManyToManyField(ExerciseDef)

    def build_next_workout(self, user):
        for exercise_def in self.exercise_defs.all():
            return Workout(user=user, exercises=exercise_def.build_next_exercise())


Routine {
    name: "day a",
    exercises: "bench press", "bar bell row", "squats"
}



class Workout(models.Model):

    generated_from = models.ForeignKey(routine)

    exercise_defs = models.





"What is today's workout?"
- "answer is a list of exercises"

"What weights should I use for this exercise?"
- "answer is based on previous weights + available weights"





