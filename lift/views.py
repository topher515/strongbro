import json

from django.shortcuts import redirect
from django.core import serializers
from django.core.urlresolvers import reverse, resolve
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
#from django.views.generic import View, TemplateView
from simple_rest import Resource

from django.db.models.query import EmptyQuerySet

from lift.models import ExerciseData, WorkoutData, ExerciseDef, WorkoutDef
from lift.serializer import ExerciseDataJSONSerializer



class JsonView(Resource):
    """
    A view which returns JSON
    """
    def __init__(self, *args, **kwargs):
        #Serializer = serializers.get_serializer(serializer)
        #Serializer = custom_serializers[serializer]
        Serializer = ExerciseDataJSONSerializer
        self.serializer = Serializer()
        #print self.serializer
        super(JsonView, self).__init__(*args,**kwargs)

    # def dispatch(self, request, *args, **kwargs):
    #     resp = super(JsonView, self).dispatch(request, *args, **kwargs)
    #     if isinstance(resp, HttpResponse):
    #         return resp
    #     elif isinstance(resp, models.Model):
    #         return 
    #     elif isinstance(resp, QuerySet):
    #         return ser
    #     else:
    #         return resp

    # def dispatch(self, request, *args, **kwargs):
    #     print request.POST

    def not_found(self,message="not found"):
        return HttpResponse(json.dumps({"message":message}), status=404)

    def method_not_allowed(self,message="method not allowed"):
        return HttpResponse(json.dumps({"message":message}), status=405)

class AuthMixin(object):

    #@method_decorator(login_required)
    @csrf_exempt
    def dispatch(self, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponse(json.dumps({
                    "message":"not authorized"}),status=403)

        return super(AuthMixin,self).dispatch(*args,**kwargs)


class ModelListJsonView(JsonView):

    query_set = EmptyQuerySet()

    def get_query_set(self):
        return self.query_set

    def get(self, request):
        return HttpResponse(self.serializer.serialize(self.get_query_set()),
                status=200)

    def post(self, request):
        raise NotImplementedError

    def put(self, request):
        raise self.method_not_allowed()

    def delete(self, request):
        raise self.method_not_allowed()


class ModelDetailJsonView(JsonView):

    model = None

    # def get_model(self):
    #     return self.model

    @classmethod
    def resolve_to_instance(self, url):
        match = resolve(url)
        assert(match.func.model is self.get_model())
        return self.get_instance(match.kwargs.get('id'))

    def get_model(self):
        return self.model

    def get_instance(self, id):
        return self.get_model().objects.get(id=id)

    def get(self, request, id):
        return HttpResponse(self.serializer.serialize([self.get_instance(id)]), 
                                        status=200)

    def post(self, request, *args, **kwargs):
        return self.method_not_allowed()

    def put(self, request, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, request, *args, **kwargs):
        raise NotImplementedError()


class ExerciseDefView(ModelListJsonView):
    query_set = ExerciseDef.objects.all()

class ExerciseDefDetailView(ModelDetailJsonView):
    model = ExerciseDef

class WorkoutDefView(ModelListJsonView): # No auth necessary on defs
    query_set = WorkoutDef.objects.all()

class WorkoutDefDetailView(ModelDetailJsonView): # No auth necessary on defs
    model = WorkoutDef


class ExerciseDataView(AuthMixin, ModelListJsonView):
    query_set = ExerciseData.objects.all()


class ExerciseDataDetailView(AuthMixin, ModelDetailJsonView):
    model = ExerciseData


class WorkoutDataView(AuthMixin, ModelListJsonView):
    query_set = WorkoutData.objects.all()

    def post(self, request, *args, **kwargs):
        workout_def = WorkoutDefDetailView.resolve_to_instance(request.POST['workout_def'])
        workout_data = WorkoutData.build_first_workout_data(request.user)
        url = reverse(WorkoutDataDetailView.as_view(), kwargs={"id":workout_data.id})
        return redirect(url)


class WorkoutDataDetailView(AuthMixin, ModelDetailJsonView):
    model = WorkoutData



