import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Autor, Gatunek, Ksiazka, InstancjaKsiazki, Wydawca, Bibliotekarz
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# required imports for prolongata

from katalog.forms import ProlongataForm
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

# required for user forms

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from katalog.models import Autor

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
    queryset = Autor.objects.all()
    template_name = 'autor_list.html'
    paginate_by = 10


class AutorSzczegolView(generic.DetailView):
    model = Autor
    template_name = 'autor_detail.html'


class KsiazkaListView(generic.ListView):
    model = Ksiazka
    context_object_name = 'moja_ksiazka_list'
    queryset = Ksiazka.objects.all()
    template_name = 'ksiazka_moja_list.html'
    paginate_by = 3


class KsiazkaSzczegolView(generic.DetailView):
    model = Ksiazka
    template_name = 'ksiazka_detail.html'


class KsiazkaCreate(CreateView):
    model = Ksiazka
    fields = ['tytul', 'autor', 'opis', 'isbn', 'gatunek']
    initial = {'opis': 'Twoja kolejna dodana ksiazka'}


class KsiakzaUpdate(UpdateView):
    model = Ksiazka
    fields = '__all__'


class KsiazkaDelete(DeleteView):
    model = Ksiazka
    success_url = reverse_lazy('ksiazki')


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
        return InstancjaKsiazki.objects.filter(wypozycza=self.request.user).filter(status__exact='w').order_by('data_zwrotu')


@login_required
def prolonguj_ksiazka_bibliotekarz(request, pk):
    instancja = get_object_or_404(InstancjaKsiazki, pk=pk)

    if request.method == 'POST':
        form = ProlongataForm(request.POST)
        if form.is_valid():
            instancja.data_zwrotu = form.cleaned_data['data_prolongaty']
            instancja.save()
            return HttpResponseRedirect(reverse('moje-pozyczone'))
    else:
        nowa_data_prolongaty = datetime.date.today() + datetime.timedelta(weeks=3)
        form = ProlongataForm(
            initial={'data_prolongaty': nowa_data_prolongaty}
        )

    context = {
        'form': form,
        'instancja': instancja,
    }

    return render(request, 'katalog/prolonguj_ksiazka_bibliotekarz.html', context)


class AutorCreate(CreateView):
    model = Autor
    fields = ['imie', 'nazwisko', 'data_urodzenia', 'data_smierci']
    initial = {'data_smierci': '12/30/2070'}


class AutorUpdate(UpdateView):
    model = Autor
    fields = '__all__'


class AutorDelete(DeleteView):
    model = Autor
    success_url = reverse_lazy('autorzy')
