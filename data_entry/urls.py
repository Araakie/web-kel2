from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import terima_proyek_engineering,terima_management,tampilkan_management,ProjectManagementAPIView,terima_managementsSI

app_name = 'data_entry'

urlpatterns = [
    path('pengguna/', views.set_pengguna, name='set_pengguna'),
    path('pengguna/<int:id>/', views.view_pengguna, name='view_pengguna'),
    path('api/pengguna/<int:user_id>/', views.get_pengguna_detail_api, name='get_pengguna_detail_api'),
    path('pengguna/<int:id>/view', views.view_pengguna, name='viewdata'),
    path('pengguna/<int:id>/update', views.update_pengguna, name='updatedata'),
    path('pengguna/<int:id>/delete', views.delete_pengguna, name='deletedata'),
    path('fromfile/', views.set_param_fromfile, name='unggahparam'),
    path('content/', views.set_content, name='set_content'),
    path('projek-final/', views.projek_final_view, name='projek_final'),
    path('signin/', views.signin_view, name='signin'),
    path('home/', views.home_project, name='homeproject'),
    path('newproject/', views.new_project, name='newproject'),
    path('dashboard/', views.project_dashboard, name='project_dashboard'),
    #path('timeline/', views.projecttimeline, name='projecttimeline'),
    path('project/', views.view_project, name='view_project'),
    path('profilelengkap/', views.profile_lengkap, name='profilelengkap'),
    # path('activitylog/', views.activity_log, name='activity_log'),
    path('api/terima_proyek/', terima_proyek_engineering, name='terima_proyek_engineering'),
    path('timeline/', tampilkan_management, name='tampilkan_management'),
    path('api/terima-management/', terima_management, name='terima_management'),
    path('api/terima-managementsSI/', terima_managementsSI, name='terima_managementsSI'),
    path('api/project-management/', ProjectManagementAPIView.as_view(), name='api-project-management'),

    path('api/project-list/', views.get_project_list, name='api-project-list'),
    path('api/home-project/', views.api_home_project, name='api_home_project'),

    path('api/all-timelines/', views.all_timelines, name='all_timelines'),

    
]

# Tambahkan ini di bagian paling bawah
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
