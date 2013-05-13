import json

from django.core.serializers.json import Serializer as JSONSerializer
from django.core.serializers.json import DjangoJSONEncoder

from lift.models import ExerciseData, ExerciseDef

class ExerciseDataJSONSerializer(JSONSerializer):

    def handle_field(self, obj, field):
        #value = field._get_val_from_obj(obj)

        if isinstance(obj, ExerciseData) and field.name == "data":
            self._current[field.name] = json.loads(field.value_to_string(obj))
        elif isinstance(obj, ExerciseDef) and field.name == "options":
            self._current[field.name] = json.loads(field.value_to_string(obj))
        else:
            super(ExerciseDataJSONSerializer,self).handle_field(obj,field)
