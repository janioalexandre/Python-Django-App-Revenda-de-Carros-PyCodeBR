from django import forms
from cars.models import Car, Brand

class CarForm(forms.Form):
    model = forms.CharField(label='Model', max_length=200)
    brand = forms.ModelChoiceField(Brand.objects.all(), label='Brand')
    factory_year = forms.IntegerField(label='Factory Year')
    model_year = forms.IntegerField(label='Model Year')
    plate = forms.CharField(label='Plate', max_length=10)
    value = forms.FloatField(label='Value')
    photo = forms.ImageField(label='Photo')

    def save(self):
        data = self.cleaned_data
        car = Car.objects.create(
            model=data['model'],
            brand=data['brand'],
            factory_year=data['factory_year'],
            model_year=data['model_year'],
            plate=data['plate'],
            value=data['value'],
            photo=data['photo']
        )
        car.save()
        return car
