from django import forms
from .models import Post, Commentaire, priorite


class Ecrire_Un_post(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titre','description','communaute','priorite','evenementiel','date_evenement')
        #fields = '__all__'

class FormulaireCom(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ('contenu',)

class FormulaireFiltrage(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('priorite',)

class FormulaireFiltrageCommu(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('priorite','communaute',)