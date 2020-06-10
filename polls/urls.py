from django.urls import path, re_path
from django.conf.urls import handler404

from . import views

urlpatterns = [
	path('',views.index, name='index'),
	re_path(r'^resultat/([0-9a-zA-Z]+)/',views.get_resultat, name='resultat'),
	path('r/resultat/',views.redirect_resultat, name='redirect_resultat'),
	path('favoris/',views.save_favoris, name='favoris'),
	re_path(r'^maj/index/([0-9]+)/',views.mise_index, name="maj_index"),
	re_path(r'^aliments/([0-9]+)/',views.get_aliment, name='get_aliment'),
	re_path(r'^save/([0-9]+)/',views.save, name='save'),

]

handler404 = views.redirect_404

#Faire un r_path pour déterminer si c'est un utilisateur demander une auth puis sur /polls/UTIL donner accès au compte
# sur polls/util/edit donner accès au formulaire d'édition du compte