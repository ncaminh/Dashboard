import json, os, pandas as pd
import numpy as np
import time

def check_file(filename, **kwargs):

    """Read file with **kwargs; files supported: xls, xlsx, csv, csv.gz, pkl"""

    read_map = {'xls': pd.read_excel, 'xlsx': pd.read_excel, 'csv': pd.read_csv,
                'gz': pd.read_csv, 'pkl': pd.read_pickle}
    if (filename.endswith(('.xls', '.xlsx'))):
        return 1;
    elif (filename.endswith('.csv')):
        return 2;             

    return 0;



def extract_data_from_file(filename, file_type, **kwargs):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("A:" + current_time)

    if (file_type == 1):
        print("jjnjn")
        df = pd.read_excel(filename, sheet_name='Working', skiprows = 3);
    else:
        print("aaaaaa")
        df = pd.read_csv(filename);
    
    print("cccccccc")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("B:" + current_time)

    df = df.rename(columns=lambda x: x.replace('\n',''));
    df = df.replace("Y", 1)

    json_file = open('blockMapping/JSON/diseases_mapping.json', 'r', encoding='utf-8');
    diseases_mapping = json.load(json_file);
    json_file.close();

    for main_disease in diseases_mapping.keys():
        if main_disease in df.columns:
            df = df.drop(columns=main_disease);
        if (isinstance(diseases_mapping[main_disease], str)):
            df[main_disease] = df[diseases_mapping[main_disease]];
        else:
            # df[main_disease] = df.apply(lambda row : insert_main_columns(row, diseases_mapping[main_disease]), axis=1);
            sub_diseases = diseases_mapping[main_disease]
            df[main_disease] = df[sub_diseases].sum(axis = 1, skipna = True) / df[sub_diseases].sum(axis = 1, skipna = True)

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("C:" + current_time)

    diseaseList = df.columns[10:]

    table = df.pivot_table(values=diseaseList, index=['Planning Area', 'Sub Zone'], aggfunc="count");
    result = {
        'ToaPayoh': [table.loc['Toa Payoh'].index.values.tolist()] + [table.columns.values.tolist()] + table.loc['Toa Payoh'].values.tolist(), 
        'AMK': [table.loc['Ang Mo Kio'].index.values.tolist()] + [table.columns.values.tolist()] + table.loc['Ang Mo Kio'].values.tolist(),
        'Hougang': [table.loc['Hougang'].index.values.tolist()] + [table.columns.values.tolist()] + table.loc['Hougang'].values.tolist(),
        'Bishan': [table.loc['Bishan'].index.values.tolist()] + [table.columns.values.tolist()] + table.loc['Bishan'].values.tolist(),
        'Serangoon': [table.loc['Serangoon'].index.values.tolist()] + [table.columns.values.tolist()] + table.loc['Serangoon'].values.tolist(),
        'Geylang': [table.loc['Geylang'].index.values.tolist()] + [table.columns.values.tolist()] + table.loc['Geylang'].values.tolist(),
        'Novena': [table.loc['Novena'].index.values.tolist()] + [table.columns.values.tolist()] + table.loc['Novena'].values.tolist(),
        'Kallang': [table.loc['Kallang'].index.values.tolist()] + [table.columns.values.tolist()] + table.loc['Kallang'].values.tolist(),
        'Rochor': [table.loc['Rochor'].index.values.tolist()] + [table.columns.values.tolist()] + table.loc['Rochor'].values.tolist(),
        'Novena-Kallang-Rochor': [table.loc[['Novena', 'Kallang', 'Rochor']].index.get_level_values(1).values.tolist()] + [table.columns.values.tolist()] + table.loc[['Novena', 'Kallang', 'Rochor']].values.tolist(), 
    }
    
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("D:" + current_time)

    with open('blockMapping/JSON/df.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)



    return result; 

def insert_main_columns(row, diseases):
  for disease in diseases:
    if not (pd.isna(row[disease])): return 1;
  return np.nan;