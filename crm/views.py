from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import Client, Deal
from .forms import DealForm, ClientForm


class ClientListView(ListView):
    model = Client
    template_name = 'crm/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10  # Пагинация по 10 штук

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        # Логика поиска по имени, телефону или email
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset

class ClientDetailView(DetailView):
    model = Client
    template_name = 'crm/client_detail.html'
    context_object_name = 'client'


class DealCreateView(CreateView):
    model = Deal
    form_class = DealForm
    template_name = 'crm/deal_form.html'

    def get_success_url(self):
        return reverse_lazy('client_detail', kwargs={'pk': self.object.client.pk})

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    success_url = reverse_lazy('client_list')