from django.urls import path
from . import views

urlpatterns = [
        path('upload/<str:check>/', views.upload, name = 'upload_success'),
        path('upload/', views.upload, name = 'upload'),
        path('download/mapping/', views.get_csv, name = 'download_mapping'),
        path('download/', views.download_csv_mapping, name = 'download'),
        path('display/filter1/', views.filter_first_iter, name = 'filter1'),
        path('display/filter2/<int:month>/<int:year>/<str:region>', views.filter_second_iter, name = 'filter2'),
        path('display/<int:month>/<int:year>/<str:region>/<str:block_street>/', views.display, name = 'display'),
    ]