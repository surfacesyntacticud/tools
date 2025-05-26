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

            if morphosyn.startswith("K"): #ignorer les formes Kms, Kmf, Kmp, Kfp (participe)
                continue

            if lemma not in adj_forms: # initialiser le lemme s'il n'est pas dans le dictionnaire
                adj_forms[lemma] = []   # liste de tuples (forme, trait)
            adj_forms[lemma].append((form, morphosyn)) # ajouter les traits au lemme correspondant

# Créer des compteurs
nb_adj_total = 0
nb_adj_silent = 0
nb_adj_silent_number = 0
nb_adj_silent_gender = 0
nb_adj_invariable = 0
nb_adj_exception = 0

# Initialiser des ensembles d'adjectifs
adj_silent = set()
adj_silent_number = set()
adj_silent_gender = set()
adj_invariable = set()
adj_exception = set()   # adjectifs au pluriel audible au masculin mais silencieux au féminin

adj_summary = []  # Liste pour stocker les résultats

# Créer des listes de formes
masculine = ["m", "ms", "mp"]
feminine = ["f", "fs", "fp"]
plural = ["p", "mp", "fp"]
singular = ["s", "ms", "fs", "m"]

# Règles
silent = ["a", "e", "i", "o", "u", "y", "eil", "rieur"] # variations en nombre et en genre silencieuses
audible_gender = ["f", "eux", "eau", "t", "eur", "s", "n"]  # variations en genre audibles
silent_exception_gender = ["majeur", "mineur", "meilleur"]  # exceptions de variations en genre silencieuses
audible_number = ["al"] # variations en -aux au masculin pluriel
silent_exception_number = ["bancal", "banal", "fatal", "glacial", "natal", "naval"] # exceptions de variations en nombre silencieuses

# Parcourir la liste d'adjectifs
for lemma, forms in adj_forms.items():
    nb_adj_total += 1

    # Vérifier la présence de traits pour toutes les formes d'adjectifs
    has_audible_number = lemma.endswith(tuple(audible_number))
    has_audible_gender = lemma.endswith(tuple(audible_gender))
    is_silent = lemma.endswith(tuple(silent))

    has_mp_form = any(ms == "mp" for _, ms in forms)
    has_form_ending_aux = any(form.endswith("aux") for form, ms in forms if ms == "mp")
    has_form_ending_al = any(form.endswith("al") for form, ms in forms if ms == "mp")

    has_masculine = any(form in masculine for _, form in forms)
    has_feminine = any(form in feminine for _, form in forms)
    has_singular = any(form in singular for _, form in forms)
    has_plural = any(form in plural for _, form in forms)

    category = ""

    # adjectifs aux traits Number[ctxt] et Gender[ctxt]
    if is_silent and not has_audible_gender or lemma in silent_exception_gender:
        adj_silent.add(lemma)
        nb_adj_silent += 1
        category = "variations en genre et en nombre silencieuses"
        adj_summary.append([lemma, forms, category])

        continue

    # adjectifs au trait Number[ctxt]
    if has_masculine and has_feminine and not is_silent and has_audible_gender:
        adj_silent_number.add(lemma)
        nb_adj_silent_number += 1
        category = "variations en genre audible et en nombre silencieuses"
        adj_summary.append([lemma, forms, category])
        continue
    
    # traitement du cas des adjectifs dont le lemme finit par -al
    if not is_silent and has_audible_number:
        if lemma.endswith("al") and has_mp_form and has_feminine:
            # adjectifs au trait Gender[ctxt] et au trait Number[ctxt] uniquement au féminin
            if has_form_ending_aux:
                adj_exception.add(lemma)
                nb_adj_exception += 1
                category = "variations en genre silencieuses et en nombre audibles au masculin mais silencieuses au féminin"
                adj_summary.append([lemma, forms, category])
                continue
            # adjectifs au trait Gender[ctxt] et Number[ctxt]
            else:
                adj_silent.add(lemma)
                nb_adj_silent += 1
                category = "variations en genre et en nombre silencieuses"
                adj_summary.append([lemma, forms, category])
                continue
        # adjectifs au trait Gender[ctxt]
        else:
            adj_silent_gender.add(lemma)
            nb_adj_silent_gender += 1
            category = "variations en genre silencieuses et en nombre audibles"
            adj_summary.append([lemma, forms, category])
            continue

    # adjectifs au trait Gender[ctxt] et Number[ctxt]
    else:
        adj_invariable.add(lemma)
        nb_adj_invariable += 1
        category = "invariable"
        adj_summary.append([lemma, forms, category])
        continue

# Création du dataframe pour les résultats
adj_df = pd.DataFrame(adj_summary, columns=["adjectifs", "ensembles des traits morpho", "catégorie"])

# Sauvegarde des adjectifs dans différents fichiers .lex
def save_lex_file(filename, data_set):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("adj\n%-------------\n")
        for item in sorted(data_set):
            f.write(f"{item}\n")

save_lex_file("adj_silent.lex", adj_silent)
save_lex_file("adj_silent_number.lex", adj_silent_number)
save_lex_file("adj_silent_gender.lex", adj_silent_gender)
save_lex_file("adj_invariable.lex", adj_invariable)
save_lex_file("adj_exception.lex", adj_exception)

# Sauvegarde des résultats dans un fichier CSV si nécessaire
adj_df.to_csv("adj_silent.csv", index=False)

# Affichage des statistiques
print(f"Nombre total d'adjectifs : {nb_adj_total}")
print(f"Genre et nombre silencieux : {nb_adj_silent}")
print(f"Genre audible, nombre silencieux : {nb_adj_silent_number}")
print(f"Genre silencieux, nombre audible : {nb_adj_silent_gender}")
print(f"Invariables : {nb_adj_invariable}")
print(f"Genre silencieux, nombre audible au masculin uniquement : {nb_adj_exception}")