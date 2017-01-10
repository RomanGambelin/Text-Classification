# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 10:36:08 2016

"""

"dicotexte = dictionnaire avec les textes sous forme de liste"
"dd = double dictionnaire qui à chaque mot de chaque texte lui associe sa fréquence dans le texte"
"dc = dictionnaire qui associe à chaque mot sa fréquence dans le corpus"
"dn = dictionnaire qui associe à chaque mot le nombre de texte dans lequel il apparait"
"dicoTFIDF = double dictionnaire qui associe à chaque mot dans chaque texte sa valeur TF-IDF associée"
"nbt = nombre de texte"
"nbMotsCorpus = le nom est assez clair pour celui là ... :D"
"dg = dictionnaire qui associe à chaque texte son groupe"
"dgt = dictionnaire qui associe à chaque groupe la liste de textes qu'il contient"
"dv = dictionnaire qui associe à chaque texte le vecteur de fréquence des mots pertinents dans le texte"
"fg = dictionnaire qui associe à chaque groupe la liste des n mots les plus fréquents dans le groupe"

"Ce qui est nécessaire d'importer pour le projet"
"Permet de charger les textes avec glob.glob(chemin/*)"
import glob
from math import log
from math import sqrt
"Permet d'utiliser sorted mais on utilise une autre méthode de tri dans la fonction fctpertience"
from operator import itemgetter
from random import randint
"Nous permet de tester la rapidité entre deux fonctions pour optimiser avec time.clock()"
import time

"PARTIE 1"

"Importer les textes"
## Please enter the path of the folder containing the texts folder "20_newsgroups"
Folder='C:\\Users\\Isa\Desktop\\Projects\\Text-Classification\\'
"A l'aide de glob que l'on a importé on récupère le chemin de chacun des textes, on lui précise le chemin du dossier source (/*/* permet d'ouvrir les sous dossiers)"
lpostexte=glob.glob(Folder+'20_newsgroups\\*\\*')
dicotexte={}
i=1
"On lit tous les textes que l'on sauvegarde dans un dictionnaire"
for pos in lpostexte:
    texte=open(pos)
    dicotexte[i]=texte.read()
    texte.close()
    i=i+1

"Création d'un ensemble m de mots récurrents en anglais (donc des mots non pertinents)"
m=["first","second","one","two","some","out","about","over","must","really","being","through","last","got","want","those","very","much","any","along","whole","each","just","into","among","how","many","least","likely","ever","did","other","just","its","did","then","you","she","they","mine","your","yours","him","her","his","our","ours","their","theirs","for","and","nor","but","yet","when","soon","since","before","after","till","until","while","if","unless","because","though","also","although","whereas","above","behind","here","there","afterwards","already","eventually","now","once","soon","still","weekly","today","always","never","occasionally","rarely","seldom","usually","often","else","enough","even","fairly","hardly","scarcely","barely","somewhat","too","actually","anyway","besides","firstly","secondly","further","furthermore","moreover","somehow","therefore","thus","same","however","nevertheless","otherwise","near","next","behind","between","under","that","this","these","the","which","was","are","can","could","will","would","should","may","might","have","has","does","don","doesn","more","less","lot","what","why","where","who","whose","not","from","off","outside","than","such","like","with","without","rather","most","both","get","all","none","only","been","had","many","lot","were"]
mc=set(m)
    
"Fonction noramisant les textes en liste de mots"
def normaliser(texte):
    "Mise en caractères minuscules du texte"
    texte=texte.lower()
    "Création de la liste qui a contenir tous les mots du textes"
    ltexte=[]
    "Création du liste locale qui va servir à composer chaque mot"
    l=[]
    "a devient vrai dès lors qu'on décide de ne pas compter une chaîne de caractère (on considère que celle-ci est délimitée par espaces)"
    a=False
    "pt est vrai lorsque le dernière caractère regardé est un point ."
    pt=False
    "t est vrai lorsque le dernier caractère regardé est un tiret -"
    t=False
    "Pour chaque caractère i dans le texte"
    for i in texte:
        "cas où le caractère précédent était un tiret"
        if t:
            "si le caractère suivant est une lettre on l'ajoute à l"
            if (i >="a" and i<="z"):
                l.append(i)
            else:
                "sinon l est réinitialisé (on passe au mot suivant et on ne compte pas la chaîne de carractère précédente)"
                l=[]
            t=False
            "cas où le caractère précédent est un point"
        elif pt:
            "si le caractère suivant est un espace"
            if i==" ":
                "si le mot contient plus de deux lettres et qu'il n'est pas dans mc on ajoute le mot à ltexte et on réinitialise l"
                if len(l)>2:
                    mot="".join(l)
                    if mot not in mc:
                        ltexte.append(mot)
                l=[]
            else:
                "sinon a devient vrai et on décide de ne pas compter la chaîne de carractère associée au point"
                a=True
                pt=False
        elif (not a):
            "cas où a n'est pas vrai"
            "si i est une lettre alors on ajoute i à l"
            if (i >="a" and i<="z"):
                l.append(i)
            elif i=="-":
                "sinon si i est un tiret on ajoute i à l et t devient vrai"
                t=True
                l.append(i)
            elif (i!="." and i!=":"):
                "sinon si i est un caractère différent d'un . ou : on ajoute le mot avec les mêmes conditions qu'au dessus et on réinitialise l"
                if len(l)>2:
                    mot="".join(l)
                    if mot not in mc:
                        ltexte.append(mot)
                l=[]
            elif (i==":"):
                "sinon si i est un : a devient vrai et on ne compte plus la chaîne de caractères associés (jusqu'au prochain espace)"
                a=True
            else:
                "sinon si i est un . pt devient vrai"
                pt=True
        elif (i==" "):
            "si a est vrai et que i est un espace, a devient faux et on passe au mot suivant (on on réinitialise l), si i est différent d'un espace rien ne se passe"
            a=False
            l=[]
    return(ltexte)

for i in dicotexte.keys():
    dicotexte[i]=normaliser(dicotexte[i])

"Nombre de mot dans le corpus"
nbMotCorpus=0
for x in dicotexte.values():
    nbMotCorpus=nbMotCorpus+len(x)
    
"Nombre de texte"
nbt=len(dicotexte)

"Calcule la fréquence des mots dans chaque texte"
def frequencetxt():
    "Création du dictionnaire qui associe à chaque texte un dictionnaire reliant les mots du texte à leur fréquence"
    d={}
    "Pour chaque texte i on initialise d[i]"
    for i in dicotexte.keys():
        d[i]={}
    for k,v in d.items():
        "pour chaque texte k et dictionnaire v associé on attribue à n la longueur du texte k"
        n=len(dicotexte[k])
        "pour chaque mot du texte on somme le nombre de fois où il apparaît, pondéré par n"
        for mot in dicotexte[k]:
            if mot not in v:
                v[mot]=1.0/n
            else:
                v[mot]=v[mot]+1.0/n
    return(d)

dd=frequencetxt()

"Le nombre de textes dans lequel apparaît chaque mot du corpus"
def occurenceCorp1():
    "Création du dictionnaire qui associe à chaque mot le nombre de textes dans lequel il apparaît"
    dnc={}
    "Pour chaque dictionnaire v associé à un texte"
    for v in dd.values():
        "Pour chaque mot m dans v"
        for m in v.keys():
            "La valeur de m dans dnc prend +1 (le mot apparaît dans un texte supplémentaire)"
            if m in dnc:
                dnc[m]=dnc[m]+1
            else:
                dnc[m]=1
    return dnc
    
dn=occurenceCorp1()

"Calcule la fréquence des mots dans le corpus (mais on ne l'utilise pas)"
def frequenceCorpusDico():
    "Création du dictionnaire qui associe à chaque mot sa fréquence dans le corpus"
    dc={}
    "Pour chaque mot du corpus"
    for k,v in dd.items():
        "n prend la valeur de la longueur du texte k"
        n=len(dicotexte[k])
        "Pour chaque mot apparaissant dans le texte k"
        for mot in v.keys():
            "On ajoute sa fréquence dans le texte multipliée par n et divisée par le nombre de mots dans le corpus"
            if mot not in dc:
               dc[mot]=(float(v[mot])*n)/nbMotCorpus
            else:
                dc[mot]=dc[mot]+(float(v[mot])*n)/nbMotCorpus
    return dc

dc=frequenceCorpusDico()

"PARTIE 2"

"Dictionnaire qui associe à chaque mot le TF-IDF correspondant"
def TF_IDF():
    di={}
    "on itère dans le dictionnaire qui a les fréquences, k étant le numéro du texte"
    for k,v in dd.items():
        di[k]={}
        "on itère ensuite dans v, un dictionnaire qui contient les mots du texte k auquel on a associé une fréquence f"
        for m,f in v.items():
            "on met en place certaines conditions supplémentaires"
            if (dn[m]>250) and (dn[m]<5000):
                di[k][m]=f*log(nbt/dn[m])
    return di

dicoTFIDF=TF_IDF()


"Déterminer les n mots les plus pertinents"
def fctpertinence(n,dicoTF_IDF):
    mpert=[("",0)]*n
    "On itère sur les mots dans chacun des textes"
    for t,v in dicoTF_IDF.items():
        for m in v.keys():
            "Si leur TF-IDF est supérieur au premier de la liste des mots pertinents on va le remplacer"
            if dicoTF_IDF[t][m]>mpert[0][1] :
                "On vérifie juste si le mot est déjà dans la liste (pour ne pas l'avoir en double, si jamais son TF-IDF est plus grand que celui sauvegardé, on le remplace également)"
                if m in [mot for (mot,freq) in mpert]:
                    pos=[mot for (mot,freq) in mpert].index(m)
                    if dicoTF_IDF[t][m]>mpert[pos][1]:
                        mpert[pos]=(m,dicoTF_IDF[t][m])
                else:
                    mpert[0]=(m,dicoTF_IDF[t][m])
                    "On trie la liste pour avoir le mot avec le plus petit TF-IDF en premier"
                    i=0
                    while i<(n-1) and mpert[i][1]>mpert[i+1][1]:
                        tmp=mpert[i]
                        mpert[i]=mpert[i+1]
                        mpert[i+1]=tmp
                        i=i+1
    return [mot for (mot,freq) in mpert]

mp=fctpertinence(100,dicoTFIDF)
    
"Création du dictionnaire qui associe à chaque texte le vecteur de fréquence des mots pertinents dans le texte"
def dicovecteur(motspert):
    dv={}
    n=len(motspert)
    for k,v in dd.items():
        dv[k]=[0]*n
        cpt=0
        for m in motspert:
            if m in v:
                dv[k][cpt]=v[m]
            cpt=cpt+1
    return dv

dv=dicovecteur(mp)


"Calcule la distance entre deux vecteurs"
"Fonction qui prend en argument pour les deux textes le vecteur de fréquence des mots pertinents"
def distanceCosinus(vecteurA,vecteurB):
    produitscalaire=0
    normeA=0
    normeB=0
    "Les vecteurs A et B ont la même taille n"
    for i in range(len(vecteurA)):
        produitscalaire=produitscalaire+vecteurA[i]*vecteurB[i]
        normeA=normeA+vecteurA[i]**2
        normeB=normeB+vecteurB[i]**2
    normeA=sqrt(normeA)
    normeB=sqrt(normeB)
    if produitscalaire!=0:
        return produitscalaire/(normeA*normeB)
        "Permet d'éviter l'erreur de division par zéro"
    else:
        return 0

"PARTIE 3"
   
"Fonction kmeans pour k groupes et n mots pertinents"
def kmeans(k,n):
    'Création de la liste des n mots pertinents du corpus'
    motspert=fctpertinence(n,dicoTFIDF)
    'Création du dictionnaire reliant chaque texte à son vecteur de fréquences des n mots pertinents'
    dv=dicovecteur(motspert)
    'Création de cm = liste des centres mobiles'
    cm=[] 
    'Création de dg = dictionnaire associant à chaque texte son groupe'
    dg={}
    "Création de dgt = dictionnaire associant à chaque groupe la liste de textes qu'il contient"
    dgt={}
    "Création du booléen B, faux de base, il devient vrai à chaque début d'itération et devient faux dès qu'un texte change de groupe"
    B=False
    "Boucle d'initialisation de cm et dgt"
    "Opération répétée k fois pour les k groupes demandés (et donc les k centres mobiles)"
    for i in range(k):
        "Choix aléatoire d'un texte parmis le nombre total de textes (nbt) comme centre mobile initial"
        a=randint(1,nbt)
        "Boucle pour s'assurer qu'on ne prend pas deux fois le même texte (tt que le vecteur associé au texte a est déjà dans cm on retire un nouveau a)"
        while dv[a] in cm:
            a=randint(1,nbt)
        "Ajout du vecteur associé au texte à la liste des centres mobiles"
        cm.append(dv[a])
        "Initialisation du groupe i"
        dgt[i]=[]
    "Initialisation du nombre d'itérations pour kmeans"
    nbit=0
    "Initialisation de dg : association de la valeur -1, qui ne correspond à aucun groupe, à chaque texte"
    for i in dv.keys():
        dg[i]=-1
    "Boucle méthode des k means"
    "Tourne tant que B est faux ou que le nombre d'itération est inférieur à 5"
    while B==False and nbit<5:
        "B devient vrai au début de chaque itération, de sorte que si aucun texte ne change de groupe, la boucle s'arrête"
        B=True
        "Boucle de tri des textes (association d'un groupe à chaque texte)"
        for t,v in dv.items():
            "On initialise la plus petite distance cosinus entre le texte et les centres mobiles égale à -1 (qui est la plus grand distance possible)"
            d=-1
            "Initialisation de l'indice des centres (et donc des groupes)"
            ic=0 
            "Comparaison des distances entre le vecteur du texte v et chaque centre mobile c"
            for c in cm:
                "dist prend la valeur de la distance cosinus entre v et c"
                dist=distanceCosinus(v,c)
                "si la distance calculée est plus petite (supérieure en valeure réelle dans le cas de la distance cosinus) à la plus petite distance déjà calculée pour ce texte"
                if dist>=d:
                    "alors la plus petite distance calculée pour le texte devient la dernière distance calculée"
                    d=dist
                    "si le groupe associé à t est différent du groupe associé au centre mobile"
                    if dg[t]!=ic:
                        "alors B devient faux"
                        B=False
                        "et on associe le texte au groupe du centre mobile"
                        dg[t]=ic
                "Indice du centre mobile prend +1, on regarde le centre mobile suivant"
                ic=ic+1
            "Ajout du texte à la liste associée à son groupe dans dgt"
            dgt[dg[t]].append(t)
        "Réinitialisation des centre mobiles en liste vide"
        cm=[]
        "Le nombre d'itération prend +1"
        nbit=nbit+1
        "Boucle de calcul des moyennes et redéfinition des centres mobiles"
        "Si B est faux (un texte a précedement changé de groupe) et que le nombre d'itération n'a pas atteint son maximum"
        if B==False and nbit<5:
            "Pour chaque liste de texte lt associée à un groupe g dans dgt"
            for g,lt in dgt.items():
                "Calcul de la taille du groupe tg"
                tg=len(lt)
                "Création d'une liste eachg qui va qui va contenir les coordonnées moyennes d'un groupe"
                eachg=[]
                "Boucle associant les coordonnées moyennes d'un groupe à eachg"
                "Opération répétée n fois (pour les n mots pertinents et donc les n coordonnées du vecteur)"
                for i in range(n):
                    "Initialisation de la valeur de la coordonnée moyenne i"
                    valeur=0
                    "Pour chaque texte t du groupe"
                    for t in lt:
                        "la valeur de la coordonnée i du texte t pondérée par la taille du groupe s'ajoute à la valeur moyenne"
                        valeur=valeur+float(dv[t][i])/tg
                    "ajout de la coordonnée moyenne au vecteur de coordonnées moyennes eachg"
                    eachg.append(valeur)
                "ajout de eachg aux centres mobiles"
                cm=cm+[eachg]
                "réinitialisation de la liste du group g"
                dgt[g]=[]
        "affiche le numéro de l'itération effectuée"
        print(nbit)
    "retourne un tuple contenant dg et dgt"
    return  (dg,dgt)

(dg,dgt)=kmeans(20,500)

"Fonction annexe pour avoir des infos sur l'efficacité"
"La première calcule le nombre de vecteur = 0"
"La deuxième donne la taille des groupes, le nombre de texte qu ils contiennent"
def nbrvec0 (n):
    cmpt=0
    vectnul=[0]*n
    motspert=fctpertinence(n,dicoTFIDF)
    dv=dicovecteur(motspert)
    for t,vect in dv.items():
        if vect==vectnul:
            cmpt=cmpt+1
    return(cmpt)

def taillegr ():
    res={}
    for gr in dg.values():
        if gr in res:
            res[gr]=res[gr]+1
        else:
            res[gr]=1
    return res

"Pour chaque groupe de textes donner les m mots les plus fréquents du centre du groupe"  
"Fonction qui revoie un dictionnaire associant à chaque groupe la liste de ses n mots les plus pertinents"
def frequenceGroupe(dgt,n):
    "Création d'un dictionnaire associant à chaque groupe un dictionnaire qui associe à chaque mot du groupe sa fréquence dans le groupe"
    dfg={}
    "Création d'un dictionnaire associant à chaque groupe une liste des n mots les plus fréquents dans le groupe"
    fg={}
    "Création d'un dictionnaire associant à chaque texte sa taille"
    ltt={}
    "Création d'un dictionnaire associant à chaque groupe sa taille"
    ltg={}
    "Boucle calculant la taille des groupes et donnant des valeurs à ltt et ltg"
    for g,lt in dgt.items():
        "Initialisation de fg en une liste de n chaines de carractères vides"
        fg[g]=[""]*n
        "Initialisation de dfg ltg et fg"
        dfg[g]={}
        ltg[g]=0
        "Ajoute la taille de chaque texte à la taille totale du groupe auquel il appartient"
        for t in lt:
            ltt[t]=len(dicotexte[t])
            ltg[g]=ltg[g]+ltt[t]
    "Boucle calculant la fréquence de chaque mot d'un groupe dans son groupe"
    "Pour chaque groupe g et liste de textes lt dans dgt"
    for g,lt in dgt.items():
        "Pour chaque texte t dans lt"
        for t in lt:
            "Pour chaque mot m et fréquence associée f dans t"
            for m,f in dd[t].items():
                "Ajout de sa fréquence pondérée à sa fréquence totale dans le texte"
                if m not in dfg[g]:
                    dfg[g][m]=f*float(ltt[t])/ltg[g]
                else:
                    dfg[g][m]=dfg[g][m]+f*float(ltt[t])/ltg[g]
    "Boucle déterminant les n mots les plus fréquents dans chaque texte (donnant des valeurs à fg)"
    "Pour chaque groupe et dictionnaire de fréquences de mots associé dans dfg"
    for g,dfm in dfg.items():
        "Création et initialisation d'une liste contenant les fréquences associées à fg"
        lf=[0]*n
        "Pour chaque mot et fréquence associée dans dfm"
        for m,f in dfm.items():
            "Ajout d'un mot à fg[g] si sa fréquence est supérieure à la fréquence minimale des mots contenus dans fg[g]"
            if f>lf[0]:
                lf[0]=f
                fg[g][0]=m
                i=0
                "Tri par décalage (la liste étant déjà triée à chaque itération)"
                while i<(n-1) and f>lf[i+1]:
                    tmp=lf[i+1]
                    lf[i+1]=f
                    lf[i]=tmp
                    tmp=fg[g][i+1]
                    fg[g][i+1]=m
                    fg[g][i]=tmp
                    i=i+1
    return fg
    
fg=frequenceGroupe(dgt,20)
                
                
                    
                    
                
            
            
                
                
    
    
    
    
    
    
    
    
    
    
    
    

