from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from .forms import *

from django.contrib import messages
from datetime import datetime

from .models import *


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.

# def home(request):

#     # # récuperationndes données
#     # donnees = Produits.objects.all()

#     # context = {
#     #     'donnees':donnees
#     # }

# # , context
#     return render(request,'home.html')


@login_required(login_url='login')
def Acc(request):

    return render(request, 'acc.html')


class Affichage(LoginRequiredMixin, ListView):

    # Affichage du template
    template_name = 'home.html'
    # Récupération des données
    queryset = Produits.objects.all()



# Class dj'ajout des données

class AjoutProduits(LoginRequiredMixin, CreateView):

    # utilisation du modele
    model = Produits
    # specifier le forulaire à utiliser
    form_class = AjoutProduit
    # afichage du template
    template_name = 'ajout-donnees.html'
    # redirection après enregistrement 
    success_url = reverse_lazy('home') 




# class pour la modification

class update_donnees(LoginRequiredMixin, UpdateView):

    # recuperation du model
    model = Produits
    # specifier le formulaire
    form_class = AjoutProduit
    # princision du templates
    template_name = 'modification.html'
    # redirection
    success_url = reverse_lazy('home')


# fonction pour supprimer 
# @login_required(login_url='login')
# def supprimer(request, id):
#     if request.method =="POST":
#         produit = get_object_or_404(Produits, id=id)
#         produit.delete()
#         return JsonResponse({'success':True, 'message': "Le produit a été supprimé avec succès"})
#     return JsonResponse({'success': False, 'message': "Methode non autorisée" })

# class pour supprimer les données
class delete(LoginRequiredMixin, DeleteView):

    model = Produits
    template_name = "delete.html"
    success_url = reverse_lazy('home')


# fonction de recher de produit
@login_required(login_url='login')
def recherche(request):

    type_bouteille = request.GET.get('type')
    marque = request.GET.get('marque')
    resultats = Produits.objects.all()
    if type_bouteille:
        resultats = resultats.filter(name__iexact=type_bouteille)
    if marque:
        resultats = resultats.filter(description__icontains=marque)
    context = {
        'donnees': resultats
    }
    return render(request, 'resultat_recheche.html', context)


# # fonction pour voir les details
    
# def detail(request, id):

#     n = Produits.objects.get(id=id)

#     return render(request, 'detail.html', {'n':n})


# class pour voir les details d'un produit 

class edit(LoginRequiredMixin, DetailView):

    model = Produits
    template_name = 'detail.html'
    context_object_name = 'n'



# fonction pour l'accueil

def Acceuil(request):
    context = {}
    context['produits'] = Produits.objects.filter(quantite__gt = 0)  # Récupération de tous les produits
    print(context['produits'])
    return render(request, 'index1.html', context)

#profil
from django.shortcuts import render
from .models import Produits

def dashboard(request):
    if request.method == 'POST':
        print(request.POST['element'].split('_')[0])
        if request.POST['element'].split('_')[0] == "vente":
            vente_id = request.POST['element'].split('_')[1]
            vente = get_object_or_404(Vente, id=vente_id)
            vente.delete()
            # Logique pour traiter la vente
            # Par exemple, vous pouvez rediriger vers une page de détails de la vente
            return redirect('dashboard')
        elif request.POST['element'].split('_')[0] == "commande":
            commande_id = request.POST['element'].split('_')[1]
            commande = get_object_or_404(PasserCommander, id=commande_id)
            commande.delete()
            # Logique pour traiter la commande
            return redirect('dashboard')
    # Récupération des produits pour le dashboard
    produits = Produits.objects.all()
    return render(request, 'Client/dashboard.html', {
        "historique1": Vente.objects.all(),
        "historique2": PasserCommander.objects.all(),
        'produits': produits,
        'user': request.user
    })

# fonction pour la vente
def VenteProduits(request, id):
    produit = get_object_or_404(Produits, id=id)
    message = None  # Variable pour stocker les messages d'erreur ou d'avertissement

    if request.method == 'POST':
        form = AjoutVente(request.POST)
        if form.is_valid():
            quantite = form.cleaned_data['quantite']
            customer_name = form.cleaned_data['customer']

            # Vérification si la quantité demandée est supérieure au stock
            if quantite > produit.quantite:
                message = "La quantité demandée dépasse le stock disponible !"
            else:
                customer, _ = Customer.objects.get_or_create(name=customer_name)

                # Calcul du montant total de la vente
                total_amount = produit.price * quantite

                # Enregistrement de la vente
                sale = Vente(produit=produit, quantite=quantite, total_amount=total_amount, customer=customer)
                sale.save()

                # Mise à jour de la quantité de vente dans le produit
                produit.quantite -= quantite
                produit.save()

                # Redirection vers la page de reçu
                return redirect('facture', sale_id=sale.id)
    else:
        form = AjoutVente()

    # Vérification si le stock est bas (par exemple <= 5)
    if produit.quantite <= 5 and not message:
        message = "Attention, le stock est bas !"

    context = {
        'produit': produit,
        'form': form,
        'message': message  # Passer le message au template
    }
    return render(request, 'fomulaire_vente.html', context)
    


