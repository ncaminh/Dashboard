import json
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .readfile import check_file, extract_data_from_file

# Create your views here.
def map_view(request, *args, **kwargs):
    json_file = open('blockMapping/JSON/df.json', 'r', encoding='utf-8');
    temp1 = json.load(json_file);
    json_file.close();

    mapping_file = open('blockMapping/JSON/diseases_mapping.json', 'r', encoding='utf-8');
    temp2 = json.load(mapping_file);
    mapping_file.close();
    return render(request, "map_page/map_table.html", {'json_info': json.dumps(temp1), 'mapping_info': json.dumps(temp2)});


def upload_file_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_type = check_file(request.FILES['file'].name);
            #file_type == 1: xlsx or xls; == 2: csv; == 0: other
            if(file_type != 0):
                var_a = extract_data_from_file(request.FILES['file'], file_type);
                mapping_file = open('blockMapping/JSON/diseases_mapping.json', 'r', encoding='utf-8');
                temp2 = json.load(mapping_file);
                mapping_file.close();

                return render(request, "map_page/map_table.html", {'json_info': json.dumps(var_a), 'mapping_info': json.dumps(temp2)});
    else:
        form = UploadFileForm()
        my_context = {
            'form': form,
        }
    return render(request, 'upload_page/upload_block.html', {'form': form});
