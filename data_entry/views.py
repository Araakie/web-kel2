from django.shortcuts import render, get_object_or_404, redirect
from .forms import PenggunaForm
from .models import Pengguna
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UploadParamFromFileForm
from .models import ParameterOptPembebanan, ParameterBlending
from django.http import HttpRequest
import requests


def set_pengguna(request):
    list_pengguna = Pengguna.objects.all().order_by('-id')
    form = PenggunaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('data_entry:set_pengguna')

    return render(request, 'data_entry/input_data_2.html', {
        'form': form,
        'list_pengguna': list_pengguna,
    })


def view_pengguna(request, id):
    try:
        pengguna = Pengguna.objects.get(pk=id)
        return render(request, 'data_entry/pengguna_detail.html', {'user_id': pengguna.id})
    except Pengguna.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
def get_pengguna_detail_api(request, user_id):
    try:
        pengguna = Pengguna.objects.get(pk=user_id)
        data = {
            'email': pengguna.email,
            'address_1': pengguna.address_1,
            'address_2': pengguna.address_2,
            'city': pengguna.city,
            'state': pengguna.state,
            'zip_code': pengguna.zip_code,
            'tanggal_join': pengguna.tanggal_join.strftime('%Y-%m-%d')  # Format date as string
        }
        return JsonResponse(data)
    except Pengguna.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
def update_pengguna(request, id):
    pengguna = get_object_or_404(Pengguna, id=id)
    if request.method == 'POST':
        form = PenggunaForm(request.POST, instance=pengguna)
        if form.is_valid():
            form.save()
            return redirect('data_entry:view_pengguna', id=pengguna.id)
    else:
        form = PenggunaForm(instance=pengguna)

    list_pengguna = Pengguna.objects.all()
    context = {
        'form': form,
        'list_pengguna': list_pengguna,
        'pengguna': pengguna,
    }
    return render(request, 'data_entry/update_pengguna.html', context)

def confirm_delete_pengguna(request, id):
    pengguna = get_object_or_404(Pengguna, id=id)
    if request.method == "POST":
        pengguna.delete()
        return redirect('data_entry:set_pengguna')
    return render(request, 'data_entry/confirm_delete.html', {'object': pengguna})


def delete_pengguna(request, id):
    pengguna = get_object_or_404(Pengguna, id=id)
    pengguna.delete()
    return redirect('data_entry:set_pengguna')

def set_param_fromfile(request):
    context = None
    data = None
    form = UploadParamFromFileForm(None)

    if request.method == "POST":
        form = UploadParamFromFileForm(request.POST, request.FILES)
        if form.is_valid():
            unit = form.cleaned_data['unit']
            kategori = form.cleaned_data['kategori_param']
            uploadedfile = request.FILES['file']
            # str = []
            if (kategori == 'OPTB'):
                paran_value = []
                for line in uploadedfile:
                    text = line.decode()
                    textsplit = text.split(":")
                    paran_value.append(textsplit[1])
                paramoptb = ParameterOptPembebanan.objects.get_or_create(
                    unit=unit,
                    daya_min=int(paran_value[0])
                )
                return redirect('setparam:detailoptbunit', unit=unit.id)

            elif kategori == 'BLEND':
                paran_value = []
                for line in uploadedfile:
                    text = line.decode()
                    textsplit = text.split(":")
                    paran_value.append(textsplit[1])
                if (len(paran_value) >= 24):
                    param_blend = ParameterBlending.objects.get_or_create(
                        unit=unit,
                        AH=float(paran_value[0])
                    )
                    return redirect('setparam:detailbpunit', unit=unit.id)
    else:
        context = {'form': form}

    return render(request, 'setparam/setparamfromfile.html', context)

from .forms import ContentForm

def set_content(request):
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            form.save()
            form = ContentForm()  # kosongkan form setelah submit berhasil
    else:
        form = ContentForm()

    context = {
        'form': form,
    }
    return render(request, 'data_entry/create_content.html', context)

from django.shortcuts import render

