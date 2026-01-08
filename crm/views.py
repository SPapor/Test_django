from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Client, Deal


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