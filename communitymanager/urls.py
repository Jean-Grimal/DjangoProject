from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.communautes),
    path('communautes', views.communautes, name= 'communautes'),
    path('communaute/<id_de_la_communaute>', views.communaute, name='communaute'),
    path('communautes/abonnements/<id_de_la_communaute>', views.abonnement, name='abonnement'),
    path('communautes/desabonnement/<id_de_la_communaute>', views.desabonnement, name='desabonnement'),
    path('communautes/afficher/post/<int:id_du_post>', views.afficher_post, name='afficher_post'),
    path('communautes/nouveau/commentaire/post/<id_du_post>', views.nouveau_commentaire, name='nouveau_commentaire'),
    path('communautes/nouveau_post', views.nouveau_post, name='nouveau_post'),
    path('communautes/modif_post/<post_id>', views.modif_post, name='modif_post'),
    path('communautes/fil/actalite', views.afficher_fil_actu, name='fil_actualite'),
    path('communautes/like/<id_du_post>', views.like, name='like'),
    path('communautes/unlike/<id_du_post>', views.unlike, name='unlike'),
    path('communautes/filtrage/priorite', views.Filtrage_Priorite, name='filtrage_priorite'),
    path('communautes/filtrage/priorite/communaute', views.Filtrage_Priorite_Communaute, name='filtrage_priorite_communaute'),
]