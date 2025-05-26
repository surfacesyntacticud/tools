import pandas as pd

# Charger le fichier Lefff
file_path = "lefff-3.4.mlex"

# Dictionnaire pour stocker les formes morphologiques des noms communs
nc_forms = {}

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        # Chaque ligne doit comprendre au moins trois éléments : forme, catégorie gramaticale, lemme
        if len(parts) >=3: 
            form, pos, lemma = parts[:3]
            if pos == "nc": 
                # Récupérer les traits morphosyntaxiques
                morphosyn = parts[3] if len(parts) > 3 else "" 
                if lemma not in nc_forms:
                    nc_forms[lemma] = set()
                nc_forms[lemma].add(morphosyn) 

# Initialisation des compteurs et des listes
nb_nc_total = 0
nb_nc_number_ctxt = 0
nc_number_ctxt = set()
nc_summary = []

# Chercher uniquement les noms dont la seule information morpho est "m" ou "f"
for lemma, forms in nc_forms.items():
    nb_nc_total += 1
    # Les noms ne varient pas selon le nombre
    if forms == {"m"} or forms == {"f"}:
        nc_number_ctxt.add(lemma)
        nb_nc_number_ctxt += 1
        category = "Nombre contextuel à l’écrit"
        nc_summary.append([lemma, forms, category])

# Sauvegarder les résultats dans un fichier CSV
nc_df = pd.DataFrame(nc_summary, columns=["noms communs", "traits morpho", "catégorie"])
nc_df.to_csv("nc_number_ctxt.csv", index=False)

# Sauvegarder les lemmes dans un fichier .lex
with open("nc_number_ctxt.lex", "w", encoding="utf-8") as f:
    f.write("nc\n")
    f.write("%-------------\n")
    for lemma in sorted(nc_number_ctxt):
        f.write(f"{lemma}\n")

# Afficher les statistiques
print(f"Nombre total de noms communs : {nb_nc_total}")
print(f"Nombre de noms à marquer Number[ctxt] : {nb_nc_number_ctxt}")
