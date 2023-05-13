from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ksiazki/', views.KsiazkaListView.as_view(), name='ksiazki'),
    path('autorzy/', views.AutorListView.as_view(), name='autorzy'),
    path('ksiazka/<int:pk>', views.KsiazkaSzczegolView.as_view(),
         name='ksiazka-detail'),
    path('wydawcy/', views.WydawcaListView.as_view(), name='wydawcy'),
    path('wydawca/<int:pk>', views.WydawcaSzczegolView.as_view(),
         name='wydawca-detail'),
    path('bibliotekarze/', views.BibliotekarzListView.as_view(), name='bibliotekarze'),
    path('bibliotekarz/<int:pk>', views.BibliotekarzSzczegolView.as_view(),
         name='bibliotekarz-detail'),
    path('mojeksiazki/', views.KsiazkiUzytkownikaListView.as_view(),
         name='moje-pozyczone'),
]
