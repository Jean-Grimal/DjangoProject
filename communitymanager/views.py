from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

# Create your views here.
from .models import Communaute, Post, Commentaire,priorite
from .forms import FormulaireCom, Ecrire_Un_post, FormulaireFiltrage, FormulaireFiltrageCommu


def communautes(request):
    if request.user.is_authenticated:
        commus = Communaute.objects.all()

        communautes_suivies = []
        communautes_non_suivies = []


        for commu in commus:
            if commu.recherche_abonnement(request.user):
                communautes_suivies.append(commu)
            else:
                communautes_non_suivies.append(commu)

        return render(request, 'communautes.html', locals())

    else:
        return redirect('login')


def abonnement(request, id_de_la_communaute):
    commu = Communaute.objects.get(id=id_de_la_communaute)
    commu.abonnes.add(request.user)
    return redirect('communautes')


def desabonnement(request, id_de_la_communaute):
    commu = Communaute.objects.get(id=id_de_la_communaute)
    commu.abonnes.remove(request.user)
    return redirect('communautes')


def communaute(request, id_de_la_communaute):
    posts_aime = []
    posts_vus = []
    posts_ecarlates = []
    posts_rouges = []
    posts_oranges = []
    posts_jaunes = []
    all_posts = Post.objects.all()
    for post in all_posts :
        prio = post.priorite
        if post.recherche_vue(request.user):
            posts_vus.append(post)
        if post.recherche_like(request.user):
            posts_aime.append(post)
        if prio.label == 'Ecarlate':
            posts_ecarlates.append(post)
        if prio.label == 'Rouge':
            posts_rouges.append(post)
        if prio.label == 'Orange':
            posts_oranges.append(post)
        if prio.label == 'Jaune':
            posts_jaunes.append(post)
    commu = Communaute.objects.get(id=id_de_la_communaute)
    Posts = Post.objects.filter(communaute__id=id_de_la_communaute)
    Utilisateur = request.user
    return render(request, 'communaute.html', locals())


def afficher_post(request, id_du_post):
    auteur = request.user
    users = User.objects.all()
    post = Post.objects.get(id=id_du_post)
    Prio = post.priorite
    Commu = post.communaute
    couleur = Prio.label
    post.vues.add(request.user)
    commentaires = Commentaire.objects.filter(post__id=id_du_post)
    nb_commentaires = commentaires.count()
    a_aime = post.recherche_like(request.user)
    nb_likes = 0
    for utilisateur in users :
        if post.recherche_like(utilisateur):
            nb_likes +=1

    return render(request, 'post.html', locals())


def nouveau_commentaire(request, id_du_post):

    post = Post.objects.get(id=id_du_post)

    form = FormulaireCom(request.POST or None)

    if form.is_valid():
        commentaire = form.save(commit=False)
        commentaire.auteur = request.user
        commentaire.post = post

        commentaire.save()

        return redirect('afficher_post', id_du_post= post.id)

    else:

        return render(request, 'commentaire.html', locals())


