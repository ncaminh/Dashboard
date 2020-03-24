from django.db import connection
import pandas as pd
from .sql import *
from .choices import *
from .models import *
import csv, io, sys, datetime

#FUNCTIONS (LOGIC)

#for data manipulation
def get_dummy_landed_house_floor(list_of_dict):
    new_list = []
    i = 1
    for dict in list_of_dict:
        new_list.append("Landed" + str(i))
        i += 1
    return new_list

def get_dummy_landed_unit(list_of_dict):
    new_list = []
    for dict in list_of_dict:
        new_list.append(' ')
    return new_list

def get_unique_house_floor(list_of_dict):
    new_set = set()
    count_none = 0
    for dict in list_of_dict:
        if dict['house_floor'] is None:
            count_none += 1
        new_set.add(dict['house_floor'])

    new_list = list(new_set)
    for i in range(count_none - 1):
        new_list.append(None)
    print(new_list)
    print(count_none)
    return new_list

def get_dummy_house_floor(list_of_dict):
    new_set = set()
    
    i = 1
    for dict in list_of_dict:
        if dict['house_floor'] is not None:
            new_set.add(str(dict['house_floor']))
        else:
            new_set.add('Unknown' + str(i))
            i += 1

    new_list = list(new_set)
    new_list.sort()
    return new_list
   
def get_dummy_house_unit(list_of_dict):
    new_set = set()
    
    i = 1
    for dict in list_of_dict:
        #print('hu: ' + dict['house_unit'])
        if dict['house_unit'] != '':
            new_set.add(dict['house_unit'])
        else:
            #print('Unknown' + str(i))
            new_set.add('Unknown' + str(i))
            i += 1

    new_list = list(new_set)
    new_list.sort()
    return new_list

def get_unique_house_unit(list_of_dict):
    new_set = set()
    count_none = 0
    for dict in list_of_dict:
        new_set.add(dict['house_unit'])

    new_list = list(new_set)
    new_list.sort()
    return new_list

def is_rental_block(list_of_dict):
    if len(list_of_dict) > 0:
        #print(list_of_dict[0]['rental_status'])
        return list_of_dict[0]['rental_status'] != 0
    else:
        return False

def restructure_data(list_of_dict):
    new_dict = {}
    list_house_floors =  get_unique_house_floor(list_of_dict)
    #print("list hf")
    #print(list_house_floors)

    id_hf = 1
    id_hu = 1
    for hf in list_house_floors:
        house_unit_dict = {}
        track_house_unit = []
        for dict in list_of_dict:
            if dict['house_floor'] == hf:
                hu = dict['house_unit']
                #print(track_house_unit)
                #print("hu: " + str(hu))
                if track_house_unit.count(hu) == 0 and hu != '':
                    track_house_unit.append(hu)
                    list_patient_id = [dict['patient_id']]
                    content_dict = {
                        'fa_risk_status' : 'FR' if dict['fa_risk_status'] == True else '', 
                        'fa_status' : 'FA' if dict['fa_status'] == True else '',
                        'tcu_status' : 'TD' if dict['tcu_status'] == True else '',
                        'irms_status' : 'AD' if dict['irms_status'] == 'Admitted' else '',
                        'irms_status_2' : 'WD' if dict['irms_status'] == 'Withdrawn' else '',
                        'patient_id' : list_patient_id,
                        }
                elif hu == '':
                    hu = "Unknown" + str(id_hu)
                    id_hu += 1
                    list_patient_id = [dict['patient_id']]
                    content_dict = {
                            'fa_risk_status' : 'FR' if dict['fa_risk_status'] == True else '', 
                            'fa_status' : 'FA' if dict['fa_status'] == True else '',
                            'tcu_status' : 'TD' if dict['tcu_status'] == True else '',
                            'irms_status' : 'AD' if dict['irms_status'] == 'Admitted' else '',
                            'irms_status_2' : 'WD' if dict['irms_status'] == 'Withdrawn' else '',
                            'patient_id' : list_patient_id,
                            }
                elif track_house_unit.count(hu) > 0:
                    list_patient_id = house_unit_dict[hu]['patient_id']
                    list_patient_id.append(dict['patient_id'])
                    content_dict = {
                        'fa_risk_status' : 'FR' if ((dict['fa_risk_status'] == True) or (house_unit_dict[hu]['fa_risk_status'] == 'FR')) else '', 
                        'fa_status' : 'FA' if ((dict['fa_status'] == True) or (house_unit_dict[hu]['fa_status'] == 'FA')) else '',
                        'tcu_status' : 'TD' if ((dict['tcu_status'] == True) or (house_unit_dict[hu]['tcu_status'] == 'TD')) else '',
                        'irms_status' : 'AD' if ((dict['irms_status'] == 'Admitted') or (house_unit_dict[hu]['irms_status'] == 'AD')) else '',
                        'irms_status_2' : 'WD' if ((dict['irms_status'] == 'Withdrawn') or (house_unit_dict[hu]['irms_status_2'] == 'WD')) else '',
                        'patient_id' : list_patient_id,
                        }
                house_unit_dict[hu] = content_dict
                if hf is None:
                    dict['house_floor'] = 'x'
                    break
        if hf is None:
            hf = 'Unknown' + str(id_hf)
            id_hf += 1
        new_dict[str(hf)] = house_unit_dict
    return new_dict

