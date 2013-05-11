import json

from django.core import serializers
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View, TemplateView
from django.db.models.query import EmptyQuerySet

from lift.models import ExerciseData

class JsonView(View):

    def get_json(self, *args, **kwargs):
        raise NotImplementedError()

    def get(self, *args, **kwargs):
        return self.get_json(*args, **kwargs)


class AuthMixin(object):

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({
                    "error":"not authorized"}),status=403)

        return super(AuthMixin,self).dispatch(*args,**kwargs)


class ModelJsonView(JsonView):

    query_set = EmptyQuerySet()

    def __init__(self, serializer="json", *args, **kwargs):
        Serializer = serializers.get_serializer(serializer)
        self.serializer = Serializer()
        super(ModelJsonView, self).__init__(*args,**kwargs)

    def get_query_set(self):
        return self.query_set.filter(user=self.request.user)

    def get_json(self, request):
        return self.serializer.serialize(self.get_query_set())


class Exercises(AuthMixin, ModelJsonView):

    query_set = ExerciseData.objects.all()