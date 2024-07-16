#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

def saisie_donnees():
    n_travees = int(input("Entrez le nombre de travées : "))
    longueurs = []
    charges = []
    for i in range(n_travees):
        longueurs.append(float(input(f"Entrez la longueur de la travée {i+1} (en m) : ")))
        charges.append(float(input(f"Entrez la charge uniformément répartie sur la travée {i+1} (en kN/m) : ")))
    return n_travees, longueurs, charges

def calcul_matrices(n_travees, longueurs, charges):
    n_appuis = n_travees + 1
    A = np.zeros((n_appuis, n_appuis))
    B = np.zeros(n_appuis)
    for i in range(1, n_travees):
        L1, L2 = longueurs[i-1], longueurs[i]
        q1, q2 = charges[i-1], charges[i]
        A1 = (q1 * L1**3) / 24
        A2 = (q2 * L2**3) / 24
        A[i, i-1] = L1
        A[i, i] = 2 * (L1 + L2)
        A[i, i+1] = L2
        B[i] = 6 * (A1 / L1 + A2 / L2)
    # Conditions aux limites : moments nuls aux extrémités pour une poutre simplement appuyée
    A[0, 0] = A[-1, -1] = 1
    return A, B

def resolution_systeme(A, B):
    return np.linalg.solve(A, B)

def calcul_moments(n_travees, longueurs, charges, moments_appuis):
    moments = []
    for i in range(n_travees):
        L = longueurs[i]
        q = charges[i]
        M1, M2 = moments_appuis[i], moments_appuis[i+1]
        x = np.linspace(0, L, 100)
        M = M1 * (1 - x/L) + M2 * (x/L) + (q*x/2) * (L - x)
        moments.append((x, M))
    return moments

def calcul_efforts_tranchants(n_travees, longueurs, charges, moments_appuis):
    efforts_tranchants = []
    for i in range(n_travees):
        L = longueurs[i]
        q = charges[i]
        M1, M2 = moments_appuis[i], moments_appuis[i+1]
        x = np.linspace(0, L, 100)
        V = (M2 - M1) / L + q * (L/2 - x)
        efforts_tranchants.append((x, V))
    return efforts_tranchants

def affichage_resultats(moments, efforts_tranchants, longueurs):
    plt.figure(figsize=(12, 10))

    # Diagramme des moments de flexion
    plt.subplot(2, 1, 1)
    offset = 0
    for i, (x, M) in enumerate(moments):
        plt.plot(x + offset, M, label=f'Travée {i+1}')
        offset += longueurs[i]
    plt.title('Diagramme des moments de flexion')
    plt.xlabel('Position le long de la poutre (m)')
    plt.ylabel('Moment de flexion (kN.m)')
    plt.legend()
    plt.grid(True)

    # Diagramme des efforts tranchants
    plt.subplot(2, 1, 2)
    offset = 0
    for i, (x, V) in enumerate(efforts_tranchants):
        plt.plot(x + offset, V, label=f'Travée {i+1}')
        offset += longueurs[i]
    plt.title('Diagramme des efforts tranchants')
    plt.xlabel('Position le long de la poutre (m)')
    plt.ylabel('Effort tranchant (kN)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('diagrammes.png')
    print("Graphique sauvegardé dans 'diagrammes.png'")
    plt.show()

def main():
    print("Début de l'exécution")
    n_travees, longueurs, charges = saisie_donnees()
    print("Données saisies")
    A, B = calcul_matrices(n_travees, longueurs, charges)
    print("Matrices calculées")
    moments_appuis = resolution_systeme(A, B)
    print("Système résolu")
    moments = calcul_moments(n_travees, longueurs, charges, moments_appuis)
    print("Moments calculés")
    efforts_tranchants = calcul_efforts_tranchants(n_travees, longueurs, charges, moments_appuis)
    print("Efforts tranchants calculés")

    print("\nMoments aux appuis :")
    for i, moment in enumerate(moments_appuis):
        print(f"Appui {i+1}: {moment:.2f} kN.m")

    print("Tentative d'affichage des résultats")
    try:
        affichage_resultats(moments, efforts_tranchants, longueurs)
        print("Affichage réussi")
    except Exception as e:
        print(f"Erreur lors de l'affichage : {e}")

if __name__ == "__main__":
    main()