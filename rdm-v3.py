#!/usr/bin/env python3
import numpy as np

def saisie_donnees():
    n_travees = int(input("Entrez le nombre de travées : "))
    longueurs = []
    charges = []
    for i in range(n_travees):
        longueurs.append(float(input(f"Entrez la longueur de la travée {i+1} (en m) : ")))
        charges.append(float(input(f"Entrez la charge uniformément répartie sur la travée {i+1} (en kN/m) : ")))
    return n_travees, longueurs, charges

def calcul_trois_moments(n_travees, longueurs, charges):
    n_appuis = n_travees + 1
    A = np.zeros((n_appuis, n_appuis))
    B = np.zeros(n_appuis)
    
    for i in range(1, n_travees):
        L1, L2 = longueurs[i-1], longueurs[i]
        q1, q2 = charges[i-1], charges[i]
        A[i, i-1] = L1
        A[i, i] = 2 * (L1 + L2)
        A[i, i+1] = L2
        B[i] = -(q1 * L1**3 / 6 + q2 * L2**3 / 6)
    
    A[0, 0] = A[-1, -1] = 1
    
    return A, B

def resolution_systeme(A, B):
    return np.linalg.solve(A, B)

def affichage_resultats(longueurs, moments_appuis):
    print("\nMoments aux appuis (kN.m):")
    abs_cumul = 0
    for i, L in enumerate(longueurs):
        print(f"Appui {i}: x = {abs_cumul:.2f} m, M = {moments_appuis[i]:.2f}")
        abs_cumul += L
    print(f"Appui {len(longueurs)}: x = {abs_cumul:.2f} m, M = {moments_appuis[-1]:.2f}")

def main():
    n_travees, longueurs, charges = saisie_donnees()
    A, B = calcul_trois_moments(n_travees, longueurs, charges)
    moments_appuis = resolution_systeme(A, B)
    affichage_resultats(longueurs, moments_appuis)

if __name__ == "__main__":
    main()