def restructure_data_landed2(list_of_dict):
    new_dict = {}
    list_house_floors = []
    for i in range(1,len(list_of_dict) + 1):
        list_house_floors.append("Landed" + str(i))
   
    i = 0
    for hf in list_house_floors:
        house_unit_dict = {}
        dict = list_of_dict[i]
        list_patient_id = [dict['patient_id']]
        content_dict = {
            'fa_risk_status' : 'FR' if dict['fa_risk_status'] == True else '', 
            'fa_status' : 'FA' if dict['fa_status'] == True else '',
            'tcu_status' : 'TD' if dict['tcu_status'] == True else '',
            'irms_status' : 'AD' if dict['irms_status'] == 'Admitted' else '',
            'irms_status_2' : 'WD' if dict['irms_status'] == 'Withdrawn' else '',
            'patient_id' : list_patient_id,
            }
        house_unit_dict[' '] = content_dict

        new_dict[str(hf)] = house_unit_dict
        i += 1
    return new_dict

def restructure_data_landed(list_of_dict):
    new_dict = {}
    i = 1
    for dict in list_of_dict:
        content_dict = {
            'fa_risk_status' : 'FR' if dict['fa_risk_status'] == True else '', 
            'fa_status' : 'FA' if dict['fa_status'] == True else '',
            'tcu_status' : 'TD' if dict['tcu_status'] == True else '',
            'irms_status' : 'AD' if dict['irms_status'] == 'Admitted' else '',
            }
        new_dict['Landed' + str(i) ] = content_dict
        i  = i + 1
    return new_dict

#for fetching data and sql interaction
def get_patient_info():
    with connection.cursor() as cursor:
        cursor.execute(PATIENT_INFO_INITIALIZATION)
        return cursor.fetchall()

def get_compiled_data():
    with connection.cursor() as cursor:
        cursor.execute(STANDARD_TEMPLATE)
        return cursor.fetchall()

def get_blk_filtered_by_month_year_region(month, year, region):
    with connection.cursor() as cursor:
        cursor.execute(FILTERED_MONTH_YEAR_REGION, [month, year, region])
        return cursor.fetchall()

def get_data_for_display(month, year, region, block, street):
    with connection.cursor() as cursor:
        cursor.execute(FILTERED_MONTH_YEAR_REGION_BLOCK_STREET, [month, year, region, block, street])
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

def get_all_regions():
    with connection.cursor() as cursor:
        cursor.execute(ALL_REGIONS)
        return cursor.fetchall()


def handle_csv_file(input_file, a_file_type, associated_file):
    data_set = input_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)

    if a_file_type == FA_RISK:
        io_string = skip_lines_in_csv(io_string, 1)
        store_fa_risk(io_string, associated_file)
    elif a_file_type == TCU_DEFAULTER:
        io_string = skip_lines_in_csv(io_string, 5)
        store_tcu_defaulter(io_string, associated_file)
    elif a_file_type == IRMS:
        skip_lines_in_csv(io_string, 1)
        store_irms(io_string, associated_file)
    elif a_file_type == POSTAL_CODE:
        skip_lines_in_csv(io_string, 1)
        store_postal_code(io_string, associated_file)
    elif a_file_type == RENTAL_BLOCK:
        skip_lines_in_csv(io_string, 1)
        store_rental_block(io_string, associated_file)

def store_fa_risk(data_as_io_string, associated_file):
    new_fa_risks = []

    for column in csv.reader(data_as_io_string, delimiter = ',', quotechar = "|"):
        new_fa_risk = Fa_Risk(
            date_generated = datetime.datetime.strptime(column[0], '%m/%d/%Y'),
            patient_id = column[14],
            patient_name = set_null_if_nan(column[15]),
            patient_nric = set_null_if_nan(column[13]),
            house_block = column[23],
            #house_floor = column[24],
            house_floor = set_null_if_not_int(column[24]),
            house_unit = column[25],
            street = column[26],
            #postal_code = column[28],
            postal_code = set_null_if_not_int(column[28]),
            fa_risk = column[67],
            fa = column[68],
            file = associated_file,
        )
        new_fa_risks.append(new_fa_risk)
    Fa_Risk.objects.bulk_create(new_fa_risks)

