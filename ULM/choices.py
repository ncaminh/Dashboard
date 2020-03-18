import calendar

FA_RISK = 'FA'
TCU_DEFAULTER = 'TC'
IRMS = 'IR'
POSTAL_CODE = 'PC'
RENTAL_BLOCK = 'RB'
FILE_TYPE_CHOICES = [
    (FA_RISK, 'FA Risk'),
    (TCU_DEFAULTER, 'TCU Defaulter'),
    (IRMS, 'IRMS'),
    (POSTAL_CODE, 'Postal Code'),
    (RENTAL_BLOCK, 'Rental Block'),
]

MONTH_CHOICES = [
    (1, calendar.month_name[1]),
    (2, calendar.month_name[2]),
    (3, calendar.month_name[3]),
    (4, calendar.month_name[4]),
    (5, calendar.month_name[5]),
    (6, calendar.month_name[6]),
    (7, calendar.month_name[7]),
    (8, calendar.month_name[8]),
    (9, calendar.month_name[9]),
    (10, calendar.month_name[10]),
    (11, calendar.month_name[11]),
    (12, calendar.month_name[12]),
]

