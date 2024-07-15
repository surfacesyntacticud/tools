# Règles Grew pour instancier le trait Subject des infinitifs

> écrit par Guy Perrier en mars 2023

Le principe est d’appliquer successivement les règles ci-dessous. Après l’application de chaque règle, il faut corriger manuellement les exceptions qui ne rentrent pas dans le cadre de la règle.

 - Infinitifs compléments de nom.

```
pattern{
V[VerbForm=Inf,!Subject, !InIdiom];
N[upos=NOUN|PRON];
N -[udep]-> P; P[upos=ADP]; P -[comp:obj]-> V
}
commands{
V.Subject=SubjRaising
}
```


 - Infinitifs dépendant de relations d’un type qui implique qu’ils ont nécessairement un sujet de type Generic (NoRaising si on ne veut 
pas préciser).
```
pattern{
V[VerbForm=Inf,!Subject, !InIdiom];
H -[1=appos|dislocated|parataxis|root|subj]-> V
}
commands{
V.Subject=Generic
}
```
 - Infinitifs introduits par une préposition qui dépend de relations d’un type qui implique que les infinitifs ont nécessairement un 
sujet de type Generic (NoRaising si on ne veut pas préciser).
```
pattern{
P[upos=ADP];
V[VerbForm=Inf,!Subject, !InIdiom];
P -[comp:obj]-> V;
H -[1=appos|dislocated|parataxis|root|subj]-> P
}
commands{
V.Subject=Generic
}
```
 - Infinitifs dépendant d’un auxiliaire causatif et dont le sujet est l’objet direct de cet auxiliaire.
```
pattern{
V[VerbForm=Inf,!Subject];
AUX -[comp:aux@caus]-> V;
AUX -[comp:obj@agent]-> O
}
commands{
V.Subject=ObjRaising
}
```
 - Infinitifs dépendant d’un auxiliaire causatif et dont le sujet n’est pas exprimé dans la phrase.
```
pattern{
V[VerbForm=Inf,!Subject];
AUX -[comp:aux@caus]-> V;
}
commands{
V.Subject=ObjRaising
}
```
 - Infinitifs attributs du sujet avec le verbe « être ».
```
pattern{
V0[upos=AUX|VERB, lemma = "être"]; 
V0 -[comp:pred]-> V; 
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
%P -[comp:obj]-> V
}
commands{
V.Subject=Generic
}
```
 - Infinitifs introduits par une préposition attributs du sujet avec le verbe « être ».
```
pattern{
V0[upos=AUX|VERB, lemma = "être"]; 
P[upos=ADP]; 
V0 -[comp:pred]-> P; 
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
P -[comp:obj]-> V
}
commands{
V.Subject=Generic
}
```
 - Infinitifs compléments d’un verbe à un temps simple avec un sujet impersonnel.
```
pattern{
V0 -[1=comp]-> V; 
V0 -[1=subj,deep=expl]-> SUBJ;
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
}
commands{
V.Subject=Generic
}
```
 - Infinitifs compléments d’un verbe à un temps composé avec un sujet impersonnel.
```
pattern{
V0 -[1=comp]-> V; 
AUX -[1=comp,2=aux]-> V0;
AUX -[1=subj,deep=expl]-> SUBJ;
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
}
commands{
V.Subject=Generic
}
```
 - Infinitifs introduits par une préposition compléments d’un verbe à un temps simple avec un sujet impersonnel.
```
pattern{
P[upos=ADP];
V0 -[1=comp]-> P; 
V0 -[1=subj,deep=expl]-> SUBJ;
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
P -[comp:obj]-> V
}

commands{
V.Subject=Generic
}
```
 - Infinitifs introduits par une préposition compléments d’un verbe à un temps composé avec un sujet impersonnel.
```
pattern{
AUX -[1=comp,2=aux]-> V0;
AUX -[1=subj,deep=expl]-> SUBJ;
P[upos=ADP];
V0 -[1=comp]-> P; 
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
P -[comp:obj]-> V}
commands{
V.Subject=Generic
}
Auxiliaires à l’infinitif. Le trait à mettre est en général Subject = SubjRaising.
V[upos=AUX,VerbForm=Inf, !Subject, !InIdiom];
}
commands{
V.Subject=SubjRaising
}
}
```
 - Infinitifs introduits par la préposition « pour ».
```
pattern{
P[upos=ADP, lemma=pour];
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
P -[comp:obj]-> V;
}
commands{
V.Subject=Generic
}
```
 - Infinitifs introduits par la locution prépositionnelle « afin de ».
```
pattern{
A[upos=ADV, lemma=afin]; 
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
A -[comp:obj]-> P;
P -[comp:obj]-> V;
}
commands{
V.Subject=Generic
}
```
 - Infinitifs coordonnés. Le trait Subject du premier conjoint est transféré sur les autres.
```
pattern{
V1[VerbForm=Inf,Subject];
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
V1 -[1=conj]-> V;
}
commands{
V.Subject=V1.Subject
}
```
 - Infinitifs introduits par une préposition coordonnés. Le trait Subject du premier conjoint est transféré sur les autres.
```
pattern{
V1[VerbForm=Inf,Subject];
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
V1 -[1=conj]-> V;
}
commands{
V.Subject=V1.Subject
}
```
 - Infinitifs restants. Par défaut, on met Subject=Generic et on corrige manuellement (environ 200 occurrences dans SUD_French-GSD).
```
pattern{
V[upos=AUX|VERB,VerbForm=Inf, !Subject, !InIdiom];
}
commands{
V.Subject=SubjRaising
}