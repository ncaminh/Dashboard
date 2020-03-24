from . import database as database_file

DATABASE_NAME = database_file.DATABASE_NAME

PATIENT_INFO_INITIALIZATION = """
SELECT 
	MAX(date_generated) as date_generated 
	,patient_id
    ,MAX(patient_name) as patient_name
    ,MAX(patient_nric) as patient_nric
	,MAX(house_block) as house_block
	,MAX(house_floor) as house_floor
	,MAX(house_unit) as house_unit
	,MAX(street) as street
	,MAX(postal_code) as postal_code
    ,postal_code.region as region
FROM 
(SELECT
	MAX(date_generated) as date_generated
	,patient_id
    ,MAX(patient_name) as patient_name
    ,MAX(patient_nric) as patient_nric
	,MAX(house_block) as house_block
	,MAX(house_floor) as house_floor
	,MAX(house_unit) as house_unit
	,MAX(street) as street
	,MAX(postal_code) as postal_code
FROM """ + DATABASE_NAME + """.ulm_fa_risk as fa
INNER JOIN """ + DATABASE_NAME + """.ulm_file as f
	ON fa.file_id = f.id
WHERE
	f.file_name = 'FA Risk'
    AND fa != ''
    AND fa_risk != ''
GROUP BY patient_id, MONTH(date_generated), YEAR(date_generated)

UNION

SELECT
	MAX(date_generated)
    ,patient_id
    ,MAX(patient_name) as patient_name
    ,MAX(patient_nric) as patient_nric
	,MAX(house_block) as house_block
	,MAX(house_floor) as house_floor
	,MAX(house_unit) as house_unit
	,MAX(street) as street
	,MAX(postal_code) as postal_code
FROM """ + DATABASE_NAME + """.ulm_tcu_defaulter as tcu
INNER JOIN """ + DATABASE_NAME + """.ulm_file as f
	ON tcu.file_id = f.id
WHERE f.file_name = 'TCU Defaulter'
GROUP BY patient_id, MONTH(date_generated), YEAR(date_generated)

UNION

SELECT
	MAX(ref_submission_date) as date_generated
    ,patient_id
    ,MAX(patient_name) as patient_name
    ,MAX(patient_nric) as patient_nric
	,MAX(house_block) as house_block
	,MAX(house_floor) as house_floor
	,MAX(house_unit) as house_unit
	,MAX(street) as street
	,MAX(postal_code) as postal_code
FROM """ + DATABASE_NAME + """.ulm_irms as irms
INNER JOIN """ + DATABASE_NAME + """.ulm_file as f
	ON irms.file_id = f.id
WHERE 
	f.file_name = 'IRMS'
GROUP BY
	patient_id, MONTH(ref_submission_date), YEAR(ref_submission_date)
) AS temp_pat_id
LEFT JOIN """ + DATABASE_NAME +  """.ulm_postal_code as postal_code
	ON temp_pat_id.postal_code >= postal_code.low_bound
    AND temp_pat_id.postal_code <= postal_code.high_bound
GROUP BY patient_id, MONTH(date_generated), YEAR(date_generated)
"""

PATIENT_INFO = DATABASE_NAME + ".ulm_patient_info as pat_id"

FA_RISK_CLEAN = """(
SELECT
	MAX(date_generated) as fa_date
	,patient_id
	, CASE WHEN fa_risk = 'High' THEN true ELSE false END AS fa_risk_status
    , CASE WHEN fa = 'Yes' THEN TRUE ELSE FALSE END AS fa_status
FROM """ + DATABASE_NAME + """.ulm_fa_risk as fa
INNER JOIN """ + DATABASE_NAME + """.ulm_file as f
	ON fa.file_id = f.id
WHERE
	f.file_name = 'FA Risk'
    AND fa != ''
    AND fa_risk != ''
GROUP BY patient_id, MONTH(date_generated), YEAR(date_generated)
) AS fa_risk
"""

TCU_DEFAULTER_CLEAN = """( SELECT
	MAX(date_generated) as tcu_date
    ,patient_id
	,CASE 
		WHEN first_visit_model >= 0.4 THEN TRUE 
        WHEN overall_model >= 0.4 THEN TRUE
        ELSE FALSE
	END AS tcu_status
FROM """ + DATABASE_NAME + """.ulm_tcu_defaulter as tcu
INNER JOIN """ + DATABASE_NAME + """.ulm_file as f
	ON tcu.file_id = f.id
WHERE f.file_name = 'TCU Defaulter'
GROUP BY patient_id, MONTH(date_generated), YEAR(date_generated)
) AS tcu_defaulter
"""

