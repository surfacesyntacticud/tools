import pandas as pd 

file_path = "lefff-3.4.mlex"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines() # stocker les lignes dans une liste
# dictionnaire pour stocker les formes morphosyntaxiques des participes
part_forms = {}

for line in lines:
    parts = line.strip().split("\t")
    if len(parts) >=3: # la ligne comprend au moins trois éléments : forme, catégorie, lemme
        form, pos, lemma = parts[:3]
        if pos == "adj" or pos == "v": 
            morphosyn = parts[3] if len(parts) > 3 else "" # extraire les traits morphosyntaxiques

            if morphosyn.startswith("K"): # prendre uniquement les formes Kms, Kmf, Kmp, Kfp (participe)
                if lemma not in part_forms: # initialiser le lemme s'il n'est pas dans le dictionnaire
                    part_forms[lemma] = []   # liste de tuples (forme, trait)
                part_forms[lemma].append((form, morphosyn)) # ajouter les traits au lemme correspondant

# Créer des compteurs
nb_part_total = 0
nb_part_silent = 0
nb_part_silent_number = 0
nb_part_silent_gender = 0
nb_part_invariable = 0
nb_part_exception = 0

# Initialiser des ensembles de participes
part_silent = set()
part_silent_number = set()
part_silent_gender = set()
part_invariable = set()
part_exception = set()   # participes au pluriel audible au masculin mais silencieux au féminin

part_summary = []  # Liste pour stocker les résultats

# Créer des listes de formes
exception = ["K"]
masculine = ["Km", "Kms", "Kmp"]
feminine = ["Kf", "Kfs", "Kfp"]
plural = ["Kp", "Kmp", "Kfp"]
singular = ["Ks", "Kms", "Kfs", "Km"]

# Règles
silent = ["a", "e", "i", "o", "u", "y", "eil", "rieur", "é", "ï", "û"] # variations en nombre et en genre silencieuses
audible_gender = ["f", "eux", "eau", "t", "eur", "s", "n"]  # variations en genre audibles
silent_exception_gender = ["majeur", "mineur", "meilleur"]  # exceptions de variations en genre silencieuses
audible_number = ["al"] # variations en -aux au masculin pluriel
silent_exception_number = ["bancal", "banal", "fatal", "glacial", "natal", "naval"] # exceptions de variations en nombre silencieuses

# Parcourir la liste de participes
for lemma, forms in part_forms.items():
    nb_part_total += 1

    ms_form = next((form for form, ms in forms if ms == "Kms" or ms == "Km"), None)

    # Vérifier la présence de traits pour toutes les formes de participes
    has_audible_number = ms_form and ms_form.endswith(tuple(audible_number))
    has_audible_gender = ms_form and ms_form.endswith(tuple(audible_gender))
    is_silent = ms_form and ms_form.endswith(tuple(silent))

    has_mp_form = any(ms == "Kmp" for _, ms in forms)
    has_form_ending_aux = any(form.endswith("aux") for form, ms in forms if ms == "Kmp")
    has_form_ending_al = any(form.endswith("al") for form, ms in forms if ms == "Kmp")

    has_masculine = any(ms in masculine for _, ms in forms)
    has_feminine = any(ms in feminine for _, ms in forms)
    has_singular = any(ms in singular for _, ms in forms)
    has_plural = any(ms in plural for _, ms in forms)

    category = ""

    # participes aux traits Number[ctxt] et Gender[ctxt]
    if is_silent and not has_audible_gender or lemma in silent_exception_gender:
        part_silent.add(lemma)
        nb_part_silent += 1
        category = "variations en genre et en nombre silencieuses"
        part_summary.append([lemma, forms, category])
        continue

    # participes au trait Number[ctxt]
    if has_masculine and has_feminine and not is_silent and has_audible_gender:
        part_silent_number.add(lemma)
        nb_part_silent_number += 1
        category = "variations en genre audible et en nombre silencieuses"
        part_summary.append([lemma, forms, category])
        continue
    
    # traitement du cas des participes dont le lemme finit par -al
    if not is_silent and has_audible_number:
        if lemma.endswith("al") and has_mp_form and has_feminine:
            # participes au trait Gender[ctxt] et au trait Number[ctxt] uniquement au féminin
            if has_form_ending_aux:
                part_exception.add(lemma)
                nb_part_exception += 1
                category = "variations en genre silencieuses et en nombre audibles au masculin mais silencieuses au féminin"
                part_summary.append([lemma, forms, category])
                continue
            # participes au trait Gender[ctxt] et Number[ctxt]
            else:
                part_silent.add(lemma)
                nb_part_silent += 1
                category = "variations en genre et en nombre silencieuses"
                part_summary.append([lemma, forms, category])
                continue
        # participes au trait Gender[ctxt]
        else:
            part_silent_gender.add(lemma)
            nb_part_silent_gender += 1
            category = "variations en genre silencieuses et en nombre audibles"
            part_summary.append([lemma, forms, category])
            continue

    # participes au trait Gender[ctxt] et Number[ctxt]
    else:
        part_invariable.add(lemma)
        nb_part_invariable += 1
        category = "invariable" 
        part_summary.append([lemma, forms, category])
        continue

# Création du dataframe pour les résultats
part_df = pd.DataFrame(part_summary, columns=["participes", "ensembles des traits morpho", "catégorie"])

# Sauvegarde des participes dans différents fichiers .lex
def save_lex_file(filename, data_set):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("part\n%-------------\n")
        for item in sorted(data_set):
            f.write(f"{item}\n")

save_lex_file("part_silent.lex", part_silent)
save_lex_file("part_silent_number.lex", part_silent_number)
save_lex_file("part_invariable.lex", part_invariable)

# Sauvegarde des résultats dans un fichier CSV si nécessaire
part_df.to_csv("part_silent.csv", index=False)

# Affichage des statistiques
print(f"Nombre total de participes : {nb_part_total}")
print(f"Genre et nombre silencieux : {nb_part_silent}")
print(f"Genre audible, nombre silencieux : {nb_part_silent_number}")
print(f"Genre silencieux, nombre audible : {nb_part_silent_gender}")
print(f"Invariables : {nb_part_invariable}")