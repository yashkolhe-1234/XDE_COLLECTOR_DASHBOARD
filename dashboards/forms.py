"""
Forms for dashboard data management.
"""
from django import forms
from .models import PandharRaste


class PandharRasteForm(forms.ModelForm):
    """
    Form for adding/editing PandharRaste data.
    """
    class Meta:
        model = PandharRaste
        fields = [
            'taluka',
            'geo_tag_roads',
            'geo_tag_length_km',
            'cleared_roads',
            'cleared_length_km',
            'farmers_benefited',
        ]
        labels = {
            'taluka': 'तालुका',
            'geo_tag_roads': 'Geo-tag केलेले रस्ते',
            'geo_tag_length_km': 'Geo-tag लांबी (कि.मी.)',
            'cleared_roads': 'अतिक्रमण काढलेले रस्ते',
            'cleared_length_km': 'काढलेली लांबी (कि.मी.)',
            'farmers_benefited': 'लाभार्थी शेतकरी',
        }
        widgets = {
            'taluka': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'तालुका नाव प्रविष्ट करा'
            }),
            'geo_tag_roads': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0'
            }),
            'geo_tag_length_km': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'step': '0.01'
            }),
            'cleared_roads': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0'
            }),
            'cleared_length_km': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0',
                'step': '0.01'
            }),
            'farmers_benefited': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0'
            }),
        }

