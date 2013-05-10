import json

from datetime import datetime, timedelta
from django import forms

from utils import ClassRegistry, namedlist
from collections import defaultdict # namedtuple, 
from numbers import Number


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


    def wrap_data(self, data):
        return self.DataWrapper().from_dict(data)
    
    class DataWrapper(object):
        """
        The `ExercisedataWrapper` defines functionality which can be determined
        from *just this* exercise data. (For instance, was this exercise failed
        at this weight?)

        Also, it should know how to serialize this data to JSON and back
        """

        def from_dict(self, data):
            raise NotImplementedError()

        def to_dict(self):
            raise NotImplementedError()

        def to_json(self):
            return json.dumps(self.to_dict())





class Strongliftish(Algorithm):

    Set = namedlist('Set', ['name', 'assigned_reps', 'completed_reps', 'weight', 'rested_secs'])
    SetDef = namedlist('SetDef', ['assigned_reps','work_weight_factor', 'rest_secs'])

    DEFAULT_OPTIONS = {

        "set_def":{
            # name:   reps, work_weight_factor, rest_secs
            "warmup":SetDef(3, 0.5, 60*1.5),
            "work":  SetDef(5, 1.0, 60*1.5),
        },

        "sets":[
            ["warmup", 1],
            ["work",   5],
        ],


        "work_weight":"MIN",
        "upload_factor":0.02,
        "deload_factor":-0.2,
    }


    class DataWrapper(Algorithm.DataWrapper):

        version = 1

        def __init__(self):
            self.sets = []
            self.work_weight = None
        
        @property
        def exer_data(self):
            return self

        def from_dict(self, data):
            self.sets = [Strongliftish.Set(*set_) for set_ in data["sets"]]
            self.work_weight = data["w"]

        def to_dict(self):
            return {"sets":[set_ for set_ in self.sets], "w":self.work_weight}

        def zero_data(self):
            for set_ in self.sets:
                set_.completed_reps = 0
                set_.rested_secs = 0


        @property
        def failed(self):
            for set_ in self.sets:
                if set_.name != "work":
                    continue
                if set_.assigned_reps > set_.completed_reps:
                    return True
            return False

        @property
        def succeeded(self):
            return not self.failed


    def get_default_weight(self):
        w = self.options['work_weight']
        if isinstance(w,Number):
            return w
        elif w == "MIN":
            return BARBELLS[0]
        else:
            raise ValueError("Unexpected work_weight value: %s" % w)


    def set_new_work_weight(self, exer_data, weight):
        for set_ in exer_data.sets:
            set_.weight = weight * \
                        self.options["set_def"][set_.name].work_weight_factor
        exer_data.work_weight = weight

    def build_first_exercise_data(self):

        exer_data = self.DataWrapper()

        for set_name, set_count in self.options["sets"]:
            for i in xrange(set_count):
                set_def = self.options["set_def"][set_name]
                set_ = Strongliftish.Set(name=set_name, 
                            assigned_reps=set_def.assigned_reps,
                            completed_reps=0, 
                            weight=0, # This is set later 
                            rested_secs=0)
                exer_data.sets.append(set_)
        self.set_new_work_weight(exer_data, self.get_default_weight())

        return exer_data

    def xload(self, factor_name, exer_data):
        new_weight = exer_data.work_weight + (
                    exer_data.work_weight * self.options[factor_name])
        self.set_new_work_weight(exer_data, new_weight)
        exer_data.zero_data()
        return exer_data

    def duplicate(self, old_exer_data):
        exer_data = self.DataWrapper()
        exer_data.from_dict(old_exer_data.to_dict())
        return exer_data

    def build_new_with_upload(self, exer_data):
        return self.xload("upload_factor", self.duplicate(exer_data))

    def build_new_with_deload(self, exer_data):
        return self.xload("deload_factor", self.duplicate(exer_data))

    def build_next_exercise_data(self, previous_exercises):
        """
        If `previous_exercise_data` is a QuerySet containing `ExerciseData`
        then use that data to determine the *next* ExerciseData
        """
        prevs = previous_exercises

        last_exer = prevs[0].exer_data

        if last_exer.succeeded:
            # Use upload values from last one         
            exer_data = self.build_new_with_upload(last_exer)

        else:
            if self.did_fail_last_three(prevs):
                # Use deloaded values based on last one
                exer_data = self.build_new_with_deload(last_exer)

            else:
                # Use same values as last one
                exer_data = self.duplicate(last_exer)
                exer_data.zero_data()

        return exer_data
                

    def did_fail_last_three(self, previous_exercises):
        prevs = previous_exercises

        for p in prevs[:3]:
            if p.exer_data.succeeded:
                return False
        return True