def store_tcu_defaulter(data_as_io_string, associated_file):
    new_tcu_defaulters = []
    for column in csv.reader(data_as_io_string, delimiter = ','):
        new_tcu_defaulter = Tcu_Defaulter(
            date_generated = datetime.datetime.strptime(column[0], '%m/%d/%Y'),
            #serial_number = column[],
            patient_id = column[4],
            patient_name = column[2],
            patient_nric = column[3],
            postal_code =  set_null_if_not_int(column[5]),
            street = column[6],
            #designation = column[],
            house_block = column[8],
            house_floor = set_null_if_not_int(column[9]),
            house_unit = column[10],
            visit_type = column[11],
            first_visit_model = column[12],
            repeat_visit_model = column[13],
            overall_model = column[14],
            file = associated_file,
        )
        new_tcu_defaulters.append(new_tcu_defaulter)
    Tcu_Defaulter.objects.bulk_create(new_tcu_defaulters)

def store_irms(data_as_io_string, associated_file):
    new_irms_s = []
    for column in csv.reader(data_as_io_string, delimiter = ','):
        new_irms = Irms(
            patient_id = column[10],
            patient_name = column[8],
            patient_nric = column[9],
            postal_code =  set_null_if_not_int(column[11]),
            house_block = column[12],
            house_floor = set_null_if_not_int(column[13]),
            house_unit = column[14],
            street = column[15],
            latest_outcome = column[29],
            application_status = column[30],
            ref_submission_date = datetime.datetime.strptime(column[33], '%m/%d/%Y'),
            #submission_date_to_SP = datetime.datetime.strptime(column[34], '%m/%d/%Y'),
            #last_status_date = datetime.datetime.strptime(column[35], '%m/%d/%Y'),
            #pending_exec_date = datetime.datetime.strptime(column[36], '%m/%d/%Y'),
            file = associated_file,
        )
        new_irms_s.append(new_irms)
    Irms.objects.bulk_create(new_irms_s)

def store_postal_code(data_as_io_string, associated_file):
    new_postal_codes = []
    for column in csv.reader(data_as_io_string, delimiter = ','):
        new_postal_code = Postal_Code(
            region = column[0],
            low_bound = set_null_if_not_int(column[1]),
            high_bound = set_null_if_not_int(column[2]),
            file = associated_file,
        )
        new_postal_codes.append(new_postal_code)
    Postal_Code.objects.bulk_create(new_postal_codes)

def store_rental_block(data_as_io_string, associated_file):
    rental_blocks = []
    for column in csv.reader(data_as_io_string, delimiter = ','):
        if column[0] != '' and not 'Block No.' in column[0]  :
            rental_block = Rental_Block(
                house_block = column[0],
                street = column[1],
                postal_code =  set_null_if_not_int(column[2]),
            
                one_room_flat = convert_to_boolean('Y', 'N', column[3]),
                two_room_flat = convert_to_boolean('Y', 'N', column[4]),
                #application_zone = models.CharField(max_length = 100)
                file = associated_file,
            )
            rental_blocks.append(rental_block)
    Rental_Block.objects.bulk_create(rental_blocks)

def store_patient_info(patient_info):
    patient_info_list = []
    for row in patient_info:
        new_patient_info = Patient_Info(
            date_generated = row[0],
            patient_id = row[1],
            patient_name = row[2],
            patient_nric = row[3],
            house_block = row[4],
            house_floor = row[5],
            house_unit = row[6],
            street = row[7],
            postal_code = row[8],
            region = row[9]
            )
        patient_info_list.append(new_patient_info)
    Patient_Info.objects.bulk_create(patient_info_list)

def handle_excel_file(input_file, a_file_type, associated_file):
    if a_file_type == FA_RISK:
        data_set = pd.read_excel(input_file, skiprows = 0)
        data_set = data_set.dropna(subset = ['FA_RISK', 'FA'])
        data_set = data_set.reset_index(drop = True)
        data_set = data_set.fillna('')
        store_fa_risk_excel(data_set, associated_file)
    elif a_file_type == TCU_DEFAULTER:
        data_set = pd.read_excel(input_file, skiprows = 3)
        data_set = data_set.fillna('')
        store_tcu_defaulter_excel(data_set, associated_file)
    elif a_file_type == IRMS:
        data_set = pd.read_excel(input_file, skiprows = 0)
        data_set = data_set.fillna('')
        store_irms_excel(data_set, associated_file)
    elif a_file_type == POSTAL_CODE:
        data_set = pd.read_excel(input_file, skiprows = 0)
        store_postal_code_excel(data_set, associated_file)
    elif a_file_type == RENTAL_BLOCK:
        sys.exit("Rental Block should be in csv format")

