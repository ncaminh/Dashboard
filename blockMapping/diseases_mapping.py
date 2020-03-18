import json;

Map_list = {
	"Cardiovascular Disease": ['Coronary Heart Disease', 'Atrial Fibrillation', 'Heart Failure', 'Hypertension', 'Pregnancy Induced Hypertension', 'Dyslipidaemia', 'Peripheral Vascular Disease'],
	"Diabetes": ['Pre-Diabetes', 'Gestational Diabetes Mellitus', 'Diabetes Mellitus'],
	"Mental Health": ['Alcohol Intoxication', 'Anxiety', 'Bipolar Disorder', 'Dementia', 'Depression', 'Insomnia', 'Intellectual Disability', 'Schizophrenia', 'Substance Abuse'],
	"Neurology": ['Stroke', "'Parkinson's Disease'", 'Epilepsy'],
	"Orthopaedics": ['Osteopenia', 'Osteoporosis', 'Hip Fracture', 'Spine Fracture', 'Osteoarthritis', 'Rheumatoid Arthritis'],
	"Renal": 'Chronic Kidney Disease',
	"Respiratory": ['Asthma', 'COPD'],
	"Urology": ['Benign Prostatic Hyperplasia', 'Nephritis/Nephrosis'],
}

with open('JSON/diseases_mapping.json', 'w') as f:
	json.dump(Map_list, f, ensure_ascii=False, indent=4)