# =====================================================================
# IMPORTS
# =====================================================================
import pandas as pd
import numpy as np
import os
import re

# =====================================================================
# CHARGEMENT DES DONNÉES BRUTES 
# =====================================================================
caract_2023 = pd.read_csv("caract-2023.csv", sep=";")
lieux_2023 = pd.read_csv("lieux-2023.csv", sep=";")
usagers_2023 = pd.read_csv("usagers-2023.csv", sep=";")
vehicules_2023 = pd.read_csv("vehicules-2023.csv", sep=";")

# =====================================================================
# DIAGNOSTIC CARACTÉRISTIQUES 2023
# =====================================================================
def diagnostic(df, year):
    print(f"\n=== DIAGNOSTIC CARACT {year} ===")
    print(f"Lignes : {df.shape[0]}")
    print(f"Colonnes : {df.shape[1]}")
    print("Valeurs manquantes :")
    print(df.isna().sum())
    print("Doublons Num_Acc :", df["Num_Acc"].duplicated().sum())

    print("Vérification jour/mois/an :")
    print("Jour hors plage :", df[(df['jour'] < 1) | (df['jour'] > 31)].shape[0])
    print("Mois hors plage :", df[(df['mois'] < 1) | (df['mois'] > 12)].shape[0])
    print("Année incohérente :", df[df['an'] != int(year)].shape[0], "\n")

    bad_hrmn = df[~df['hrmn'].astype(str).str.match(r'^\d{1,2}:\d{2}$', na=False)]
    print("Heures/minutes incorrectes :", len(bad_hrmn))

    print("lat avec virgule :", df['lat'].astype(str).str.contains(",").sum())
    print("long avec virgule :", df['long'].astype(str).str.contains(",").sum(), "\n")

diagnostic(caract_2023, "2023")

# =====================================================================
# NETTOYAGE CARACTÉRISTIQUES 2023
# =====================================================================

def nettoyer_caracteristiques(df):
    df = df.copy()

    # Correction lat / long (virgule -> point)
    df["lat"] = (df["lat"].astype(str).str.replace(",", ".", regex=False).astype(float))
    df["long"] = (df["long"].astype(str) .str.replace(",", ".", regex=False) .astype(float) )

    # Colonnes numériques à convertir
    cols_num = ["jour", "mois", "an", "hrmn", "lum", "agg", "int", "atm", "col"]

    for col in cols_num:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Bornes issues de la documentation BAAC
    plage = {
        "jour": (1, 31),
        "mois": (1, 12),
        "an": (1900, 2100),
        "hrmn": (0, 2359),
        "lum": (1, 5),
        "agg": (1, 2),
        "int": (1, 8),
        "atm": (1, 9),
        "col": (1, 7)
    }

    for col, (minv, maxv) in plage.items():
        df.loc[(df[col] < minv) | (df[col] > maxv), col] = np.nan

    cols_int = ["jour", "mois", "an", "hrmn", "lum", "agg", "int", "atm", "col"]

    for col in cols_int:
        df[col] = df[col].astype("Int64")

    return df


# =====================================================================
# DIAGNOSTIC LIEUX 2023
# =====================================================================
def diagnostic_lieux(df, year):
    print(f"\n=== DIAGNOSTIC LIEUX {year} ===")
    print(df.info())
    print("Valeurs manquantes :")
    print(df.isna().sum())
    print("Doublons Num_Acc :", df["Num_Acc"].duplicated().sum())

diagnostic_lieux(lieux_2023, "2023")