def nouveau_post(request):

    form = Ecrire_Un_post(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.auteur = request.user
        post.save()
        return redirect('afficher_post', id_du_post= post.id)
    return render(request, 'Nouveau_post.html', locals())

def modif_post(request, post_id):
    """
    permet de modifier un post
    """
    post = Post.objects.get(id=post_id)

    if not post.auteur == request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = Ecrire_Un_post(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('afficher_post', id_du_post=post.id)

    else:
        form = Ecrire_Un_post(instance=post)
        return render(request, 'modif_post.html', locals())

def afficher_fil_actu(request):
    if request.user.is_authenticated:
        commus = Communaute.objects.all()
        Utilisateur = request.user
        tous_les_posts = Post.objects.none()

        posts_aime = []
        posts_vus = []
        posts_ecarlates = []
        posts_rouges = []
        posts_oranges = []
        posts_jaunes = []
        all_posts = Post.objects.all()
        for post in all_posts:
            prio = post.priorite
            if post.recherche_vue(request.user):
                posts_vus.append(post)
            if post.recherche_like(request.user):
                posts_aime.append(post)
            if prio.label == 'Ecarlate':
                posts_ecarlates.append(post)
            if prio.label == 'Rouge':
                posts_rouges.append(post)
            if prio.label == 'Orange':
                posts_oranges.append(post)
            if prio.label == 'Jaune':
                posts_jaunes.append(post)

        for commu in commus:
            if commu.recherche_abonnement(request.user):
                posts_precedents = tous_les_posts
                posts_commu = Post.objects.filter(communaute=commu)
                tous_les_posts = posts_precedents | posts_commu

        tous_les_posts = tous_les_posts.order_by('-date')
        return render(request, 'Fil_actu.html', locals())

    else:
        return redirect('login')

def like(request, id_du_post):
    post = Post.objects.get(id=id_du_post)
    post.likes.add(request.user)
    return redirect('afficher_post', id_du_post=post.id)


def unlike(request, id_du_post):
    post = Post.objects.get(id=id_du_post)
    post.likes.remove(request.user)
    return redirect('afficher_post', id_du_post=post.id)

def Filtrage_Priorite(request):
    form = FormulaireFiltrage(request.POST or None)
    if form.is_valid():
        Priorite = form.cleaned_data['priorite']
        commus = Communaute.objects.all()

        tous_les_posts = Post.objects.none()

        posts_aime = []
        posts_vus = []
        posts_ecarlates = []
        posts_rouges = []
        posts_oranges = []
        posts_jaunes = []
        all_posts = Post.objects.all()
        for post in all_posts:
            prio = post.priorite
            if post.recherche_vue(request.user):
                posts_vus.append(post)
            if post.recherche_like(request.user):
                posts_aime.append(post)
            if prio.label == 'Ecarlate':
                posts_ecarlates.append(post)
            if prio.label == 'Rouge':
                posts_rouges.append(post)
            if prio.label == 'Orange':
                posts_oranges.append(post)
            if prio.label == 'Jaune':
                posts_jaunes.append(post)

        for commu in commus:
            if commu.recherche_abonnement(request.user):
                if Priorite.label == 'Ecarlate':
                    posts_precedents = tous_les_posts
                    posts_commu = Post.objects.filter(communaute=commu).filter(priorite=Priorite)
                    tous_les_posts = posts_precedents | posts_commu
                elif Priorite.label =='Rouge':
                    posts_precedents = tous_les_posts
                    posts_commu = Post.objects.filter(communaute=commu).filter(priorite=Priorite)
                    tous_les_posts = posts_precedents | posts_commu
                    posts_precedents = tous_les_posts
                    prio2 = priorite.objects.get(label='Ecarlate')
                    posts_commu = Post.objects.filter(communaute=commu).filter(priorite=prio2)
                    tous_les_posts = posts_precedents | posts_commu
                elif Priorite.label == 'Orange':
                    posts_precedents = tous_les_posts
                    posts_commu = Post.objects.filter(communaute=commu).filter(priorite=Priorite)
                    tous_les_posts = posts_precedents | posts_commu
                    posts_precedents = tous_les_posts
                    prio2 = priorite.objects.get(label='Ecarlate')
                    posts_commu = Post.objects.filter(communaute=commu).filter(priorite=prio2)
                    tous_les_posts = posts_precedents | posts_commu
                    posts_precedents = tous_les_posts
                    prio2 = priorite.objects.get(label='Rouge')
                    posts_commu = Post.objects.filter(communaute=commu).filter(priorite=prio2)
                    tous_les_posts = posts_precedents | posts_commu
                elif Priorite.label =='Jaune':
                    posts_precedents = tous_les_posts
                    posts_commu = Post.objects.filter(communaute=commu).filter(priorite=Priorite)
                    tous_les_posts = posts_precedents | posts_commu
                    posts_precedents = tous_les_posts
                    prio2 = priorite.objects.get(label='Ecarlate')
                    posts_commu = Post.objects.filter(communaute=commu).filter(priorite=prio2)
                    tous_les_posts = posts_precedents | posts_commu
                    posts_precedents = tous_les_posts
                    prio2 = priorite.objects.get(label='Rouge')
                    posts_commu = Post.objects.filter(communaute=commu).filter(priorite=prio2)
                    tous_les_posts = posts_precedents | posts_commu
                    posts_precedents = tous_les_posts
                    prio2 = priorite.objects.get(label='Orange')
                    posts_commu = Post.objects.filter(communaute=commu).filter(priorite=prio2)
                    tous_les_posts = posts_precedents | posts_commu
                else:
                    posts_precedents = tous_les_posts
                    posts_commu = Post.objects.filter(communaute=commu)
                    tous_les_posts = posts_precedents | posts_commu
        tous_les_posts = tous_les_posts.order_by('-date')
        return render(request, 'Fil_actu.html', locals())
    return render(request, 'filtrage_priorite.html', locals())

def Filtrage_Priorite_Communaute(request):
    form = FormulaireFiltrageCommu(request.POST or None)
    if form.is_valid():
        Priorite = form.cleaned_data['priorite']
        Communaute_Choisie = form.cleaned_data['communaute']

        tous_les_posts = Post.objects.none()
        posts_ecarlates = []
        posts_rouges = []
        posts_oranges = []
        posts_jaunes = []
        posts_aime = []
        posts_vus = []
        all_posts = Post.objects.all()
        for post in all_posts:
            prio = post.priorite
            if post.recherche_vue(request.user):
                posts_vus.append(post)
            if post.recherche_like(request.user):
                posts_aime.append(post)
            if prio.label == 'Ecarlate':
                posts_ecarlates.append(post)
            if prio.label == 'Rouge':
                posts_rouges.append(post)
            if prio.label == 'Orange':
                posts_oranges.append(post)
            if prio.label == 'Jaune':
                posts_jaunes.append(post)


        if Priorite.label == 'Ecarlate':
            posts_precedents = tous_les_posts
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie).filter(priorite=Priorite)
            tous_les_posts = posts_precedents | posts_commu
        elif Priorite.label =='Rouge':
            posts_precedents = tous_les_posts
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie).filter(priorite=Priorite)
            tous_les_posts = posts_precedents | posts_commu
            posts_precedents = tous_les_posts
            prio2 = priorite.objects.get(label='Ecarlate')
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie).filter(priorite=prio2)
            tous_les_posts = posts_precedents | posts_commu
        elif Priorite.label == 'Orange':
            posts_precedents = tous_les_posts
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie).filter(priorite=Priorite)
            tous_les_posts = posts_precedents | posts_commu
            posts_precedents = tous_les_posts
            prio2 = priorite.objects.get(label='Ecarlate')
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie).filter(priorite=prio2)
            tous_les_posts = posts_precedents | posts_commu
            posts_precedents = tous_les_posts
            prio2 = priorite.objects.get(label='Rouge')
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie).filter(priorite=prio2)
            tous_les_posts = posts_precedents | posts_commu
        elif Priorite.label =='Jaune':
            posts_precedents = tous_les_posts
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie).filter(priorite=Priorite)
            tous_les_posts = posts_precedents | posts_commu
            posts_precedents = tous_les_posts
            prio2 = priorite.objects.get(label='Ecarlate')
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie).filter(priorite=prio2)
            tous_les_posts = posts_precedents | posts_commu
            posts_precedents = tous_les_posts
            prio2 = priorite.objects.get(label='Rouge')
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie).filter(priorite=prio2)
            tous_les_posts = posts_precedents | posts_commu
            posts_precedents = tous_les_posts
            prio2 = priorite.objects.get(label='Orange')
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie).filter(priorite=prio2)
            tous_les_posts = posts_precedents | posts_commu
        else:
            posts_precedents = tous_les_posts
            posts_commu = Post.objects.filter(communaute=Communaute_Choisie)
            tous_les_posts = posts_precedents | posts_commu
        tous_les_posts = tous_les_posts.order_by('-date')
        return render(request, 'Fil_actu.html', locals())
    return render(request, 'filtrage_priorite_communaute.html', locals())