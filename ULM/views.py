import csv, io, sys, datetime, calendar
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
from .models import *
from .forms import UploadForm, FilterFirstIterForm, FilterSecondIterForm
from .choices import *
from .logic import *

#this handles uploading of raw data
def upload(request, check="foo"):

    #templates
    template_upload = 'ULM/upload.html'

    #list of file types
    file_types = FILE_TYPE_CHOICES
    print(file_types)
    #list of existing files
    files = File.objects.all()

    upload_form = UploadForm()

    context = {
        'title' : 'Upload',
        'intro' : 'Please upload required csv files below.',
        'files' : files,
        'file_types' : file_types,
        'form'  : upload_form,
        'check' : check,
        }

    if request.method == 'GET':
        return render(request, template_upload, context)

    input_file = request.FILES['file_field']

    #Handle non-csv uploads

    if request.method == 'POST':
        
        a_file_type = request.POST.get('file_type')

        #set default file name for certain files
        a_file_name = get_default_file_name(a_file_type)

        #ensure unique file name for each file type
        try:
            #delete data if existing file exists
            associated_file = File.objects.get(file_name = a_file_name, file_type = a_file_type)
            associated_file.delete()

            new_file = File.objects.create(
                    file_name = a_file_name,
                    file_type = a_file_type,
                )
            associated_file = new_file
        except File.DoesNotExist:
            #create new file
            new_file = File.objects.create(
                    file_name = a_file_name,
                    file_type = a_file_type,
                )
            associated_file = new_file
        except File.MultipleObjectsReturned:
            #should not happen
            sys.exit("Error: files should be unique")

        if input_file.name.endswith('.csv'):
            handle_csv_file(input_file, a_file_type, associated_file)
        elif input_file.name.endswith('.xlsx'):
            handle_excel_file(input_file, a_file_type, associated_file)

        #query PATIENT INFO and store to model to fasten process
        #query occurs only if files exist for each file types

        #check file completeness
        files_dict  = File.objects.values()
        fa_risk_file_exist = False
        tcu_file_exist = False
        irms_file_exist = False
        postal_code_file_exist = False
        rental_block_file_exist = False
        for dict in files_dict:
            if dict['file_type'] == FA_RISK:
                fa_risk_file_exist = True
            elif dict['file_type'] == TCU_DEFAULTER:
                tcu_file_exist = True
            elif dict['file_type'] == IRMS:
                irms_file_exist = True
            elif dict['file_type'] == POSTAL_CODE:
                postal_code_file_exist = True
            elif dict['file_type'] == RENTAL_BLOCK:
                rental_block_file_exist = True
        if fa_risk_file_exist and tcu_file_exist and irms_file_exist and postal_code_file_exist and rental_block_file_exist:
            all_file_type_exist = True

        if all_file_type_exist:
            Patient_Info.objects.all().delete()
            patient_info = get_patient_info()
            store_patient_info(patient_info)

        return redirect('upload_success', "bar")
    
# show a message that uploading is successful


#webpage to show download button
def download_csv_mapping(request):
    template_download_csv = 'ULM/download_csv.html'
    context = {
        'title' : 'Download Unit Level Mapping',
        'content' : 'Press the button below to start downlading the compiled data',
        }
    return render(request, template_download_csv, context)

    if request.method == 'POST':
        return redirect('download_mapping')

#this function excecutes sql statement and automatically download the result (as attachment)
def get_csv(request):
    csv_file = "Unit Level Mapping.csv"
    data = get_compiled_data()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + csv_file

    #writer = csv.DictWriter(response, fieldnames = dict_data[0].keys())
    writer = csv.writer(response)
    writer.writerow(['Month', 'Patient Id', 'House Block', 'House Floor', 'House Unit', 'Street', 'Postal Code', 'Region', 'FA Risk', 'FA', 'TCU Defaulter', 'Referral Status', 'Rental Status'])
    for row in data:
        writer.writerow(row)
    return response

#First preliminary filter before showing visualization table
#filter by month, year and region
def filter_first_iter(request):
    template_filter_first_iter = 'ULM/filter_first.html'
    region_choices = get_all_regions()
    filter_form = FilterFirstIterForm(region_choices)

    context = {
        'title' : 'Filter by Month and Region',
        'intro' : 'Please select the month and region to display the visualization.',
        'form'  : filter_form,
        }

    if request.method == 'GET':
        return render(request, template_filter_first_iter, context)
    
    elif request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        region = request.POST.get('region')
        return redirect('filter2', month, year, region)

#Second preliminary filter before showing visualization table
#Once user did the first filter, they need to choose a block-street pair
def filter_second_iter(request, month, year, region):
    template_filter_second_iter = 'ULM/filter_second.html'
    block_street_choices = get_blk_filtered_by_month_year_region(month, year, region)
    filter_form = FilterSecondIterForm(block_street_choices)

    context = {
        'title' : 'Filter by Month and Region',
        'intro' : 'Please select the block and street pair to display the visualization.',
        'response' : {
            'Month' : calendar.month_name[month],
            'Year' : year,
            'Region' : region,
            },
        'form'  : filter_form,
        }

    if request.method == 'GET':
        return render(request, template_filter_second_iter, context)

    elif request.method == 'POST':
        block_street = request.POST.get('block_street')
        return redirect('display', month, year, region, block_street)

#Display the visualization table
def display(request, month, year, region, block_street):
    template_display = 'ULM/display.html'

    #parsing
    block, street = block_street.split(" - ", 1)

    isLanded = False
    if block == "Landed":
        isLanded = True

    #conversion to match sql filter
    if block == "Landed" or block == "Empty":
        block_converted = ""
    else:
        block_converted = block

    dict_data = get_data_for_display(month, year, region, block_converted, street)

    if isLanded:
        compiled_status = restructure_data_landed2(dict_data)
        house_floor_list = get_dummy_landed_house_floor(dict_data)
        house_unit_list = get_dummy_landed_unit(dict_data)
    else:
        compiled_status = restructure_data(dict_data)
        house_floor_list = get_unique_house_floor(dict_data)
        house_unit_list = get_unique_house_unit(dict_data)

    
    
    rental_status = is_rental_block(dict_data)

    
    context = {
        'title' : 'Filter by Month and Region',
        'intro' : 'The ULM table will be displayed below',
        'response' : {
            'Month' : calendar.month_name[month],
            'Year' : year,
            'Region' : region,
            'Block' : block,
            'Street' : street,
            },
        'house_floor' : house_floor_list,
        'house_unit' : house_unit_list,
        'rental_status' : rental_status,
        'data' : compiled_status,
        }

    return render(request, template_display, context)