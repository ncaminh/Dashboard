from django.db import models
from .choices import FILE_TYPE_CHOICES, FA_RISK

# Create your models here.

class File(models.Model):
    file_name = models.CharField(max_length = 100)
    upload_date_time = models.DateTimeField(auto_now = True)
    file_type = models.CharField(
        max_length = 2, 
        choices = FILE_TYPE_CHOICES, 
        default = FA_RISK,
    )

    def __str__(self):
        return self.file_name

class Fa_Risk(models.Model):
    date_generated = models.DateField()
    patient_id = models.CharField(max_length = 20)
    house_block = models.CharField(max_length = 10)
    house_floor = models.IntegerField(null = True)
    house_unit = models.CharField(max_length = 100)
    street = models.CharField(max_length = 100)
    postal_code = models.IntegerField(null = True)
    fa_risk = models.CharField(max_length = 100)
    fa = models.CharField(max_length = 100)
    file = models.ForeignKey(File, on_delete = models.CASCADE)

class Tcu_Defaulter(models.Model):
    date_generated = models.DateField()
    #serial_number = models.CharField(max_length = 20)
    patient_id = models.CharField(max_length = 20)
    postal_code =  models.IntegerField(null = True)
    street = models.CharField(max_length = 100)
    #designation = models.CharField(max_length = 100)
    house_block = models.CharField(max_length = 10)
    house_floor = models.IntegerField(null = True)
    house_unit = models.CharField(max_length = 100)
    visit_type = models.CharField(max_length = 10)
    first_visit_model = models.FloatField(null = True)
    repeat_visit_model = models.FloatField(null = True)
    overall_model = models.FloatField(null = True)
    file = models.ForeignKey(File, on_delete = models.CASCADE)

class Irms(models.Model):
    patient_id = models.CharField(max_length = 20)
    postal_code =  models.IntegerField(null = True)
    house_block = models.CharField(max_length = 10)
    house_floor = models.IntegerField(null = True)
    house_unit = models.CharField(max_length = 100)
    street = models.CharField(max_length = 100)
    ref_submission_date = models.DateField()
    #submission_date_to_SP = models.DateField()
    #last_status_date = models.DateField()
    #pending_exec_date = models.DateField()
    latest_outcome = models.CharField(max_length = 100)
    application_status = models.CharField(max_length = 100)
    file = models.ForeignKey(File, on_delete = models.CASCADE)

class Postal_Code(models.Model):
    region = models.CharField(max_length = 100)
    low_bound =  models.IntegerField(null = True)
    high_bound =  models.IntegerField(null = True)
    file = models.ForeignKey(File, on_delete = models.CASCADE)

class Rental_Block(models.Model):
    house_block = models.CharField(max_length = 10)
    postal_code =  models.IntegerField(null = True)
    street = models.CharField(max_length = 100)
    one_room_flat = models.BooleanField(null = True)
    two_room_flat = models.BooleanField(null = True)
    #application_zone = models.CharField(max_length = 100)
    file = models.ForeignKey(File, on_delete = models.CASCADE)

class Patient_Info(models.Model):
    date_generated = models.DateField()
    patient_id = models.CharField(max_length = 20)
    house_block = models.CharField(max_length = 10)
    house_floor = models.IntegerField(null = True)
    house_unit = models.CharField(max_length = 100)
    street = models.CharField(max_length = 100)
    postal_code = models.IntegerField(null = True)
    region = models.CharField(max_length = 100, null = True)