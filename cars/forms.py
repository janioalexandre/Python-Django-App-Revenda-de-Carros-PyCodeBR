from django import forms

class CarForm(forms.Form):
    model = forms.CharField(label='Model', max_length=200)
    brand = forms.CharField(label='Brand', max_length=200)
    factory_year = forms.IntegerField(label='Factory Year')
    model_year = forms.IntegerField(label='Model Year')
    plate = forms.CharField(label='Plate', max_length=10)
    value = forms.FloatField(label='Value')
    photo = forms.ImageField(label='Photo')
