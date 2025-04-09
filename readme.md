	# THEME DU CHALLENGE INDABAX
---------------------------------------------------------------------------
	TABLEAU DE BORD DE LA CAMPAGNE DE DON DE SANG
---------------------------------------------------------------------------

#NOM DE L APPLICATION
---------------------------------------------------------------------------
	Nom de l équipe:TensorPulse
---------------------------------------------------------------------------
##AUTEURS

Ce challenge a été réalisé par:

MEFFO TAHAFO LEA JECY        		jecy.meffo@facsciences-uy1.cm
NANGMO FEULFACK DUPLESSE ANNICK		duplessenangmo17@gmail.com
MBAH-NDAM Pavel				mbpavel21@gmail.com
--------------------------------------------------------------------------
##INSTRUCTIONS D UTILISATION
##Via le lien 		[https://tensorpulse.pythonanywhere.com/prediction]
-------------------------------------------------------------------------- 
ou:
1. Décompressez le dossier du projet : `blood_donation_dashboard.zip`.  
2. Installez les bibliothèques nécessaires en exécutant :  
   
   pip install -r requirement.txt
   
3.Placez-vous dans le dossier blood_donation_dashboard et lancez l'application :
	python3 src/appp.py
4.    Une fois démarré, accédez au tableau de bord à partir de votre navigateur.


## DESCRIPTION

Dans le cadre de l'IndabaX Hackathon, notre objectif est de concevoir un tableau de bord innovant et interactif, entièrement développé en Python, dédié à la visualisation et à l'analyse des données liées aux campagnes de don de sang. Ce projet mettra en avant la richesse et le potentiel du jeu de données fourni, tout en proposant des solutions basées sur les données pour améliorer les stratégies des campagnes futures.

Le tableau de bord visera à répondre aux besoins critiques des organisateurs de campagnes, en leur fournissant des informations clés pour optimiser la prise de décisions. Grâce à cet outil, ils pourront identifier des tendances, comprendre les comportements des donneurs, et élaborer des modèles prédictifs pour maximiser les résultats des campagnes.

## TABLE DES MATIERES
1. Étapes du Nettoyage des Données  
2. Fonctionnalités du Tableau de Bord  
3. Outils Utilisés  
4. Instructions d'Utilisation  
5. Hypothèses Formulées  
6. Exécution et Interaction  
7. Explications sur l'API du Modèle de Prédiction  




## FONCTIONNALITÉS DU TABLEAU DE BORD
	Le tableau de bord inclut les fonctionnalités suivantes :  
	
- **Cartographie des Donneurs** : Visualisation géographique pour identifier les zones de participation.  
- **Analyse Santé et Éligibilité** : Impact des conditions médicales sur l'éligibilité au don.  
- **Edude du genre Feminin** : afin d'evaluer les vacteur influancant le don chez les femmmes.  
- **Analyse de l'Efficacité des Campagnes** : Identification des périodes favorables et des groupes actifs.  
- **Fidélisation des Donneurs** : Étude des facteurs favorisant les dons répétés.   
- **Modèle Prédictif d'Éligibilité** : Prédictions en temps réel via une API intégrée.  

## OUTILS UTILISÉS

**Analyse et Visualisation des Données :**  
- Pandas  
- Matplotlib  
- Plotly  
- Dash 
- Geopy  
- ydata_profiling(pour une analyse automatique des données)

**Machine Learning :**  
- Scikit-learn  
- Flask/FastAPI  

