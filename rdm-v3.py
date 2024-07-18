#!/usr/bin/env python3
import numpy as np

def calcul_poutre_continue(longueurs_travees, charges):
    """
    Calcule les moments aux appuis et les réactions pour une poutre continue.
    Les moments sont considérés nuls uniquement aux extrémités.
    
    :param longueurs_travees: Liste des longueurs de chaque travée
    :param charges: Liste des charges uniformément réparties sur chaque travée
    :return: Tuple contenant les moments aux appuis et les réactions
    """
    n_travees = len(longueurs_travees)
    n_appuis = n_travees + 1
    
    # Matrice de rigidité et vecteur de charge
    K = np.zeros((n_appuis-2, n_appuis-2))
    F = np.zeros(n_appuis-2)
    
    for i in range(n_travees-1):
        L1 = longueurs_travees[i]
        L2 = longueurs_travees[i+1]
        q1 = charges[i]
        q2 = charges[i+1]
        
        if i > 0:
            K[i-1, i] += 2 / L1
            K[i, i-1] += 2 / L1
        
        K[i, i] += 4 / L1 + 4 / L2
        
        if i < n_travees-2:
            K[i, i+1] += 2 / L2
            K[i+1, i] += 2 / L2
        
        F[i] += q1 * L1 / 2 + q2 * L2 / 2
    
    # Résolution pour les moments aux appuis intermédiaires
    M_intermediaires = np.linalg.solve(K, F)
    
    # Ajout des moments nuls aux extrémités
    moments = np.zeros(n_appuis)
    moments[1:-1] = M_intermediaires
    
    # Calcul des réactions
    reactions = np.zeros(n_appuis)
    for i in range(n_travees):
        L = longueurs_travees[i]
        q = charges[i]
        M_gauche = moments[i]
        M_droite = moments[i+1]
        
        reactions[i] += q * L / 2 + (M_gauche - M_droite) / L
        reactions[i+1] += q * L / 2 + (M_droite - M_gauche) / L
    
    return moments, reactions

# Exemple d'utilisation
longueurs_travees = [2, 5, 3, 6]  # mètres
charges = [1, 2, 1, 3]  # kN/m

moments, reactions = calcul_poutre_continue(longueurs_travees, charges)

print("Moments aux appuis (kN·m):")
for i, m in enumerate(moments):
    print(f"Appui {i+1}: {m:.2f}")

print("\nRéactions aux appuis (kN):")
for i, r in enumerate(reactions):
    print(f"Appui {i+1}: {r:.2f}")