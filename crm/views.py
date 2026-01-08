from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import Client, Deal
from .forms import DealForm, ClientForm, NoteForm


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

class DealDetailView(DetailView):
    model = Deal
    template_name = 'crm/deal_detail.html'
    context_object_name = 'deal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note_form'] = NoteForm()
        return context

def add_note(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.deal = deal
            note.save()
    return redirect('deal_detail', pk=pk)