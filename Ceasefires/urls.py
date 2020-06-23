from django.db import models
from Ceasefires.models import *
from Ceasefires.views import *
from rest_framework import serializers,viewsets,routers
from django_filters.rest_framework import DjangoFilterBackend

from django.urls import path,include

from Ceasefires import views

router = routers.DefaultRouter()

# ========================================================

class RegionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Region
        fields = "__all__"
    pass

class RegionViewset(viewsets.ModelViewSet):
    queryset=Region.objects.all()
    serializer_class=RegionSerializer

router.register("regions",RegionViewset)

# ========================================================

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class CountryViewset(viewsets.ModelViewSet):
    queryset=Country.objects.all()
    serializer_class=CountrySerializer

router.register("countries",CountryViewset)

# ========================================================

class CeasefireSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ceasefire
        fields = ["country","effect_date"]
        filter_backends = [DjangoFilterBackend]

class CeasefireViewset(viewsets.ModelViewSet):
    queryset=Ceasefire.objects.all()
    serializer_class=CeasefireSerializer

router.register("ceasefires",CeasefireViewset)

# ========================================================

class ActorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Actor 
        fields = "__all__"

class ActorViewset(viewsets.ModelViewSet):
    queryset=Actor.objects.all()
    serializer_class=ActorSerializer

router.register("actors",ActorViewset)

"""
class ActorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"

class ActorViewset(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

router.register("actors",ActorViewset)
"""

# ========================================================

class DeclarationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Declaration
        fields = "__all__"

class DeclarationViewset(viewsets.ModelViewSet):
    queryset=Declaration.objects.all()
    serializer_class=DeclarationSerializer

router.register("declarations",DeclarationViewset)

# ========================================================

urlpatterns = [
    path("api/",include(router.urls)),
    path("update/",views.updateData)
]
