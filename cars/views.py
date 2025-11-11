from cars.models import Car
from cars.forms import CarModelForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
    ordering = ['-id']

    def get_queryset(self):
        cars = super().get_queryset().order_by('-id')
        search = (self.request.GET.get('search') or '').strip()
        if search:
            # Search by model or brand name; if numeric, also match years
            query = Q(model__icontains=search) | Q(brand__name__icontains=search)
            try:
                year = int(search)
                query |= Q(factory_year=year) | Q(model_year=year)
            except ValueError:
                pass
            cars = cars.filter(query)
        return cars

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'

    def form_valid(self, form):
        response = super().form_valid(form)
        car_name = f"{self.object.brand} - {self.object.model}"
        messages.success(self.request, f'O veículo <strong>{car_name}</strong> foi cadastrado com sucesso!')
        return response

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        car_name = f"{self.object.brand} - {self.object.model}"
        messages.success(self.request, f'O veículo <strong>{car_name}</strong> foi atualizado com sucesso!')
        return response

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'

    def form_valid(self, form):
        car_name = f"{self.object.brand} - {self.object.model}"
        messages.success(self.request, f'O veículo <strong>{car_name}</strong> foi excluído com sucesso!')
        return super().form_valid(form)