#FUNction pour la facture
def SaveRecu(request, id):

    vente = get_object_or_404(Vente, id=id)
    customer = vente.customer
    quantite = vente.quantite
    total_amount = vente.total_amount
    produit = vente.produit

    recu = Facture_Client(
        customer = customer,
        quantite = quantite,
        total_amount = total_amount,
        produit = produit
    )

    recu.save()

    return redirect('facture', sale_id = id)


#  fonction pour afficher les données de la vente

def Facture(request, sale_id):

    if len(sale_id.split('-')) > 1:
        # If sale_id is a string with a hyphen, split it and take the first part
        sale_id = sale_id.split('-')[1]
        sale = get_object_or_404(PasserCommander, id=int(sale_id))
        customer = sale.nom_complet
        produit = sale.id_produit
        quantite = sale.quantite
        sale_date = sale.date_livraison
        total_amount = sale.total_amount
    else:
        sale = get_object_or_404(Vente, id=int(sale_id))
        customer = sale.customer
        produit = sale.produit
        quantite = sale.quantite
        sale_date = sale.sale_date
        total_amount = sale.total_amount
    

    print(quantite)
    context = {
        'sale':sale,
        'customer':customer,
        'produit':produit,
        'quantite':quantite,
        'sale_date': sale_date,
        'id':sale.id,
        'prix_unitaire': produit.price,
        'total_amount':total_amount
    }
    return render(request, 'facture-client.html', context)


class vente(ListView):
    template_name = 'vente.html'
    queryset = Vente.objects.all()

def recu(request):
    recus = Facture_Client.objects.all()
    return render (request, 'recu.html',{'recus': recus})


def commande(request,id):
    produit = get_object_or_404(Produits, id=id)
    if request.method == 'POST':
        nom_Complet = request.POST.get('customer')
        telephone = request.POST.get('telephone')
        localisation = request.POST.get('localisation')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        quantite = request.POST.get('quantite')
        date_livraison = request.POST.get('date_livraison')
        print(nom_Complet, telephone, localisation, heure_debut, heure_fin, quantite, date_livraison)

        try:
            
            # Récupération des données POST
            nom_Complet = request.POST.get('customer')
            telephone = request.POST.get('telephone')
            localisation = request.POST.get('localisation')
            heure_debut = request.POST.get('heure_debut')
            heure_fin = request.POST.get('heure_fin')
            quantite = request.POST.get('quantite')
            date_livraison = request.POST.get('date_livraison')
            print(nom_Complet, telephone, localisation, heure_debut, heure_fin, quantite, date_livraison,)

            # Conversion et récupération des objets liés
            produit = Produits.objects.get(id=id)

            passeCommand = PasserCommander(
                id_produit=produit,
                nom_complet=nom_Complet,
                telephone=telephone,
                localisation=localisation,
                heure=f"{heure_debut} - {heure_fin}",
                quantite=int(quantite),
                date_livraison=date_livraison,
                total_amount= int(quantite)  * produit.price # Calcul du montant total,
            )  
            passeCommand.save() 
            print(111)

            return redirect('facture', sale_id = "t-" + str(passeCommand.id))  # ou toute autre page

        except Exception as e:
            print(e)
            messages.error(request, f"Erreur : {str(e)}")

    return render (request, 'fomulaire_commande.html', {'produit': produit})


# fonction pour modifier les donnees 

# def modifier(request, id):

#     produit= get_object_or_404(Produits, id=id)
#     categories= Categories.objects.all()
#     errors = {}

#     if request.method == 'POST':
#         name = request.POST.get('name')
#         category_id = request.POST.get('category')
#         price = request.POST.get('price')
#         quantite = request.POST.get('quantite')
#         description = request.POST.get('description')
#         date_expiration = request.POST.get('date_expiration')
#         image = request.FILES.get('image')


#         # validation des champs

#         if not name:
#             errors['name'] = "Le nom est requis"

#         if not category_id:
#             errors['category'] = "La categorie est requise"

