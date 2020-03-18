from django import forms
from .choices import *

class UploadForm(forms.Form):
    file_type = forms.ChoiceField(choices = FILE_TYPE_CHOICES, label = "File type")
    file_field = forms.FileField(allow_empty_file = False)

class FilterFirstIterForm(forms.Form):
    month = forms.ChoiceField(choices = MONTH_CHOICES, label = "Month")
    year = forms.IntegerField(min_value = 1800, max_value = 3000)
    region = forms.ChoiceField(label = "Region")

    def __init__(self, region_choices, *args, **kwargs):
        self.region_choices = region_choices
        super(FilterFirstIterForm, self).__init__(*args, **kwargs)
        self.fields['region'].choices = self.region_choices

class FilterSecondIterForm(forms.Form):
    block_street = forms.ChoiceField(label = "Block - Street")

    def __init__(self, block_street_choices, *args, **kwargs):
        self.block_street_choices = block_street_choices
        super(FilterSecondIterForm, self).__init__(*args, **kwargs)
        self.fields['block_street'].choices = self.block_street_choices