**Prototypage et Déploiement :**  
- Jupyter Notebooks  (pour l'analys exploratoire et le nettoyage des données)
- PythonAnywhere  (Pour le deployement du project)


## DESCRIPTION DES OUTILS UTILISÉS

Pour ce faire, 
	comme bibliotheques Python pour l'Analyse et la Visualisation des Données:
		●​ Pandas : Pour la manipulation et le nettoyage des données.
		●​ Matplotlib : Pour créer des visualisations statiques (ex. : graphiques à
		barres, courbes).
		●​ Plotly : Pour des visualisations interactives, y compris des cartes, des graphiques en
		barres et des nuages de points.
		●​ Dash  : Pour concevoir des applications web interactives en Python.
		●​ Geopy : Pour l’analyse géospatiale (cartographie des localisations des donneurs).
		●​ ydata_profiling : pour générer automatiquement un rapport détaillé avec des statistiques descriptives, des distributions et des corrélations
	
	Dans le domaine de machine learning:
		●Scikit-learn : Pour construire des modèles d’apprentissage automatique, Random Forest .
		●​ Flask / FastAPI : Pour créer une API REST autour du modèle de machine learning.
		
	Dans le domaine de visualisation et de cartographie:
		●​ Plotly : A également pris en charge la visualisation géographique avec des cartes choroplèthes.
		
	Comme autres outils on a:
		●js (pour la generation du pdf)
		●vscode (notre editeur de texte)
		●​ Jupyter Notebooks : Pour l’analyse exploratoire des données et le prototypage.
		●​  PythonAnywhere : Pour le déploiement du tableau de bord et de l’API 

## ETALAGES DES HYPOTHESES FAITES LORS DU DEVELOPPEMENT	

- Attribution des arrondissements manquants dans Douala grâce à *data labeling*.  
- Conversion des données en minuscules pour standardiser l’analyse.  
- Regroupement des religions en cinq catégories :  
   1. Chrétien  
   2. Laïc  
   3. Traditionnaliste  
   4. Musulman  
   5. Non précisé  
   6. multiple religiniste
   
- Gestion des cycles menstruels chez les femmes.  
- Correction des âges incohérents avec la moyenne.  

## Pourqyuoi un dash sur les femmes
apres analyse on a remarque que la fenetre qui permet a une femme de donner du sang est tres restreinte et on a decider de l'etudier afin de resotir 
les facteur influençant cela.  

	
## EXECUTION DU TABLEAU DE BORD ET INTERACTIONS AVEC LES VISUALISATIONS

 Après avoir lancé le projet, une interface s’ouvre dans le navigateur avec les éléments suivants :  
- **KPI en En-tête** : Taux de donneurs, pourcentage de femmes, âge moyen, arrondissement dominant, etc.  
- **Filtres Dynamiques** : Filtres par arrondissement, sexe, religion, variant selon les champs sélectionnés.  
- **Visualisations Cartographiques Interactives**.  

## EXPLICATIONS SUR L UTILISATION DE L API DU MODELE DE PREDICTIONS

L'API intégrée permet de prédire en temps réel l'éligibilité au don de sang. Elle a été conçue pour offrir une interaction simple et rapide entre les utilisateurs et le modèle de machine learning.  

### Fonctionnement  

1. **Entrées Acceptées**  
   L'API accepte plusieurs paramètres en entrée, notamment :  
   - Âge  
   - Genre  
   - Profession
   - Niveau d'etude
   - Situation matrimoniale
   - Profession
   - Nationalité
   - Religion
   - taux d'hemoglobie
   - et le fait de savoir si vous avez dejas fait un don
		**toutes sont abligatoire** 

2. **Traitement des Données**  
   Les données reçues par l'API sont transmises au modèle prédictif, qui utilise des algorithmes avancés pour analyser ces informations.  

3. **Résultats**  
   L'API retourne une prédiction indiquant si la personne est **éligible** ou **non éligible** ou **temporairement non elligible** au don de sang.  
   - **Éligible** : La personne satisfait aux critères requis.  
   - **Non Éligible** : La personne ne répond pas aux critères essentiels en raison de certaines contraintes (ex. : conditions médicales)...  

### Exemple d'Utilisation  

Pour utiliser l'API, il suffit d'envoyer une requête HTTP en suivant le format préétabli. Voici un exemple en Python :  


import requests

url = "http://localhost:5000/predict"
data = {
    "age": 30,
    "health_condition": "hypertension",
    "profession": "enseignant"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    prediction = response.json()
    print("Éligibilité au don de sang :", prediction["result"])
else:
    print("Erreur :", response.status_code)

###cas d utilisation

L'API aidera les organisateurs à identifier rapidement les donneurs potentiels, à mieux comprendre les profils des candidats et à adapter les futures campagnes en conséquence. Grâce à cette automatisation, les décisions critiques pourront être prises plus efficacement.
    