IRMS_CLEAN = """(
SELECT
	MAX(ref_submission_date) as irms_ref_submission_date
    ,patient_id
	,CASE
		WHEN LOWER(latest_outcome) IN ('admit', 'accept/admit', 'admit as existing case') AND application_status = 'CASE CLOSED' THEN 'Admitted'
        WHEN LOWER(latest_outcome) IN ('pre assign withdrawn', 'pre assign withdrawn – bpr', 'reject by agency', 'withdrawal after revert back by agency', 'Withdrawn', 'withdrawn & case closed by referral source') AND application_status = 'CASE CLOSED' THEN 'Withdrawn'
        ELSE 'Undetermined'
	END AS irms_status
FROM """ + DATABASE_NAME + """.ulm_irms as irms
INNER JOIN """ + DATABASE_NAME + """.ulm_file as f
	ON irms.file_id = f.id
WHERE 
	f.file_name = 'IRMS'
GROUP BY
	patient_id, MONTH(ref_submission_date), YEAR(ref_submission_date)
) AS irms
"""

POSTAL_CODE = DATABASE_NAME + ".ulm_postal_code as postal_code"

RENTAL_BLOCK = """(
	SELECT
		postal_code
		,CASE 
			WHEN one_room_flat IS TRUE THEN TRUE
			WHEN two_room_flat IS TRUE THEN TRUE
			ELSE FALSE
		END AS rental_status
	FROM """ + DATABASE_NAME + """.ulm_rental_block
) AS rental_block
"""

STANDARD_TEMPLATE = """
SELECT
pat_id.patient_name AS 'Name'
 ,DATE_FORMAT(pat_id.date_generated, '%b %Y') as 'Month'
 ,pat_id.patient_id AS 'Patient Id'
 ,pat_id.patient_nric AS 'NRIC'
 ,pat_id.house_block
 ,pat_id.house_floor
 ,pat_id.house_unit
 ,pat_id.street
 ,pat_id.region AS 'Region'
 ,pat_id.postal_code
 ,CASE 
    WHEN fa_risk_status IS TRUE THEN 'High'
    WHEN fa_risk_status IS FALSE THEN 'Low'
    ELSE 'NA'
END AS 'FA Risk (H2H)'
 ,CASE 
    WHEN fa_status IS TRUE THEN 'Yes'
    WHEN fa_status IS FALSE THEN 'No'
    ELSE 'NA'
END AS 'FA'
,CASE 
    WHEN tcu_status IS TRUE THEN 'Yes'
    WHEN tcu_status IS FALSE THEN 'No'
    ELSE 'NA'
END AS 'TCU Defaulter'
,CASE 
    WHEN irms_status IS NULL THEN 'NA'
	ELSE irms_status
END AS 'Referral Status'
 ,CASE 
    WHEN rental_status IS True THEN 'Yes'
END AS 'Rental Status'
 
FROM """ + PATIENT_INFO + \
""" LEFT JOIN """ + FA_RISK_CLEAN + \
"""	ON (
	    MONTH(pat_id.date_generated) = MONTH(fa_date)
	    AND YEAR(pat_id.date_generated) = YEAR(fa_date)
        AND pat_id.patient_id = fa_risk.patient_id
	)
LEFT JOIN """ + TCU_DEFAULTER_CLEAN + \
"""	ON (
	    MONTH(pat_id.date_generated) = MONTH(tcu_date)
	    AND YEAR(pat_id.date_generated) = YEAR(tcu_date)
        AND pat_id.patient_id = tcu_defaulter.patient_id
	)
LEFT JOIN """ + IRMS_CLEAN + \
"""	ON (
		MONTH(pat_id.date_generated) = MONTH(irms_ref_submission_date)
	    AND YEAR(pat_id.date_generated) = YEAR(irms_ref_submission_date)
        AND pat_id.patient_id = irms.patient_id
    )
LEFT JOIN """ + RENTAL_BLOCK + \
"""	ON pat_id.postal_code= rental_block.postal_code
"""

