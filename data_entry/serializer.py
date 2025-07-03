from rest_framework import serializers


class ProyekSerializer(serializers.Serializer):
    nama = serializers.CharField()
    deskripsi = serializers.CharField()
    mulai = serializers.DateField()
    selesai = serializers.DateField()
    penanggungjawab = serializers.CharField()
    jumlah = serializers.IntegerField()
    pendanaan = serializers.IntegerField()
    aktivitas = serializers.ListField(child=serializers.CharField())


# class ProyekEngineeringSerializer(serializers.Serializer):
#     nama = serializers.CharField()
#     deskripsi = serializers.CharField()
#     mulai = serializers.DateField()
#     selesai = serializers.DateField()
#     penanggungjawab = serializers.CharField()
#     jumlah = serializers.IntegerField()
#     pendanaan = serializers.IntegerField()
#     aktivitas = serializers.ListField(child=serializers.CharField())

from rest_framework import serializers
from .models import Project,Management,ManagementSI

class ProyekEngineeringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

from rest_framework import serializers
from .models import Timeline

class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['id', 'deskripsi', 'nama', 'status']


class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Management
        fields = '__all__'

from rest_framework import serializers
from .models import ProjectManagement

class ProjectManagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectManagement
        fields = '__all__'


class ManagementSISerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementSI
        fields = '__all__'
