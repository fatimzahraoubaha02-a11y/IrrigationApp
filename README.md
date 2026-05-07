Application Python pour la gestion et l’optimisation de l’irrigation agricole

#Description
Ce projet implémente des méthodes d’optimisation de distribution de l’eau sur plusieurs parcelles agricoles.
Deux volets complémentaires sont intégrés :

#1. Partie Théorique (Programmation Linéaire)
Formulation du problème : définition d’une fonction objectif (minimisation de la consommation d’eau ou maximisation du rendement).

Contraintes : disponibilité de l’eau, capacité des parcelles, besoins spécifiques des cultures.

Méthodes utilisées :

Méthode graphique : résolution visuelle pour deux variables de décision.

Méthode du simplexe et dualité : résolution algorithmique pour des problèmes linéaires complexes.

Validation théorique : vérification de la cohérence et interprétation économique des contraintes.



#2. Partie Pratique (Application Python)
Implémentation : utilisation de bibliothèques Python (PuLP, NumPy, Matplotlib).

Fonctionnalités :

Résolution graphique pour 2 variables.

Résolution par simplexe pour plusieurs parcelles.

Comparaison et validation des résultats.

Manipulation : l’utilisateur peut définir ses propres données (quantité d’eau disponible, besoins des parcelles) et obtenir une solution optimale.
