import json

from django.core.serializers.json import Serializer as JSONSerializer
from django.core.serializers.json import DjangoJSONEncoder

from lift.models import ExerciseData, ExerciseDef

class BaseJSONSerializer(JSONSerializer):

    def get_dump_object(self, obj):
        self._current["url"] = obj.get_absolute_url()
        self._current["id"] = obj.id
        return self._current

    def _handle(self, obj, field):
        if (isinstance(obj, ExerciseData) or isinstance(obj, ExerciseDef)) and \
            hasattr(obj, 'serialize_%s_field' % field.name):
            self._current[field.name] = \
                        getattr(obj, 'serialize_%s_field' % field.name)(field)
            return True
        return False

    def handle_fk_field(self, obj, field):
        if not self._handle(obj, field):
            super(BaseJSONSerializer,self).handle_fk_field(obj,field)

    def handle_field(self, obj, field):
        if not self._handle(obj, field):
            super(BaseJSONSerializer,self).handle_field(obj,field)


class ListJSONSerializer(BaseJSONSerializer):
    pass


class DetailJSONSerializer(BaseJSONSerializer):
    def start_serialization(self):
        if json.__version__.split('.') >= ['2', '1', '3']:
            # Use JS strings to represent Python Decimal instances (ticket #16850)
            self.options.update({'use_decimal': False})
        self._current = None
        self.json_kwargs = self.options.copy()
        self.json_kwargs.pop('stream', None)
        self.json_kwargs.pop('fields', None)
        #self.stream.write("[")

    def end_serialization(self):
        if self.options.get("indent"):
            self.stream.write("\n")
        #self.stream.write("]")
        if self.options.get("indent"):
            self.stream.write("\n")