FILTERED_MONTH_YEAR_REGION = """SELECT DISTINCT
CASE
	#WHEN RTRIM(house_block) = '' AND house_floor IS NOT NULL AND LEFT(street, LOCATE(' ',street) - 1) REGEXP '^[0-9]+$' THEN CONCAT(CONCAT(LEFT(street, LOCATE(' ',street) - 1), " - " ),SUBSTR(street FROM (INSTR(street, " ") )) )
    #WHEN RTRIM(house_block) = LEFT(street, LOCATE(' ',street) - 1) AND LEFT(street, LOCATE(' ',street) - 1) REGEXP '^[0-9]+$' THEN CONCAT(CONCAT(house_block, " - " ),SUBSTR(street FROM (INSTR(street, " ") )) )
    WHEN RTRIM(house_block) = '' AND house_floor IS NOT NULL THEN CONCAT("Empty - ", street)
    WHEN RTRIM(house_block) = '' AND house_floor IS NULL THEN CONCAT("Landed - ", street)
    ELSE CONCAT(house_block, " - ", street)
END AS 'Block - Street'
,CASE
	#WHEN RTRIM(house_block) = '' AND house_floor IS NOT NULL AND LEFT(street, LOCATE(' ',street) - 1) REGEXP '^[0-9]+$' THEN CONCAT(CONCAT(LEFT(street, LOCATE(' ',street) - 1), " - " ),SUBSTR(street FROM (INSTR(street, " ") )) )
    #WHEN RTRIM(house_block) = LEFT(street, LOCATE(' ',street) - 1) AND LEFT(street, LOCATE(' ',street) - 1) REGEXP '^[0-9]+$' THEN CONCAT(CONCAT(house_block, " - " ),SUBSTR(street FROM (INSTR(street, " ") )) )
    WHEN RTRIM(house_block) = '' AND house_floor IS NOT NULL THEN CONCAT("Empty - ", street)
    WHEN RTRIM(house_block) = '' AND house_floor IS NULL THEN CONCAT("Landed - ", street)
    ELSE CONCAT(house_block, " - ", street)
END AS 'Block - Street'
FROM """ + PATIENT_INFO + \
""" LEFT JOIN """ + FA_RISK_CLEAN + \
"""	ON (
		MONTH(pat_id.date_generated) = MONTH(fa_date)
		AND YEAR(pat_id.date_generated) = YEAR(fa_date)
        AND pat_id.patient_id = fa_risk.patient_id
	)
LEFT JOIN """ + TCU_DEFAULTER_CLEAN + \
"""	ON (
		MONTH(pat_id.date_generated) = MONTH(tcu_date)
		AND YEAR(pat_id.date_generated) = YEAR(tcu_date)
        AND pat_id.patient_id = tcu_defaulter.patient_id
	)
LEFT JOIN """ + IRMS_CLEAN + \
"""	ON (
		MONTH(pat_id.date_generated) = MONTH(irms_ref_submission_date)
		AND YEAR(pat_id.date_generated) = YEAR(irms_ref_submission_date)
        AND pat_id.patient_id = irms.patient_id
    )
WHERE
  	MONTH(date_generated) = %s
	AND YEAR(date_generated) = %s
    AND pat_id.region = %s
    AND (NOT(fa_risk_status = False AND fa_status = False AND tcu_status = False AND irms_status != 'Admitted')
	OR NOT(fa_risk_status = False AND fa_status = False AND tcu_status = False AND irms_status != 'Withdrawn')
	)

ORDER BY street, house_block"""

ALL_REGIONS = """SELECT DISTINCT pat_id.region, pat_id.region
FROM """ + PATIENT_INFO +\
""" ORDER BY pat_id.region
"""

FILTERED_MONTH_YEAR_REGION_BLOCK_STREET = """
SELECT
 pat_id.house_floor
 ,pat_id.house_unit
 ,pat_id.patient_id
 ,(fa_risk_status) as fa_risk_status
 ,(fa_status) as fa_status
 ,(tcu_status) as tcu_status
 ,(irms_status) as irms_status
 ,(rental_status) as rental_status
 
FROM """ + PATIENT_INFO + \
""" LEFT JOIN """ + FA_RISK_CLEAN + \
"""	ON (
		MONTH(pat_id.date_generated) = MONTH(fa_date)
		AND YEAR(pat_id.date_generated) = YEAR(fa_date)
        AND pat_id.patient_id = fa_risk.patient_id
	)
LEFT JOIN """ + TCU_DEFAULTER_CLEAN + \
"""	ON (
		MONTH(pat_id.date_generated) = MONTH(tcu_date)
		AND YEAR(pat_id.date_generated) = YEAR(tcu_date)
        AND pat_id.patient_id = tcu_defaulter.patient_id
	)
LEFT JOIN """ + IRMS_CLEAN + \
"""	ON (
		MONTH(pat_id.date_generated) = MONTH(irms_ref_submission_date)
		AND YEAR(pat_id.date_generated) = YEAR(irms_ref_submission_date)
        AND pat_id.patient_id = irms.patient_id
    )
LEFT JOIN """ + RENTAL_BLOCK + \
"""	ON pat_id.postal_code= rental_block.postal_code
    
WHERE MONTH(pat_id.date_generated) = %s
AND YEAR(pat_id.date_generated) = %s
AND pat_id.region = %s
AND RTRIM(house_block) = %s
AND street = %s
AND (NOT(fa_risk_status = False AND fa_status = False AND tcu_status = False AND irms_status != 'Admitted')
	OR NOT(fa_risk_status = False AND fa_status = False AND tcu_status = False AND irms_status != 'Withdrawn')
	)

ORDER BY house_floor, house_unit
"""