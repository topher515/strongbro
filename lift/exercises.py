from lift.models import *



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


class ExerciseDef(object):

	warmup_set_count = 1
	warmup_rep_count = 3

	work_set_count = 5
	work_rep_count = 5

	cooldown_set_count = 0
	cooldown_rep_count = 0

	weight_start = BARBELL[0]
	weight_increment = None


	@property
	def key(self):
		return self.name.lower().replace(" ","_") + "_" + self.version

	def build_sets(self, type, num, **kwargs):
		return [Set(type=type, **kwargs) for i in xrange(num)]

	def _build_exercise_data(self):
		sets = []
		for type in ["warmup","work","cooldown"]:
			sets += self.build_sets(type=type, 
								num=getattr(self,"%s_set_count" % type), 
								reps_todo=getattr(self,"%s_rep_count"))

		return ExerciseData(key=self.key, sets=sets)

	def build_first_exercise(self):
		exer_data = self._build_exercise_data()
		exer_data.weight = self.weight_start
		return exer_data

	def build_next_exercise(self, previous_exercise):
		exer_data = self._build_exercise_data()
		if previous_exercise.failed:
			if previous_exercise.did_fail_last_three():
				exer_data.weight = previous_exercise.weight - (
												previous_exercise.weight * 0.2)
			else:
				exer_data.weight = previous_exercise.weight

		else:
			exer_data.weight = previous_exercise.weight + self.weight_increment
		return exer_data


class BarbellSquatsDef(ExerciseDef):

	name = "Barbell Squats"
	version = 1

	weight_increment = 10
	weight_start