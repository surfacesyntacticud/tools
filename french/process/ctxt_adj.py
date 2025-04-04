import pandas as pd 

file_path = "lefff-3.4.mlex"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines() # stocker les lignes dans une liste
# dictionnaire pour stocker les formes morphosyntaxiques des adjectifs
adj_forms = {}

for line in lines:
    parts = line.strip().split("\t")
    if len(parts) >=3: # la ligne comprend au moins trois éléments : forme, catégorie, lemme
        form, pos, lemma = parts[:3]
        if pos == "adj": 
            morphosyn = parts[3] if len(parts) > 3 else "" # extraire les traits morphosyntaxiques

            if morphosyn.startswith("K"): #ignorer les formes Kms, Kmf, Kmp, Kfp (participe passé)
                continue

            if lemma not in adj_forms: # initialiser le lemme s'il n'est pas dans le dictionnaire
                adj_forms[lemma] = set()
            adj_forms[lemma].add(morphosyn) # ajouter les traits au lemme correspondant

# Créer des compteurs
nb_adj_total = 0
nb_adj_without_gender = 0
nb_adj_without_number = 0
nb_adj_invariable = 0
nb_exception = 0

# Initialiser des ensembles d'adjectifs
adj_without_gender = set()
adj_without_number = set()
adj_invariable = set()
adj_with_exception = set()

adj_summary = []  # Liste pour stocker les résultats

# Créer des listes de formes
exception = ["m"]
masculin = ["ms", "mp"]
feminin = ["fs", "fp"]
plural = ["p", "mp", "fp"]
singular = ["s", "ms", "fs"]


# Parcourir la liste d'adjectif
for lemma, forms in adj_forms.items():
    nb_adj_total += 1

    # Vérifier la présence de traits pour toutes les formes de l'adjectif
    has_masculin = any(form in masculin for form in forms)
    has_feminin = any(form in feminin for form in forms)
    has_singular = any(form in singular for form in forms)
    has_plural = any(form in plural for form in forms)
    has_exception = any(form in exception for form in forms)

    # Vérifie si l'adjectif varie en nombre au féminin mais pas au masculin
    if has_exception and has_feminin and has_plural:
        nb_exception += 1
        adj_with_exception.add(lemma)
        category = "Varie en genre et en nombre au féminin et ne varie pas en nombre au masculin"
        adj_summary.append([lemma, forms, category]) # ajouter les adjectifs spéciaux dans le csv avant de sortir de la boucle
        continue # éviter qu'ils soient ajouté à d'autres listes comme adj_without_gender.lex

    # Vérifier si l'adjectif varie en genre
    if (has_masculin and not has_feminin) or (has_feminin and not has_masculin) or (not has_feminin) or (not has_masculin):
        adj_without_gender.add(lemma)  # adjectif sans variation de genre
        nb_adj_without_gender += 1
        category = "Ne varie pas en genre"

    # Vérifier si l'adjectif varie en nombre
    if (has_singular and not has_plural) or (has_plural and not has_singular) or (not has_singular) or (not has_plural):
        adj_without_number.add(lemma)  # adjectif sans variation de nombre
        nb_adj_without_number += 1
        category = "Ne varie pas en nombre"
    

    if has_masculin and has_feminin:
        category = "Varie en genre"

    if has_singular and has_plural and not has_exception:
        category = "Varie en nombre"

    if has_masculin and has_feminin and has_plural and has_singular:
        category = "Varie en genre et en nombre"

    if not has_masculin and not has_feminin and not has_singular and not has_plural:
        nb_adj_invariable += 1
        adj_invariable.add(lemma)
        category = "Ne varie pas en genre et en nombre"

    adj_summary.append([lemma, forms, category])

# Création du dataframe pour les résultats
adj_df = pd.DataFrame(adj_summary, columns=["adjectifs", "ensembles des traits morpho", "catégorie"])

# Sauvegarde des adjectifs dans différents fichiers .lex
with open("adj_without_gender.lex", "w", encoding="utf-8") as f:
    for adj in sorted(adj_without_gender):
        f.write(f"{adj}\n")

with open("adj_without_number.lex", "w", encoding="utf-8") as f:
    for adj in sorted(adj_without_number):
        f.write(f"{adj}\n")

with open("adj_invariable.lex", "w", encoding="utf-8") as f:
    for adj in sorted(adj_invariable):
        f.write(f"{adj}\n")

with open("adj_with_exception.lex", "w", encoding="utf-8") as f:
    for adj in sorted(adj_with_exception):
        f.write(f"{adj}\n")


# Sauvegarde des résultats dans un fichier CSV si nécessaire
adj_df.to_csv("adjectifs_lefff.csv", index=False)

# Affichage des statistiques
print(f"Nombre total d'adjectifs : {nb_adj_total}")
print(f"Sans variation de genre : {nb_adj_without_gender}")
print(f"Sans variation de nombre : {nb_adj_without_number}")
print(f"Sans variation : {nb_adj_invariable}")
print(f"Sans variation de nombre sur le masculin : {nb_exception}")