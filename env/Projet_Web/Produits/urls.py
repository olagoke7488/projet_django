from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
  #pour l'admin
    #path('admin/', admin.site.urls),
  #  path('', home, name='home'),
   # path('',affichage.as_view(), name='home'),
  # path('ajout/',ajout_donnees,name='ajout'),
    
#piergy
    
    path('Acceuil/',Acceuil,name='Acceuil'),
    path('Acceuil/index.html',Acceuil,name='Acceuil'),
    path('adminP/',Acc,name='acc'),

    path('produit/', Affichage.as_view(), name='home'),
    path('ajout/', AjoutProduits.as_view(), name='ajout'),
    # path('modification/<int:id>/', modifier,name='modifier'),

    path('modication/<int:pk>/', update_donnees.as_view(), name='modifier'),
    # path('supprimer/<int:id>/', supprimer, name="supprimer"),
#    path ('detail/<int:id>/', detail,name='detail'),
    path('details/<int:pk>/', edit.as_view(),name='details'),
    
    path('delete/<int:pk>/', delete.as_view(),name='delete'),

    path('recherche/', recherche, name='recherche'),

    path('ajoutvente/<int:id>/', VenteProduits, name='ajoutvente'),
    path('commande/<int:id>/', commande, name='commande'),
    
    path('enregistrement-recu/<int:id>/', SaveRecu, name='saverecu'),
    path('saverecu/<int:id>/', SaveRecu, name='saverecu'),
    path('facture/<str:sale_id>/', Facture, name='facture'),
    # path('ajout/',ajout_donnees,name='ajout'),

    path('admin/', admin.site.urls),
    path('dashboard/', dashboard, name='dashboard'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
