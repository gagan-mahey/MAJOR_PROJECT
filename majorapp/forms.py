from django import forms
from majorapp.models import add_property

class add_property_form(forms.ModelForm):
    class Meta:
        model = add_property
        fields = ["property_name","property_category","property_price","sale_price","property_image","details"]