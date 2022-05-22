from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os
from django.conf import settings

import numpy as np
import pandas as pd #parcequ'on est pas des PD nous
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import plot, iplot, init_notebook_mode
import json
import geojson
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from urllib.request import urlopen
from datetime import datetime
import statistics

#Fonctions

#variables utiles pour la suite

REGIONS = {
    'Auvergne-Rhône-Alpes': ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74'],
    'Bourgogne-Franche-Comté': ['21', '25', '39', '58', '70', '71', '89', '90'],
    'Bretagne': ['35', '22', '56', '29'],
    'Centre-Val de Loire': ['18', '28', '36', '37', '41', '45'],
    'Corse': ['2A', '2B'],
    'Grand Est': ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88'],
    'Guadeloupe': ['971'],
    'Guyane': ['973'],
    'Hauts-de-France': ['02', '59', '60', '62', '80'],
    'Île-de-France': ['75', '77', '78', '91', '92', '93', '94', '95'],
    'La Réunion': ['974'],
    'Martinique': ['972'],
    'Normandie': ['14', '27', '50', '61', '76'],
    'Nouvelle-Aquitaine': ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87'],
    'Occitanie': ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82'],
    'Pays de la Loire': ['44', '49', '53', '72', '85'],
    'Provence-Alpes-Côte d\'Azur': ['04', '05', '06', '13', '83', '84'],
}

DEPARTMENTS = {
    '01': 'Ain', 
    '02': 'Aisne', 
    '03': 'Allier', 
    '04': 'Alpes-de-Haute-Provence', 
    '05': 'Hautes-Alpes',
    '06': 'Alpes-Maritimes', 
    '07': 'Ardèche', 
    '08': 'Ardennes', 
    '09': 'Ariège', 
    '10': 'Aube', 
    '11': 'Aude',
    '12': 'Aveyron', 
    '13': 'Bouches-du-Rhône', 
    '14': 'Calvados', 
    '15': 'Cantal', 
    '16': 'Charente',
    '17': 'Charente-Maritime', 
    '18': 'Cher', 
    '19': 'Corrèze', 
    '2A': 'Corse-du-Sud', 
    '2B': 'Haute-Corse',
    '21': 'Côte-d\'Or', 
    '22': 'Côtes-d\'Armor', 
    '23': 'Creuse', 
    '24': 'Dordogne', 
    '25': 'Doubs', 
    '26': 'Drôme',
    '27': 'Eure', 
    '28': 'Eure-et-Loir', 
    '29': 'Finistère', 
    '30': 'Gard', 
    '31': 'Haute-Garonne', 
    '32': 'Gers',
    '33': 'Gironde', 
    '34': 'Hérault', 
    '35': 'Ille-et-Vilaine', 
    '36': 'Indre', 
    '37': 'Indre-et-Loire',
    '38': 'Isère', 
    '39': 'Jura', 
    '40': 'Landes', 
    '41': 'Loir-et-Cher', 
    '42': 'Loire', 
    '43': 'Haute-Loire',
    '44': 'Loire-Atlantique', 
    '45': 'Loiret', 
    '46': 'Lot', 
    '47': 'Lot-et-Garonne', 
    '48': 'Lozère',
    '49': 'Maine-et-Loire', 
    '50': 'Manche', 
    '51': 'Marne', 
    '52': 'Haute-Marne', 
    '53': 'Mayenne',
    '54': 'Meurthe-et-Moselle', 
    '55': 'Meuse', 
    '56': 'Morbihan', 
    '57': 'Moselle', 
    '58': 'Nièvre', 
    '59': 'Nord',
    '60': 'Oise', 
    '61': 'Orne', 
    '62': 'Pas-de-Calais', 
    '63': 'Puy-de-Dôme', 
    '64': 'Pyrénées-Atlantiques',
    '65': 'Hautes-Pyrénées', 
    '66': 'Pyrénées-Orientales', 
    '67': 'Bas-Rhin', 
    '68': 'Haut-Rhin', 
    '69': 'Rhône',
    '70': 'Haute-Saône', 
    '71': 'Saône-et-Loire', 
    '72': 'Sarthe', 
    '73': 'Savoie', 
    '74': 'Haute-Savoie',
    '75': 'Paris', 
    '76': 'Seine-Maritime', 
    '77': 'Seine-et-Marne', 
    '78': 'Yvelines', 
    '79': 'Deux-Sèvres',
    '80': 'Somme', 
    '81': 'Tarn', 
    '82': 'Tarn-et-Garonne', 
    '83': 'Var', 
    '84': 'Vaucluse', 
    '85': 'Vendée',
    '86': 'Vienne', 
    '87': 'Haute-Vienne', 
    '88': 'Vosges', 
    '89': 'Yonne', 
    '90': 'Territoire de Belfort',
    '91': 'Essonne', 
    '92': 'Hauts-de-Seine', 
    '93': 'Seine-Saint-Denis', 
    '94': 'Val-de-Marne', 
    '95': 'Val-d\'Oise',
    '971': 'Guadeloupe', 
    '972': 'Martinique', 
    '973': 'Guyane', 
    '974': 'La Réunion', 
    '976': 'Mayotte',
}

