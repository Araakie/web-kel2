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
from .models import Project,Management

class ProyekEngineeringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

from rest_framework import serializers
from .models import Timeline

class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['id', 'deskripsi', 'nama', 'status', 'file_pdf']


class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Management
        fields = '__all__'

from rest_framework import serializers
from .models import ProjectManagement

class ProjectManagementSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None

    class Meta:
        model = ProjectManagement
        fields = '__all__'