def projek_final_view(request):
    return render(request, 'data_entry/projekfinal.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # (Autentikasi bisa kamu tambahkan nanti)
        return redirect('data_entry:projek_final')
    return render(request, 'data_entry/signin.html')


from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .models import Project

def home_project(request):
    projects = Project.objects.all()
    return render(request, 'data_entry/homeproject.html', {'projects': projects})


from .models import Project

import requests
from django.shortcuts import render, redirect
from .models import Project
from django.views.decorators.csrf import csrf_exempt


from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Project
import requests

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Project
import json
import requests

@csrf_exempt
def new_project(request):
    if request.method == 'POST':
        # Cek apakah request dari mobile (JSON) atau dari web (form)
        if request.content_type.startswith('application/json'):
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

            nama = data.get('nama')
            deskripsi = data.get('deskripsi')
            mulai = data.get('mulai')
            selesai = data.get('selesai')
            penanggungjawab = data.get('penanggungjawab')
            jumlah = data.get('jumlah', 0)
            pendanaan = data.get('pendanaan', 0)
            aktivitas1 = data.get('aktivitas1')
            aktivitas2 = data.get('aktivitas2')
            aktivitas3 = data.get('aktivitas3')
            file = None  # mobile tidak kirim file
        else:
            # Data dari form HTML (web)
            nama = request.POST.get('nama')
            deskripsi = request.POST.get('deskripsi')
            mulai = request.POST.get('mulai')
            selesai = request.POST.get('selesai')
            penanggungjawab = request.POST.get('penanggungjawab')
            jumlah = request.POST.get('jumlah')
            pendanaan = request.POST.get('pendanaan')
            aktivitas1 = request.POST.get('aktivitas1')
            aktivitas2 = request.POST.get('aktivitas2')
            aktivitas3 = request.POST.get('aktivitas3')
            file = request.FILES.get('file')

        # Validasi
        if not nama:
            return JsonResponse({"error": "Field 'nama' is required"}, status=400)

        # Simpan ke database lokal (Teman A)
        project = Project.objects.create(
            nama=nama,
            deskripsi=deskripsi,
            mulai=mulai,
            selesai=selesai,
            penanggungjawab=penanggungjawab,
            jumlah=jumlah or 0,
            pendanaan=pendanaan or 0,
            aktivitas1=aktivitas1,
            aktivitas2=aktivitas2,
            aktivitas3=aktivitas3,
            file=file
        )

        # Kirim ke teman B
        data_to_send = {
            "nama": nama,
            "deskripsi": deskripsi,
            "mulai": mulai,
            "selesai": selesai,
            "penanggungjawab": penanggungjawab,
            "jumlah": jumlah,
            "pendanaan": pendanaan,
            "aktivitas": [aktivitas1, aktivitas2, aktivitas3]
        }

        try:
            response = requests.post(
                "http://10.40.30.73:8000/api/terima_proyek/",
                json=data_to_send,
                timeout=10
            )
            print("Respon dari teman:", response.status_code, response.text)
        except Exception as e:
            print("Gagal mengirim ke teman:", e)

        # Balasan
        if request.content_type.startswith('application/json'):
            return JsonResponse({"message": "Project created and sent"}, status=201)
        else:
            return redirect('data_entry:homeproject')

    # GET request (web form)
    return render(request, 'data_entry/newproject.html')

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from .serializer import ProyekEngineeringSerializer

@api_view(['POST'])
def terima_proyek_engineering(request):
    data = request.data

    # Ambil aktivitas dari array, jika tidak lengkap isi dengan string kosong
    aktivitas = data.get('aktivitas', [])
    aktivitas1 = aktivitas[0] if len(aktivitas) > 0 else ''
    aktivitas2 = aktivitas[1] if len(aktivitas) > 1 else ''
    aktivitas3 = aktivitas[2] if len(aktivitas) > 2 else ''

    # Buat instance Project
    proyek = Project.objects.create(
        nama=data.get('nama'),
        deskripsi=data.get('deskripsi'),
        mulai=data.get('mulai'),
        selesai=data.get('selesai'),
        penanggungjawab=data.get('penanggungjawab'),
        jumlah=data.get('jumlah'),
        pendanaan=data.get('pendanaan'),
        aktivitas1=aktivitas1,
        aktivitas2=aktivitas2,
        aktivitas3=aktivitas3
    )

    serializer = ProyekEngineeringSerializer(proyek)
    return Response({'status': 'berhasil disimpan', 'data': serializer.data})


from django.shortcuts import render
from .models import Project
from .forms import ProjectSearchForm

def project_dashboard(request):
    form = ProjectSearchForm(request.GET)
    projects = []

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        if keyword:
            projects = Project.objects.filter(nama__icontains=keyword)
    
    return render(request, 'data_entry/project_dashboard.html', {
        'form': form,
        'projects': projects
    })

from django.http import JsonResponse
from django.shortcuts import render
from .models import Timeline

# def projecttimeline(request):
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         timelines = Timeline.objects.all()
#         data = []
#         for t in timelines:
#             data.append({
#                 'nama': t.nama,
#                 'deskripsi': t.deskripsi,
#                 'presentase': t.status,
#                 'file_pdf': t.file_pdf.url if t.file_pdf else None
#             })
#         return JsonResponse(data, safe=False)
    
#     return render(request, 'data_entry/projecttimeline.html')

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from .models import Management

@csrf_exempt
@api_view(['GET', 'POST'])
def terima_management(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            nama_kelompok = data.get('namaKelompok')
            deskripsi = data.get('deskripsi')
            status = data.get('status')

            if not all([nama_kelompok, deskripsi, status]):
                return JsonResponse({'error': 'Semua field harus diisi.'}, status=400)

            Management.objects.create(
                namaKelompok=nama_kelompok,
                deskripsi=deskripsi,
                status=status
            )

            return JsonResponse({'message': 'Data berhasil diterima dan disimpan.'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Format JSON tidak valid.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        data = []
        for m in Management.objects.all():
            data.append({
                'nama': m.namaKelompok,
                'deskripsi': m.deskripsi,
                'presentase': 100 if m.status.lower() == 'selesai' else 0
            })
        return JsonResponse(data, safe=False)

    return JsonResponse({'error': 'Metode tidak diizinkan.'}, status=405)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import ProjectManagement
from .serializer import ProjectManagementSerializer

# Tambahan penting:
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class ProjectManagementAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        queryset = ProjectManagement.objects.all().order_by('-timestamp')
        serializer = ProjectManagementSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectManagementSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from .models import Management

def tampilkan_management(request):
    semua_data = Management.objects.all()
    return render(request, 'data_entry/projecttimeline.html', {'data': semua_data})


from django.shortcuts import render, redirect
project_tasks = [
    {'activity': 'Analisis dan Perancangan', 'status': 'COMPLETED', 'percentage': 100, 'deadline': ''},
    {'activity': 'Setup dan Infrastruktur', 'status': 'ON PROGRESS', 'percentage': 50, 'deadline': ''},
    {'activity': 'Pengembangan Frontend dan Backend', 'status': 'ON PROGRESS', 'percentage': 90, 'deadline': ''},
    {'activity': 'Integrasi dan Testing', 'status': 'ON PROGRESS', 'percentage': 63, 'deadline': ''},
    {'activity': 'Deployment', 'status': 'NOT STARTED', 'percentage': 0, 'deadline': ''},
    {'activity': 'Feedback dan Revisi', 'status': 'NOT STARTED', 'percentage': 0, 'deadline': ''},
    {'activity': 'Maintenance', 'status': 'NOT STARTED', 'percentage': 0, 'deadline': ''},
]
def view_project(request):
    global project_tasks    
    if request.method == 'POST':
        activity = request.POST.get('activity')
        status = request.POST.get('status')
        percentage = int(request.POST.get('percentage', 0))
        deadline = request.POST.get('deadline')

        project_tasks.append({
            'activity': activity,
            'status': status,
            'percentage': percentage,
            'deadline': deadline
        })

    return render(request, 'data_entry/viewproject.html', {'tasks': project_tasks})

       
from django.shortcuts import render, redirect
from .models import Profile

import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from .models import Profile


def profile_lengkap(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        alamat = request.POST.get('alamat')
        tgl_lahir = request.POST.get('tgl_lahir')
        telp = request.POST.get('telp')
        foto_upload = request.FILES.get('foto')
        foto_kamera = request.POST.get('foto_kamera')

        profile, created = Profile.objects.get_or_create(id=1)
        profile.nama = nama
        profile.alamat = alamat
        profile.tgl_lahir = tgl_lahir
        profile.telp = telp

        if foto_upload:
            profile.foto = foto_upload
        elif foto_kamera:
            format, imgstr = foto_kamera.split(';base64,')
            ext = format.split('/')[-1]
            profile.foto.save(f"{nama}_kamera.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)

        profile.save()
        return redirect('data_entry:homeproject')

    profile = Profile.objects.first()
    return render(request, 'data_entry/profilelengkap.html', {'profile': profile})

from django.shortcuts import render
from .models import Project  # asumsi ada model Project
from datetime import timedelta
from django.utils import timezone

from django.shortcuts import render
from .models import Project
from datetime import timedelta
from django.utils import timezone
import json

def activity_log(request):
    query = request.GET.get('q')
    project = None
    labels = []
    values = []

    if query:
        try:
            project = Project.objects.get(nama__icontains=query)
            today = timezone.now().date()
            labels = [(today - timedelta(days=i)).strftime('%d-%m') for i in range(6, -1, -1)]
            values = [(i+1)*10 for i in range(7)]  # dummy
        except Project.DoesNotExist:
            project = None

    # Gunakan json.dumps agar aman untuk JavaScript
    return render(request, 'data_entry/activity_log.html', {
        'query': query,
        'project': project,
        'labels': json.dumps(labels),
        'values': json.dumps(values)
    })

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import ModelMasuk

@csrf_exempt
@api_view(['GET', 'POST'])
def terima_model_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nama = data.get('nama_kelompok')
            deskripsi = data.get('deskripsi')
            status = data.get('status')

            if not all([nama, deskripsi, status]):
                return JsonResponse({'status': 'gagal', 'keterangan': 'Data tidak lengkap'}, status=400)

            ModelMasuk.objects.create(
                nama_kelompok=nama,
                deskripsi=deskripsi,
                status=status
            )

            return JsonResponse({'status': 'berhasil'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'pesan': str(e)}, status=500)

    return JsonResponse({'status': 'hanya menerima POST'})








from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import ManagementSI

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ManagementSI

from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import ManagementSI
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ManagementSI
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import ManagementSI

@csrf_exempt
def terima_managementsSI(request):
    if request.method == 'POST':
        if not request.body:
            return JsonResponse({'success': False, 'message': 'Request body kosong'}, status=400)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse({'success': False, 'message': f'Gagal decode JSON: {str(e)}'}, status=400)

        deskripsi = data.get('deskripsi')
        status = data.get('status')
        namaKelompok = data.get('namaKelompok')

        if not all([deskripsi, status, namaKelompok]):
            return JsonResponse({'success': False, 'message': 'Semua field harus diisi'}, status=400)

        ManagementSI.objects.create(
            deskripsi=deskripsi,
            status=status,
            namaKelompok=namaKelompok
        )

        return JsonResponse({'success': True, 'message': 'Data berhasil disimpan'})

    elif request.method == 'GET':
        data = list(ManagementSI.objects.values())
        return JsonResponse({'success': True, 'data': data})

    return JsonResponse({'success': False, 'message': 'Method tidak diizinkan'}, status=405)




from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from .serializer import ProyekEngineeringSerializer

@api_view(['GET'])
def get_project_list(request):
    queryset = Project.objects.all()
    serializer = ProyekEngineeringSerializer(queryset, many=True)
    return Response(serializer.data)

from django.http import JsonResponse
from .models import Project
from django.core.serializers import serialize
import json

def api_home_project(request):
    projects = Project.objects.all()
    data = json.loads(serialize('json', projects))
    project_list = [
        {
            "nama": item['fields']['nama'],
            "deskripsi": item['fields']['deskripsi'],
            "mulai": item['fields']['mulai'],
            "selesai": item['fields']['selesai'],
            "penanggungjawab": item['fields']['penanggungjawab'],
            "jumlah": item['fields']['jumlah'],
            "pendanaan": item['fields']['pendanaan'],
            "aktivitas1": item['fields']['aktivitas1'],
            "aktivitas2": item['fields']['aktivitas2'],
            "aktivitas3": item['fields']['aktivitas3']
        }
        for item in data
    ]
    return JsonResponse(project_list, safe=False)

from django.http import JsonResponse
from .models import Management, ManagementSI, ProjectManagement


from django.http import JsonResponse
from .models import Management, ManagementSI, ProjectManagement

from django.http import JsonResponse
from .models import Management, ManagementSI, ProjectManagement


def all_timelines(request):
    if request.method == "GET":
        data = []

        # Model: Management
        for m in Management.objects.all():
            data.append({
                "nama": m.namaKelompok,
                "deskripsi": m.deskripsi,
                "presentase": 100 if m.status.lower() == "selesai" else 0
            })

        # Model: ManagementSI
        for m in ManagementSI.objects.all():
            data.append({
                "nama": m.namaKelompok,
                "deskripsi": m.deskripsi,
                "presentase": 100 if m.status.lower() == "selesai" else 0
            })

        # Model: ProjectManagement (gunakan field yg sesuai model)
        for m in ProjectManagement.objects.all():
            data.append({
                "nama": m.nama_kelompok,
                "deskripsi": m.deskripsi_model,  # ✅ ini nama field yg BENAR dari model
                "presentase": 100 if m.status_model.lower() == "selesai" else 0
            })

        return JsonResponse(data, safe=False)

    return JsonResponse({"error": "Metode tidak diizinkan"}, status=405)
