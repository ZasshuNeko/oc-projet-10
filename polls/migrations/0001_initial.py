# -*- coding: utf-8 -*-
# Generated by Django 3.0.6 on 2020-05-25 06:46

import django.db.models.deletion
from django.db import migrations, models, connection, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

import requests
import json
import io
import os
import unicodedata


def maj_bdd(apps, schema_editor):
    x = 0
    while x < 1:
        x += 1
        url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        playload = {
            'action': 'process',
            'sort_by': 'unique_scan_n',
            'page_size': '130',
            'page' : x,
            'json': 'true'
        }
        headers = {}
        reponse = requests.get(url, params=playload)
        f = reponse.json()


        Produits = apps.get_model('polls', 'Produits')
        Vendeurs = apps.get_model('polls', 'Vendeurs')
        Nutriments = apps.get_model('polls', 'Nutriments')
        Categorie = apps.get_model('polls', 'Categories')

        with open('test.json','w') as fp:
            json.dump(f,fp,indent=4,separators=(',',':'))
        for item in f['products']:
            # Vérification si nom francais est vide
            name_fr = item.get("product_name")
            test_produit = Produits.objects.filter(
            generic_name_fr__exact=name_fr)
            if not test_produit.exists():
                if name_fr:
                    #insertion du produit
                    liste_nutriment = item.get("nutriments")
                    ingredient_text = item.get("ingredients_text_fr")
                    ingredient_second = item.get("ingredients_text")

                    if not ingredient_text:
                        ingredient_text = 'Non fournis par Open Food Fact'

                    if ingredient_second:
                        nw_produit = Produits(
                            ingredient=item.get("ingredients_text"),
                            url_image_ingredients=item.get("image_ingredients_url"),
                            brands_tags=item.get("brands_tags"),
                            grade=liste_nutriment.get("nutrition-score-fr_100g"),
                            image_front_url=item.get("image_front_url"),
                            image_nutrition_url=item.get("image_nutrition_url"),
                            nova_groups=item.get("quantity"),
                            generic_name_fr=item.get("product_name"),
                            url_site=item.get("url"),
                            ingredients_text_fr=ingredient_text,
                            _id=item.get("_id"))
                        # récupération des catégories
                        categories=item.get("categories")
                        print(x,"+++++", categories)
                        if categories:
                            if categories.find(':') == -1:
                                nw_produit.save()
                                liste_categories = categories.split(',')
                                # On vérifie si les catégories existe
                                for categorie in liste_categories:
                                    categorie = categorie.strip()
                                    try:
                                        object_cat = Categorie.objects.get(
                                            nom__exact=categorie)
                                        object_cat.save()
                                        id_cat = object_cat.id
                                        try:
                                            object_cat.produit.add(nw_produit)
                                        except:
                                            print("doublon")
                                    except Categorie.DoesNotExist:
                                        no_accent = "".join((c for c in unicodedata.normalize(
                                        'NFD', categorie) if unicodedata.category(c) != 'Mn'))
                                        nw_categorie = Categorie.objects.create(nom=categorie, nom_iaccents=no_accent)
                                        nw_categorie.save()
                                        id_cat = nw_categorie.id
                                        try:
                                            nw_categorie.produit.add(nw_produit)
                                        except:
                                            print('Doublon 2')
                                liste_store = item.get("stores_tags")
                                if liste_store:
                                    for stores in item.get("stores_tags"):
                                        Vendeurs.objects.create(
                                            produits=nw_produit, nom=stores)

                                for cle, valeur in liste_nutriment.items():
                                    unit = ""
                                    val_100 = 0
                                    label = ""
                                    if cle.find("_label") == -1:
                                        if cle.find("_unit") != -1:
                                            unit = liste_nutriment.get(cle)
                                            label = cle.split('_')
                                            label = label[0]
                                        elif cle.find("_100g") != -1:
                                            val_100 = liste_nutriment.get(cle)
                                            label = cle.split('_')
                                            label = label[0]

                                        if len(unit) != 0 or len(str(val_100)) != 0:
                                            Nutriments.objects.create(
                                                produits=nw_produit, nom=label, unite=unit, valeur=val_100)
                                            unit = ""
                                            val_100 = 0


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Produits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.CharField(max_length=5024, null=True)),
                ('url_image_ingredients', models.URLField(max_length=5024, null=True)),
                ('brands_tags', models.CharField(max_length=500)),
                ('grade', models.CharField(max_length=500, blank=True, null=True)),
                ('image_front_url', models.URLField(max_length=5024, null=True)),
                ('image_nutrition_url', models.URLField(max_length=5024, null=True)),
                ('nova_groups', models.CharField(max_length=500, null=True)),
                ('generic_name_fr', models.CharField(max_length=500)),
                ('url_site', models.URLField(max_length=5024)),
                ('ingredients_text_fr', models.CharField(max_length=5024)),
                ('_id', models.FloatField()),

            ],
            options={
                'db_table': 'polls_produits',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=5024)),
                ('nom_iaccents', models.CharField(max_length=5024)),
                ('produit', models.ManyToManyField('Produits')),

            ],
            options={
                'db_table': 'polls_categories',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Vendeurs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produits', models.ForeignKey('Produits', on_delete=models.CASCADE)),
                ('nom', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'polls_vendeurs',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Nutriments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produits', models.ForeignKey('Produits', on_delete=models.CASCADE)),
                ('nom', models.CharField(max_length=5000)),
                ('unite', models.CharField(max_length=10)),
                ('valeur', models.FloatField())
            ],
            options={
                'db_table': 'polls_nutriments',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Favoris',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('produits', models.ForeignKey('Produits', on_delete=models.CASCADE)),
                ('date_ajout', models.DateField(auto_now_add=True)),
                ('aff_index', models.BooleanField()),
            ],
            options={
                'db_table': 'polls_favoris',
                'managed': True,
            },
        ),
        migrations.RunPython(maj_bdd),
    ]

