import json

from lift.models import ExerciseData

from datetime import datetime, timedelta
from django import forms

from utils import ClassRegistry


registry = ClassRegistry()


WEIGHTS = [
    1.25,1.25,
    2.5,2.5,
    5,5,
    10,10,
    25,25,
    35,35,
    45,45,45,45
]

BARBELLS = [
    40,
]


# class ExerciseDelta(object):

#   def __init__(self, weight_delta, reasons):
#       self.weight_delta = delta
#       self.reasons = [reasons] if isinstance(reasons,basestring) else reasons

#   def __str__(self):

#       if self.weight_delta == 0:
#           s = "remains the same"
#       else:
#           s = " by %s" % abs(self.weight_delta)
#           if self.weight_delta > 0:
#               s = "increased" + s
#           else:
#               s = "decreased" + s

#       return "Weight %s because %s" % (s, self.reasons)



class Algorithm(object):
    """
    An `Algorithm` is what we use to calculate the *next* ExerciseData
    starting values.

    The *next* ExerciseData is usually based on the Previous `ExerciseData`
    but does not necessarily need to be (for instance the first ExerciseData
    must be created independently)
    """
    DEFAULT_OPTIONS = {}

    def __init__(self, **options):
        self.options = {}
        self.options.update(self.DEFAULT_OPTIONS)
        self.options.update(options)

    def get_exercise_data_wrapper(self):
        raise NotImplementedError()

    def wrap_data(self, data):
        DataWrapper = self.get_exercise_data_wrapper()
        return DataWrapper().from_dict(data)

    
class ExerciseDataWrapper(object):
    """
    The `ExercisedataWrapper` defines functionality which can be determined
    from *just this* exercise data. (For instance, was this exercise failed
    at this weight?)

    Also, it should know how to serialize this data to JSON and back
    """

    def from_dict(self):
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()

    def to_json(self):
        return json.dumps(self.to_dict())




class Strongliftish(Algorithm):

    DEFAULT_OPTIONS = {

        "warmup":{
            "set_count":1,
            "rep_count":3,

        },
        "work":{
            "set_count":5,
            "rep_count":5,
        },

        "work_weight_start":"<min>",
        "warmup_weight_factor":0.5,
        "upload_factor":0.02,
        "deload_factor":0.2,
    }


    class StrongliftishDataWrapper(ExerciseDataWrapper):

        def __init__(self):
            self.warmup_todo_sets = None
            self.warmup_todo_reps = None
            self.warmup_sets = None
            self.warmup_weight = None
            self.work_todo_sets = None
            self.work_todo_reps = None
            self.work_sets = None
            self.work_weight = None
        
        def from_dict(self, data):
            wrmup = data["wrmup"]
            work = data["work"]
            self.warmup_todo_sets = wrmup["todo_s"]
            self.warmup_todo_reps = wrmup["todo_r"]
            self.warmup_sets = wrmup["comp"]
            self.warmup_weight = wrmup["wght"]
            self.work_todo_sets = work["todo_s"]
            self.work_todo_reps = work["todo_r"]
            self.work_sets = work["comp"]
            self.work_weight = wrmup["wght"]
            return self

        def to_dict(self):
            return # TODO Write this (the reverse of from_dict)

        @property
        def failed(self):
            for rep in self.work_sets:
                if rep < self.work_todo_reps:
                    return True
            return False

        @property
        def succeeded(self):
            return not self.failed


    def get_exercise_data_wrapper(self):
        return self.StrongliftishDataWrapper



    def build_first_exercise_data(self):
        algopts = self.options
        exer_data = self.get_exercise_data_wrapper()()

        # Setup work sets
        exer_data.work_todo_sets = algopts["work"]["set_count"]
        exer_data.work_todo_reps = algopts["work"]["rep_count"]
        exer_data.work_sets = [0]*exer_data.warmup_todo_reps
        exer_data.work_weight = algopts['work_weight_start']

        # Setup warmup sets
        exer_data.warmup_todo_sets = algopts["warmup"]["set_count"]
        exer_data.warmup_todo_reps = algopts["warmup"]["rep_count"]
        exer_data.warmup_sets = [0]*exer_data.warmup_todo_sets
        exer_data.warmup_weight = exer_data.work_weight*algopts["warmup_weight_factor"]


    def build_next_exercise_data(self, previous_exercise_data):
        prevs = previous_exercise_data.order_by("-ts")

        if prevs[0].succeeded:

            if prevs[0].ts > datetime.now() - timedelta(days=14):
                delta = ExerciseDelta(self.options["weight_increment, 
                    "you successfully completed all your sets on %s" % prevs[0].ts)
            else:
                delta = ExerciseDelta(0,
                    "your last successful set was more than two weeks ago.")

        else:
            if prevs[1].failed and prevs[2].failed:
                delta = ExerciseDelta(prevs[0].weight, )
            else:
                delta = ExerciseDelta(prevs[0].weight,)


    def did_fail_last_three(self, previous_exercise_data):
        prevs = previous_exercise_data.order_by("-ts")

        for data_from_db in prevs[:3]:
            data = self.wrap_data(data_from_db.data)
            if data.succeeded():
                return False
        return True


