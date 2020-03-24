import json
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .readfile import check_file, extract_data_from_file, process_data

# Create your views here.
def map_view(request, *args, **kwargs):
    json_file = open('blockMapping/JSON/df.json', 'r', encoding='utf-8')
    data = json.load(json_file)
    json_file.close()

    mapping_file = open('blockMapping/JSON/diseases_mapping.json', 'r', encoding='utf-8')
    mapping_info = json.load(mapping_file)
    mapping_file.close()

    list_all_diseases = mapping_info.keys()

    return render(request, "map_page/map_table.html", {'json_info': json.dumps(data), 'mapping_info': json.dumps(mapping_info), 'all_diseases': list_all_diseases})


def upload_file_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_type = check_file(request.FILES['file'].name);
            #file_type == 1: xlsx or xls; == 2: csv; == 0: other
            if(file_type != 0):
                data = extract_data_from_file(request.FILES['file'], file_type)
                mapping_file = open('blockMapping/JSON/diseases_mapping.json', 'r', encoding='utf-8')
                mapping_info = json.load(mapping_file)
                mapping_file.close()

                list_all_diseases = mapping_info.keys()

                return render(request, "map_page/map_table.html", {'json_info': json.dumps(data), 'mapping_info': json.dumps(mapping_info), 'all_diseases': list_all_diseases})
    else:
        form = UploadFileForm()
        my_context = {
            'form': form,
        }
    return render(request, 'upload_page/upload_block.html', {'form': form})

def change_combination_view(request, *args, **kwargs):
    if request.method == 'POST':
        list_diseases = request.POST.getlist('main-disease')
        process_data(list_diseases)
    return render(request,"change_combination_page/change_combination.html", {})
