#!/usr/bin/env python3
import numpy as np

def calcul_poutre_continue(longueur_totale, longueurs_travees, charges):
    """
    Calcule les moments et réactions pour une poutre continue avec des détails supplémentaires.
    """
    n_travees = len(longueurs_travees)
    n_appuis = n_travees + 1

    # Vérification des données d'entrée
    if abs(sum(longueurs_travees) - longueur_totale) > 1e-6:
        raise ValueError("La somme des longueurs des travées ne correspond pas à la longueur totale de la poutre.")
    if len(charges) != n_travees:
        raise ValueError("Le nombre de charges doit correspondre au nombre de travées.")

    # Calcul des moments d'encastrement parfait
    AEM = [q * L**2 / 12 for q, L in zip(charges, longueurs_travees)]
    print("Moments d'encastrement parfait:", AEM)

    # Construction de la matrice des coefficients et du vecteur des termes constants
    A = np.zeros((n_appuis-2, n_appuis-2))
    B = np.zeros(n_appuis-2)

    for i in range(n_appuis-2):
        if i > 0:
            A[i, i-1] = longueurs_travees[i]
        A[i, i] = 2 * (longueurs_travees[i] + longueurs_travees[i+1])
        if i < n_appuis-3:
            A[i, i+1] = longueurs_travees[i+1]
        B[i] = -6 * (AEM[i] + AEM[i+1])

    print("Matrice A:")
    print(A)
    print("Vecteur B:", B)

    # Résolution du système d'équations
    moments_intermediaires = np.linalg.solve(A, B)
    moments = np.zeros(n_appuis)
    moments[1:-1] = moments_intermediaires

    print("Moments intermédiaires:", moments_intermediaires)

    # Calcul des réactions
    reactions = np.zeros(n_appuis)
    for i in range(n_appuis):
        if i == 0:
            reactions[i] = charges[0] * longueurs_travees[0] / 2 + (moments[1] - moments[0]) / longueurs_travees[0]
        elif i == n_appuis - 1:
            reactions[i] = charges[-1] * longueurs_travees[-1] / 2 + (moments[-2] - moments[-1]) / longueurs_travees[-1]
        else:
            reactions[i] = (charges[i-1] * longueurs_travees[i-1] + charges[i] * longueurs_travees[i]) / 2 + \
                           (moments[i-1] - moments[i]) / longueurs_travees[i-1] + \
                           (moments[i+1] - moments[i]) / longueurs_travees[i]

    return moments, reactions

# Exemple d'utilisation
longueur_totale = 16  # mètres
longueurs_travees = [2, 5, 3, 6]  # mètres
charges = [1, 2, 1, 3]  # kN/m

moments, reactions = calcul_poutre_continue(longueur_totale, longueurs_travees, charges)

print("Moments aux appuis (kN·m):", moments)
print("Réactions aux appuis (kN):", reactions)