#         if not price:
#             errors['price'] = "Le prix est requis"

#         if not quantite:
#             errors['quantite'] = "La quantite est requise"

#         if not description:
#             errors['description'] = "La description est requise"


#         if date_expiration:
#             try:
#                 datetime.strptime(date_expiration, '%Y-%m-%d')
#             except ValueError:
#                 errors['date_expiration'] = "Le format de la date d'expiration est incorrect. Utilisez le format AAAA-MM-JJ."

        
#         if not errors:

#             category = get_object_or_404(Categories, id=category_id)
#             produit.name = name
#             produit.category = category
#             produit.price = price
#             produit.quantite = quantite
#             produit.description = description
#             produit.date_expiration = date_expiration


#             if image:
                
#                 fs = FileSystemStorage()
#                 filname= fs.save(name.name, image)
#                 produit.image = fs.url(filname)



#         produit.save()
#         messages.success(request, "Le produit a été modifié avec succès !")
#         return redirect("home")
    
#     else:

#         for key, errror  in errors.items():
#             messages.error(request, errror)

#     return render (request, "modification.html",{'produit':produit, 'categories':categories, 'errors':errors} )
    
    


  




    

# fonction d'ajout des données

# def ajout_donnees(request):
#     errors = {}
    
#     if request.method == 'POST':
#         name = request.POST['name']
#         price_str = request.POST['price']
#         quantite = request.POST['quantite']
#         date_expiration_str = request.POST['date_expiration']
#         description = request.POST['description']
#         image = request.FILES['image']

#         # Valider la date
#         try:
#             date_expiration = datetime.strptime(date_expiration_str, '%Y-%m-%d')
#         except ValueError:
#             errors['date_expiration'] = 'Le format de la date est incorrect. Utilisez le format AAAA-MM-JJ.'

#         # Valider le prix
#         try:
#             price = float(price_str)
#             if price < 0:
#                 errors['price'] = 'Le prix ne peut pas être négatif.'
#         except ValueError:
#             errors['price'] = 'Veuillez entrer un prix valide.'

#         # Si aucune erreur, sauvegarder le produit
#         if not errors:
#             try:
#                 # Récupération des catégories dans la table en fonction de la clé primaire
#                 category = Categories.objects.get(pk=request.POST['category'])

#                 savedonnes = Produits(
#                     name=name,
#                     price=price,
#                     quantite=quantite,
#                     description=description,
#                     date_expiration=date_expiration,
#                     category=category,
#                     image=image
#                 )
#                 savedonnes.save()
#                 messages.success(request, 'Produit ajouté avec succès!')
#                 return redirect('home')
#             except Categories.DoesNotExist:
#                 errors['category'] = 'La catégorie spécifiée est introuvable.'
#             except KeyError as e:
#                 errors[str(e)] = f'Le champ {e} est manquant dans la requête.'
#             except Exception as e:
#                 messages.error(request, f'Une erreur est survenue : {e}')

#     category = Categories.objects.all()  # Notez les parenthèses ici

#     return render(request, "ajout-donnees.html", {"category": category, "errors": errors})



# def search_products(request):
#     query = request.GET.get('q', '')
#     produits = Produits.objects.filter(name__icontains=query)
#     return render(request, 'search_results.html', {'produit': produits, 'query': query})


# from django.contrib.auth import login ,authenticate,logout

# from django.contrib import messages

# def Connexion_Compte(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('acc')
#         else:
#             messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")  # Utilisation du framework de messages
#             return redirect('login')  # Rediriger pour éviter la soumission multiple du formulaire
#     return render(request, 'login.html')



import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render

def Creation_Compte(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # Vérification des mots de passe
        if password != password_confirm:
            messages.error(request, 'Les mots de passe ne sont pas identiques. Veuillez réessayer.')
            return redirect('creation')

        # Vérification de la longueur et des caractères spéciaux du mot de passe
        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères, incluant des lettres, des chiffres et des caractères spéciaux.')
            return redirect('creation')

        # Vérification du format de l'adresse e-mail
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Adresse e-mail invalide. Veuillez entrer une adresse e-mail valide.')
            return redirect('creation')

        # Vérification de l'existence de l'utilisateur et de l'adresse e-mail
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
            return redirect('creation')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse e-mail est déjà utilisée. Veuillez en choisir une autre.")
            return redirect('creation')

        # Création de l'utilisateur
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Compte créé avec succès. Connectez-vous maintenant.')

        # Redirection vers la page de connexion
        return redirect('login')

    return render(request, 'creation.html')