# =====================================================================
# NETTOYAGE LIEUX 2023
# =====================================================================
def nettoyer_lieux(df):
    df = df.copy()
    cols = ["voie", "v2", "nbv", "pr", "pr1", "lartpc", "larrout"]
    for col in cols:
        df[col] = df[col].replace({"": np.nan, " ": np.nan})

    for col in ["voie", "v2", "nbv", "pr", "pr1", "larrout"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Bornes issues de la documentation BAAC
    plage = {
        "catr": (1, 9),
        "circ": (1, 9),
        "prof": (0, 9),
        "plan": (1, 9),
        "surf": (1, 9),
        "infra": (0, 9),
        "situ": (1, 8),
        "vma": (0, 150)
    }

    for col, (minv, maxv) in plage.items():
        df.loc[(df[col] < minv) | (df[col] > maxv), col] = np.nan

    cols_int = [
        "catr", "circ", "nbv", "prof", "surf", "infra", "situ", "vma"
    ]

    for col in cols_int:
        df[col] = df[col].astype("Int64")

    return df

lieux_2023_clean = nettoyer_lieux(lieux_2023)

# =====================================================================
# DIAGNOSTIC USAGERS 2023
# =====================================================================
def diagnostic_usagers(df, year):
    print(f"\n=== DIAGNOSTIC USAGERS {year} ===\n")
    print(df.info())
    print("\nValeurs manquantes :\n", df.isna().sum())
    print("Doublons Num_Acc + id_usager :", df.duplicated(subset=["Num_Acc", "id_usager"]).sum(), "\n")

diagnostic_usagers(usagers_2023, "2023")

# =====================================================================
# NETTOYAGE USAGERS 2023
# =====================================================================
def nettoyer_usagers(df):
    df = df.copy()
    df["id_vehicule"] = df["id_vehicule"].astype(str).str.replace(" ", "").str.replace("\xa0", "")
    df["id_usager"] = df["id_usager"].astype(str).str.replace(" ", "").str.replace("\xa0", "")

    aberrants = [-1, 0, 99, 999, "99", "0"]

    for col in df.columns:
        df[col] = df[col].replace(aberrants, np.nan)

# Bornes issues de la documentation BAAC
    plages = {
        "sexe": (1, 2),
        "grav": (1, 4),
        "trajet": (1, 9),
        "locp": (1, 9),
        "actp": (1, 13),
        "place": (1, 9)
    }

    for col, (minv, maxv) in plages.items():
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[(df[col] < minv) | (df[col] > maxv), col] = np.nan
    
    cols_int = [
        "Num_Acc","id_usager","place","catu","grav","sexe","an_nais","trajet"

    ]

    for col in cols_int:
        df[col] = df[col].astype("Int64")
    
    return df

usagers_2023_clean = nettoyer_usagers(usagers_2023)

# =====================================================================
# DIAGNOSTIC VEHICULES 2023
# =====================================================================
def diagnostic_vehicules(df, year):
    print(f"\n=== DIAGNOSTIC VEHICULES {year} ===\n")
    print(df.info())
    print("Doublons Num_Acc + id_vehicule :", df.duplicated(subset=["Num_Acc", "id_vehicule"]).sum())

diagnostic_vehicules(vehicules_2023, "2023")

# =====================================================================
# NETTOYAGE VÉHICULES 2023
# =====================================================================
def nettoyer_vehicules(df):
    df = df.copy()
    df["id_vehicule"] = df["id_vehicule"].astype(str).str.replace(" ", "").str.replace("\xa0", "")

    aberrants = [-1, 0, 999, "0"] # ici pas de 99 car la catégorie autres de catv va jusqu'à 99

    for col in df.columns:
        df[col] = df[col].replace(aberrants, np.nan)

# Bornes issues de la documentation BAAC
    plages = {
        "senc": (1, 3),
        "catv": (1, 99),
        "choc": (1, 9),
        "manv": (1, 26),
        "motor": (1, 6)
    }

    for col, (minv, maxv) in plages.items():
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[(df[col] < minv) | (df[col] > maxv), col] = np.nan

    cols_int = [
        "senc", "catv", "choc", "manv", "motor"
    ]

    for col in cols_int:
        df[col] = df[col].astype("Int64")
    return df

vehicules_2023_clean = nettoyer_vehicules(vehicules_2023)

# =====================================================================
# SUPPRESSION COLONNES INUTILES
# =====================================================================

### ---- CARACT 2023 ----
cols_drop_caract = [
    "dep", "com", "int",   
    "adr"                           
]
caract_2023.drop(columns=cols_drop_caract, inplace=True, errors="ignore")


### ---- LIEUX 2023 ----
cols_drop_lieux = [
    "voie",      
    "v1",        
    "larrout",   
    "v2",
    "lartpc",
    "plan",
    "pr","pr1" 
     
]
lieux_2023_clean.drop(columns=cols_drop_lieux, inplace=True, errors="ignore")


### ---- USAGERS 2023 ----
cols_drop_usagers = [
    "num_veh",
    "trajet",
    "locp",
    "actp",
    "etatp",
    "secu1", "secu2", "secu3"  
]
usagers_2023_clean.drop(columns=cols_drop_usagers, inplace=True, errors="ignore")


### ---- VÉHICULES 2023 ----
cols_drop_veh = [
    "motor",
    "num_veh",
    "obs",
    "obsm",
    "manv",
    "occutc"     
]
vehicules_2023_clean.drop(columns=cols_drop_veh, inplace=True, errors="ignore")
# =====================================================================
# AJOUT DE VARIABLES SUPPLÉMENTAIRES 
# =====================================================================
def periode_journee(h):
    if "00:00" <= h < "06:00":
        return "Nuit"
    elif "06:00" <= h < "12:00":
        return "Matin"
    elif "12:00" <= h < "18:00":
        return "Après-midi"
    else:
        return "Soir"

caract_2023["periode"] = caract_2023["hrmn"].apply(periode_journee)


def gravite_3_niveaux(grav):
    if pd.isna(grav):
        return None
    elif grav == 2:
        return "Tué"
    elif grav == 3:
        return "Blessé hospitalisé"
    elif grav in [1, 4]:
        return "Indemne"
    else:
        return None
usagers_2023_clean["grav_3_niveaux"] = usagers_2023_clean["grav"].apply(gravite_3_niveaux)

# 
usagers_2023_clean["age"] = 2023 - usagers_2023_clean["an_nais"]

def tranche_age(a):
    if pd.isna(a): 
        return None
    elif a < 18:
        return "Mineur"
    elif a < 25:
        return "18–24"
    elif a < 40:
        return "25–39"
    elif a < 60:
        return "40–59"
    else:
        return "60+"

usagers_2023_clean["tranche_age"] = usagers_2023_clean["age"].apply(tranche_age)

# Fusion de la variable agg (table caractéristiques) dans la table lieux

lieux_2023_clean = lieux_2023_clean.merge(
    caract_2023[["Num_Acc", "agg"]],
    on="Num_Acc",
    how="left"
)

def zone_detaillee(agg, catr, vma):
    if pd.isna(agg) or pd.isna(vma):
        return None
    elif catr == 1 or vma >= 90:
        return "Autoroute"
    elif agg == 2 and vma <= 50:
        return "Zone urbaine dense"
    elif agg == 1 and vma <= 80:
        return "Zone rurale"
    else:
        return "Autre"

lieux_2023_clean["zone_detaillee"] = lieux_2023_clean.apply(
    lambda x: zone_detaillee(x["agg"], x["catr"], x["vma"]),
    axis=1
)

def niveau_vitesse(v):
    if pd.isna(v):
        return None
    elif v <= 30:
        return "Faible"
    elif v <= 70:
        return "Moyenne"
    else:
        return "Élevée"
lieux_2023_clean["niveau_vitesse"] = lieux_2023_clean["vma"].apply(niveau_vitesse)

# =====================================================================
# EXPORT FINAL 2023
# =====================================================================
os.makedirs("clean", exist_ok=True)

caract_2023.to_csv("clean/caract_2023_clean.csv", index=False)
lieux_2023_clean.to_csv("clean/lieux_2023_clean.csv", index=False)
usagers_2023_clean.to_csv("clean/usagers_2023_clean.csv", index=False)
vehicules_2023_clean.to_csv("clean/vehicules_2023_clean.csv", index=False)

# MERGE FINAL 2023
df_2023 = (
    caract_2023
        .merge(lieux_2023_clean, on="Num_Acc", how="left")
        .merge(vehicules_2023_clean, on="Num_Acc", how="left")
        .merge(usagers_2023_clean, on=["Num_Acc", "id_vehicule"], how="left")
)

df_2023.to_csv("clean/final_2023.csv", index=False)

print("Informations finales après nettoyage :\n")
caract_2023.info()
caract_2023.isna().mean()

lieux_2023_clean.info()
lieux_2023_clean.isna().mean()

usagers_2023_clean.info()
usagers_2023_clean.isna().mean()

vehicules_2023_clean.info()
vehicules_2023_clean.isna().mean()
