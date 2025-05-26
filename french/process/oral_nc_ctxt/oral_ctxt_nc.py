import pandas as pd 

file_path = "lefff-3.4.mlex"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines() # stocker les lignes dans une liste
# dictionnaire pour stocker les formes morphosyntaxiques des noms communs
nc_forms = {}

for line in lines:
    parts = line.strip().split("\t")
    if len(parts) >=3: # la ligne comprend au moins trois éléments : forme, catégorie, lemme
        form, pos, lemma = parts[:3]
        if pos == "nc": 
            morphosyn = parts[3] if len(parts) > 3 else "" # extraire les traits morphosyntaxiques

            if lemma not in nc_forms: # initialiser le lemme s'il n'est pas dans le dictionnaire
                nc_forms[lemma] = set()
            nc_forms[lemma].add(morphosyn) # ajouter les traits au lemme correspondant

# Créer des compteurs
nb_nc_total = 0
nb_nc_silent_number = 0
nb_nc_audible_number = 0
nb_nc_invariable_number = 0
nb_nc_exception_number = 0

# Initialiser des ensembles de noms communs
nc_silent_number = set()
nc_audible_number = set()
nc_invariable_number = set()
nc_silent_gender = set()
nc_exception_number = set()

nc_summary = []  # Liste pour stocker les résultats

# Créer des listes de formes
exception = ["m", "f"]
masculine = ["m", "ms", "mp"]
feminine = ["f", "fs", "fp"]
plural = ["p", "mp", "fp"]
singular = ["s", "ms", "fs", "m"]

# Règles sur le nombre
# noms qui se terminent en -al mais dont le pluriel ne s'entend pas
silent_exception_number = ["appeal", "aval", "bal", "barbital", "cal", "captal", "carnaval", "cérémonial", "chacal", "chloral", "chrysocal", "copal", "dial", "dispersal", "éthanal", "festival", "foiral", "furfural", "futal", "gal", "galgal", "gardénal", "graal", "joual", "kraal", "kursaal", "matorral", "mescal", "mezcal", "méthanal", "minerval", "mistral", "nopal", "pal", "pascal", "penthotal", "phénobarbital", "pipéronal", "raval", "récital", "régal", "rétinal", "rital", "roberval", "roseval", "salicional", "sal", "sandal", "santal", "saroual", "sial", "sisal", "sonal", "tagal", "tefal", "tergal", "thiopental", "tical", "tincal", "véronal", "zicral", "bacchanal", "bancal", "cantal", "caracal", "chacal", "gavial", "gayal", "narval", "quetzal", "rorqual", "serval", "emmental", "emmenthal", "floréal", "germinal", "prairial", "deal", "goal", "choral", "corral", "dorsal", "final", "fractal", "fécial", "fétial", "latéral", "mental", "moral", "morfal", "mural", "musical", "spiritual", "negro-spiritual", "surtravail", "paranormal", "penthiobarbital", "pied-de-cheval", "protal", "queue-de-cheval", "rational", "revival", "sex-appeal", "social", "sortie-de-bal", "spatial", "squamosal", "technival", "trial", "téléjournal", "val", "étal"]
audible_number = ["al"] # noms qui se terminent par -al et prennent -aux au pluriel
audible_exception_number = ["boeuf", "oeuf", "os", "vieil", "topos", "corail", "bail", "émail", "soupirail", "vantail", "ventail", "vitrail", "ail", "fermaux", "frontail"] # noms qui se prononcent différemment au pluriel
exception_number = ["oeil", "aïeul", "ciel"]    # noms qui ont deux formes au pluriel selon le sens employé (e.g yeux et oeils pour oeils de boeuf)

# Parcourir la liste de noms communs
for lemma, forms in nc_forms.items():
    nb_nc_total += 1

    # Vérifier la présence de traits pour toutes les formes de noms communs
    has_audible_number = lemma.endswith(tuple(audible_number))

    has_exception = any(form in exception for form in forms)
    has_masculin = any(form in masculine for form in forms)
    has_feminin = any(form in feminine for form in forms)
    has_singular = any(form in singular for form in forms)
    has_plural = any(form in plural for form in forms)

    category = ""

    # Vérifie si le nom commun se termine par une lettre muette si seulement un 's' est ajouté
    if (lemma in silent_exception_number) or (has_plural and has_singular and not has_audible_number and lemma not in audible_exception_number and lemma not in exception_number):
        nc_silent_number.add(lemma)
        nb_nc_silent_number += 1
        category = "variation du pluriel silencieuse"
        nc_summary.append([lemma, forms, category])
        continue

    if (lemma in audible_exception_number) or (has_plural and has_singular and has_audible_number and lemma not in silent_exception_number and lemma not in exception_number):
        nc_audible_number.add(lemma)
        nb_nc_audible_number += 1
        category = "variation du pluriel audible"
        nc_summary.append([lemma, forms, category])
        continue

    if lemma in exception_number:
        nc_exception_number.add(lemma)
        nb_nc_exception_number += 1
        category = "deux formes au pluriel selon le sens"
        nc_summary.append([lemma, forms, category])
        continue

    if (has_singular and not has_plural) or (has_plural and not has_singular):
        nc_invariable_number.add(lemma)
        nb_nc_invariable_number += 1
        category = "invariable en nombre"
        nc_summary.append([lemma, forms, category])
        continue
    
    else:
        nc_invariable_number.add(lemma)
        nb_nc_invariable_number += 1
        category = "invariable en nombre"
        nc_summary.append([lemma, forms, category])
        continue

# Création du dataframe pour les résultats
nc_df = pd.DataFrame(nc_summary, columns=["noms communs", "ensembles des traits morpho", "catégorie"])


# Sauvegarde des noms communs dans différents fichiers .lex
def save_lex_file(filename, data_set):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("nc\n%-------------\n")
        for item in sorted(data_set):
            f.write(f"{item}\n")

save_lex_file("nc_silent_number.lex", nc_silent_number)
save_lex_file("nc_invariable_number.lex", nc_invariable_number)
save_lex_file("nc_exception_number.lex", nc_exception_number)

# Sauvegarde des résultats dans un fichier CSV si nécessaire
nc_df.to_csv("nc_silent.csv", index=False)

# Affichage des statistiques
print(f"Nombre total de noms : {nb_nc_total}")
print(f"Au pluriel silencieux: {nb_nc_silent_number}")
print(f"Au pluriel audible : {nb_nc_audible_number}")
print(f"Sans variation : {nb_nc_invariable_number}")
print(f"À deux formes au pluriel : {nb_nc_exception_number}")