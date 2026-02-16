Data Management, Data Visualisation & Text Mining
---
## ** Objectif du projet**
L’objectif principal est de créer une **application interactive** qui permet :  
- de présenter un dataset choisi,  
- de réaliser des **analyses descriptives**,  
- de générer des **visualisations interactives**,  
- et d’intégrer une **partie Text Mining** sur un article lié au thème du dataset.  

---

## ** Consignes principales**
1. **Présentation du dataset dans l’application** :  
   - Source et origine des données  
   - Nombre d’observations et de variables  
   - Types et signification des variables  
   - Nombre de valeurs manquantes par variable  
   - Tout autre élément descriptif pertinent  

2. **Statistiques descriptives** :  
   - Moyenne, médiane, min/max selon les variables  
   - Analyse adaptée aux données numériques et catégorielles  

3. **Visualisations interactives** :  
   - Minimum de **5 graphiques**  
   - Intégration de filtres dynamiques : menus déroulants, sliders, checkboxes  

4. **Text Mining** :  
   - Sélection d’un article de presse lié au thème du dataset  
   - Prétraitement du texte : nettoyage, tokenisation, suppression des stopwords  
   - Génération d’un **WordCloud** à partir du texte traité  


## ** Étapes du projet**
### **1️⃣ Choix du dataset**
- Minimum 200 000 lignes  
- Diversité des données : numériques, catégorielles et temporelles   

### **2️⃣ Préparation des données**
- Analyse exploratoire (EDA)  
- Nettoyage : traitement des valeurs manquantes, suppression des doublons, correction des incohérences  
- Justification de toutes les transformations ou suppressions  

### **3️⃣ Création de nouvelles variables**
- Générer au moins **2 variables dérivées** pertinentes à partir des données existantes  

### **4️⃣ Visualisation des tendances**
- Graphiques variés pour explorer les relations entre variables  
- Intégration de filtres interactifs pour permettre la sélection de sous-ensembles  

### **5️⃣ Partie Text Mining**
- Choix d’un article lié au dataset  
- Prétraitement du texte  
- Génération d’un WordCloud  
 
---

## ** Contenu attendu pour le rendu**
1. `requirements.txt` : toutes les librairies utilisées avec leurs versions  
2. `MEMBRES.txt` : noms et prénoms des membres du groupe et lien vers le dataset utilisé  
3. `NOTEBOOKS/` : notebook Jupyter pour exploration, nettoyage et création de variables  
4. `APP/` : fichiers `.py` de l’application Streamlit complète  

## ** Résultats attendus**
- Résumé du dataset avec informations principales  
- Statistiques descriptives et graphiques interactifs  
- Filtres dynamiques pour explorer le dataset  
- WordCloud issu de l’article de presse choisi  
- Tableau de bord interactif complet et fonctionnel
