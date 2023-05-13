from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Autor, Gatunek, Ksiazka, InstancjaKsiazki, Wydawca, Bibliotekarz
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def index(request):
    num_ks = Ksiazka.objects.all().count()
    num_in = InstancjaKsiazki.objects.all().count()
    num_in_d = InstancjaKsiazki.objects.filter(status__exact='d').count()
    num_au = Autor.objects.count()
    num_wyd = Wydawca.objects.count()
    num_bib = Bibliotekarz.objects.count()

    return render(
        request,
        'index.html',
        context={
            'num_ks': num_ks,
            'num_in': num_in,
            'num_in_d': num_in_d,
            'num_au': num_au,
            'num_wyd': num_wyd,
            'num_bib': num_bib

        }
    )


class AutorListView(generic.ListView):
    model = Autor
    context_object_name = 'autor_list'
    queryset = Autor.objects.filter(imie__icontains=' ')[:5]
    template_name = 'autor_list.html'


class KsiazkaListView(generic.ListView):
    model = Ksiazka
    context_object_name = 'moja_ksiazka_list'
    queryset = Ksiazka.objects.all()
    template_name = 'ksiazka_moja_list.html'
    paginate_by = 3


class KsiazkaSzczegolView(generic.DetailView):
    model = Ksiazka
    template_name = 'ksiazka_detail.html'


class WydawcaListView(generic.ListView):
    model = Wydawca
    context_object_name = 'wydawca_list'
    queryset = Wydawca.objects.all()
    template_name = 'wydawca_list.html'
    paginate_by = 2


class WydawcaSzczegolView(generic.DetailView):
    model = Wydawca
    template_name = 'wydawca_detail.html'


class BibliotekarzListView(generic.ListView):
    model = Bibliotekarz
    context_object_name = 'bibliotekarz_list'
    queryset = Bibliotekarz.objects.all()
    template_name = 'bibliotekarz_list.html'
    paginate_by = 1


class BibliotekarzSzczegolView(generic.DetailView):
    model = Bibliotekarz
    template_name = 'bibliotekarz_detail.html'


class KsiazkiUzytkownikaListView(LoginRequiredMixin, generic.ListView):
    model = InstancjaKsiazki
    template_name = 'KsiazkiUzytkownika.html'
    paginate_by = 2

    def get_queryset(self):
        return InstancjaKsiazki.objects.filter(wypozycza=self.request.user).filter(status__exact='o').order_by('data_zwrotu')