def store_fa_risk_excel(data_set, associated_file):
    new_fa_risks = []
    for ind in data_set.index:
        new_fa_risk = Fa_Risk(
            date_generated = data_set.iloc[ind][0],
            patient_id = data_set.iloc[ind][14],
            patient_name = set_null_if_nan(data_set.iloc[ind][15]),
            patient_nric = set_null_if_nan(data_set.iloc[ind][13]),
            house_block = data_set.iloc[ind][23],
            #house_floor = data_set[24],
            house_floor = set_null_if_not_int(data_set.iloc[ind][24]),
            house_unit = data_set.iloc[ind][25],
            street = data_set.iloc[ind][26],
            #postal_code = data_set[ind][28][ind],
            postal_code = set_null_if_not_int(data_set.iloc[ind][28]),
            fa_risk = data_set.iloc[ind][67],
            fa = data_set.iloc[ind][68],
            file = associated_file,
        )
        new_fa_risks.append(new_fa_risk)
    Fa_Risk.objects.bulk_create(new_fa_risks)

def store_tcu_defaulter_excel(data_set, associated_file):
    new_tcu_defaulters = []
    for ind, column in data_set.iterrows():
        new_tcu_defaulter = Tcu_Defaulter(
            date_generated = column.ix[0],
            #serial_number = column[],
            patient_id = column.ix[4],
            patient_name = set_null_if_nan(column.ix[2]),
            patient_nric = set_null_if_nan(column.ix[3]),
            postal_code =  set_null_if_not_int(column.ix[5]),
            street = column.ix[6],
            #designation = column[],
            house_block = column.ix[8],
            house_floor = set_null_if_not_int(column.ix[9]),
            house_unit = column.ix[10],
            visit_type = column.ix[11],
            first_visit_model = column.ix[12],
            repeat_visit_model = column.ix[13],
            overall_model = column.ix[14],
            file = associated_file,
        )
        new_tcu_defaulters.append(new_tcu_defaulter)
    Tcu_Defaulter.objects.bulk_create(new_tcu_defaulters)

def store_irms_excel(data_set, associated_file):
    new_irms_s = []
    for ind, column in data_set.iterrows():
        new_irms = Irms(
            patient_id = column[10],
            patient_name = set_null_if_nan(column[8]),
            patient_nric = set_null_if_nan(column[9]),
            postal_code =  set_null_if_not_int(column[11]),
            house_block = column[12],
            house_floor = set_null_if_not_int(column[13]),
            house_unit = column[14],
            street = column[15],
            latest_outcome = column[29],
            application_status = column[30],
            ref_submission_date = column[33],
            #submission_date_to_SP = datetime.datetime.strptime(column[34], '%m/%d/%Y'),
            #last_status_date = datetime.datetime.strptime(column[35], '%m/%d/%Y'),
            #pending_exec_date = datetime.datetime.strptime(column[36], '%m/%d/%Y'),
            file = associated_file,
        )
        new_irms_s.append(new_irms)
    Irms.objects.bulk_create(new_irms_s)

def store_postal_code_excel(data_set, associated_file):
    new_postal_codes = []
    for ind, column in data_set.iterrows():
        new_postal_code = Postal_Code(
            region = column[0],
            low_bound = set_null_if_not_int(column[1]),
            high_bound = set_null_if_not_int(column[2]),
            file = associated_file,
        )
        new_postal_codes.append(new_postal_code)
    Postal_Code.objects.bulk_create(new_postal_codes)

def get_default_file_name(file_type):
    if file_type == FA_RISK:
        return FILE_TYPE_CHOICES[0][1]
    elif file_type == TCU_DEFAULTER:
        return FILE_TYPE_CHOICES[1][1]
    elif file_type == IRMS:
        return FILE_TYPE_CHOICES[2][1]
    elif file_type == POSTAL_CODE:
        return FILE_TYPE_CHOICES[3][1]
    elif file_type == RENTAL_BLOCK:
        return FILE_TYPE_CHOICES[4][1]

# utilities
def set_null_if_not_int(value):
    try:
        integer = int(value)
        return integer
    except ValueError:
        return None

def set_null_if_nan(value):
    if value == 'nan':
        return None
    else:
        return value

def skip_lines_in_csv(data, lines):
    for i in range(lines):
        next(data)
    return data

def convert_to_boolean(val_if_true, val_if_false, value):
    if value == val_if_true:
        return True
    elif value == val_if_false:
        return False
    else:
        raise UnexpectedValueGiven
        return None