def ColonneVide(df):
    nunique = df.nunique()
    compteur = 0
    for i in df.columns:
        if nunique[compteur] == 0:
            del df[i]
        compteur += 1
    return df

def find_key(dico,v): 
    for k, val in dico.items(): 
        if v in val: 
            return k 

def addRegions(data):
    tab = []
    for i in data["Code departement"]:
        tab.append(find_key(REGIONS, i))
    data["Region"] = tab
    return data

def pm2(data):
    tab = []
    for i,k in data.iterrows():
        div = k["Surface terrain"] if k["Surface terrain"] != None else k["Surface reelle bati"]
        tab.append(k["Valeur fonciere"]/(div if div!=0 else 1))
    data["Prix au m²"] = tab
    return data

def addDate(data, year):
    data['Year'] = [year] * len(data.index)
    return data

#import de l'ensemble des données
df_2017 = pd.read_csv(os.path.join(settings.BASE_DIR, 'valeursfoncieres-2017.txt'), sep="|",low_memory=False,decimal=',')
df_2018 = pd.read_csv(os.path.join(settings.BASE_DIR, 'valeursfoncieres-2018.txt'), sep="|",low_memory=False,decimal=',')
df_2019 = pd.read_csv(os.path.join(settings.BASE_DIR, 'valeursfoncieres-2019.txt'), sep="|",low_memory=False,decimal=',')
df_2020 = pd.read_csv(os.path.join(settings.BASE_DIR, 'valeursfoncieres-2020.txt'), sep="|",low_memory=False,decimal=',')
df_2021 = pd.read_csv(os.path.join(settings.BASE_DIR, 'valeursfoncieres-2021.txt'), sep="|",low_memory=False,decimal=',')

df_2017 = ColonneVide(df_2017)
df_2018 = ColonneVide(df_2018)
df_2019 = ColonneVide(df_2019)
df_2020 = ColonneVide(df_2020)
df_2021 = ColonneVide(df_2021)

df_2017 = addRegions(df_2017)
df_2018 = addRegions(df_2018)
df_2019 = addRegions(df_2019)
df_2020 = addRegions(df_2020)
df_2021 = addRegions(df_2021)

df_2017 = pm2(df_2017)
df_2018 = pm2(df_2018)
df_2019 = pm2(df_2019)
df_2020 = pm2(df_2020)
df_2021 = pm2(df_2021)

df_2017 = addDate(df_2017,2017)
df_2018 = addDate(df_2018,2018)
df_2019 = addDate(df_2019,2019)
df_2020 = addDate(df_2020,2020)
df_2021 = addDate(df_2021,2021)

def plot_time_line_reg(col,region,title="",yaxis_title="", slide = False):
    
    
    # T2017 = df_2017.loc[df_2017["Region"] == region][col].sum()
    # T2018 = df_2018.loc[df_2018["Region"] == region][col].sum()
    # T2019 = df_2019.loc[df_2019["Region"] == region][col].sum()
    # T2020 = df_2020.loc[df_2020["Region"] == region][col].sum()
    # T2021 = df_2021.loc[df_2021["Region"] == region][col].sum()
    
    T2017 = df_2017.groupby('Region').mean()
    T2018 = df_2018.groupby('Region').mean()
    T2019 = df_2019.groupby('Region').mean()
    T2020 = df_2020.groupby('Region').mean()
    T2021 = df_2021.groupby('Region').mean()
    
    
    T2017 = T2017.loc[T2017.index == region]
    T2018 = T2018.loc[T2018.index == region]
    T2019 = T2019.loc[T2019.index == region]
    T2020 = T2020.loc[T2020.index == region]
    T2021 = T2021.loc[T2021.index == region]
    
    TAll = pd.concat([T2017,T2018,T2019,T2020,T2021])


    
    
    
    fig = px.line(TAll,x='Year', y=col ,width=700)
    fig.update_layout(title=(col if title=="" else title + " en " + region), xaxis_title="Annee", yaxis_title=yaxis_title)
    if(slide):
        fig.update_layout(xaxis_rangeslider_visible=True)
    
    return fig
# Create your views here.

def index(request):
    context = {}
    return render(request, 'ValFonc/index.html',context)

def visu(request):
    template = loader.get_template('ValFonc/Code.html')
    context = {}
    return HttpResponse(template.render(context, request))



def visuType(request):
    context = {
    }
    return render(request, 'ValFonc/visu.html', context)
def visuReg(request):
    visu_type = request.GET['visu_type']
    region = request.GET['region']
    context = {
        'fig' : plot_time_line_reg(visu_type, region, "Evolution de " + visu_type + " en " + region, visu_type),
        'visu_type' : visu_type,
        'region' : region,
    }
    return render(request, 'ValFonc/resulVisu.html', context)

