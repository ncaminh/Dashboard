from django.urls import path
from .views import (
	map_view, 
	upload_file_view,
	change_combination_view,
	)

urlpatterns = [
    path('map/', map_view, name='map'),
    path('upload_block/', upload_file_view, name='upload_block'),
    path('change/', change_combination_view, name='change_combo'),
    # path('', upload_file_view, name='upload'),

]