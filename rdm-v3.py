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
    EI = float(input("Entrez la valeur de EI (kN.m²) : "))
    return n_travees, longueurs, charges, EI

def calcul_trois_moments(n_travees, longueurs, charges, EI):
    n_appuis = n_travees + 1
    A = np.zeros((n_appuis, n_appuis))
    B = np.zeros(n_appuis)
    
    # Calcul des termes intermédiaires
    MT0 = [q * L**2 / 8 for q, L in zip(charges, longueurs)]
    theta = [q * L**3 / (24 * EI) for q, L in zip(charges, longueurs)]
    
    # Construction du système d'équations
    for i in range(1, n_travees):
        L1, L2 = longueurs[i-1], longueurs[i]
        A[i, i-1] = L1
        A[i, i] = 2 * (L1 + L2)
        A[i, i+1] = L2
        B[i] = -6 * EI * (theta[i] / L2 + theta[i-1] / L1)
    
    # Conditions aux limites : moments nuls aux extrémités pour une poutre simplement appuyée
    A[0, 0] = A[-1, -1] = 1
    
    return A, B, MT0, theta

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

def calcul_position_moment_max(L, q, M1, M2):
    x_max = (L/2) - (M2 - M1) / (q * L)
    return min(max(x_max, 0), L)  # Assure que x_max est entre 0 et L

def affichage_resultats(longueurs, charges, moments_appuis, MT0, theta, EI):
    print("\nRésultats détaillés:")
    print("Abs\tL\tq\tMT0\tq0*\tq0**\tMa\tx")
    abs_cumul = 0
    for i in range(len(longueurs)):
        L = longueurs[i]
        q = charges[i]
        Ma = moments_appuis[i]
        x_max = calcul_position_moment_max(L, q, Ma, moments_appuis[i+1])
        q0 = 6 * EI * theta[i] / L**3
        print(f"{abs_cumul:.2f}\t{L:.2f}\t{q:.2f}\t{MT0[i]:.3f}\t{q0:.3f}\t{q0:.3f}\t{Ma:.2f}\t{x_max:.2f}")
        abs_cumul += L
    print(f"{abs_cumul:.2f}\t\t\t\t\t\t{moments_appuis[-1]:.2f}")

    # Affichage graphique
    plt.figure(figsize=(12, 6))
    offset = 0
    for i, (L, q) in enumerate(zip(longueurs, charges)):
        x = np.linspace(0, L, 100)
        M = moments_appuis[i] * (1 - x/L) + moments_appuis[i+1] * (x/L) + (q*x/2) * (L - x)
        plt.plot(x + offset, M, label=f'Travée {i+1}')
        
        x_max = calcul_position_moment_max(L, q, moments_appuis[i], moments_appuis[i+1])
        M_max = moments_appuis[i] * (1 - x_max/L) + moments_appuis[i+1] * (x_max/L) + (q*x_max/2) * (L - x_max)
        plt.plot(x_max + offset, M_max, 'ro')
        plt.text(x_max + offset, M_max, f'({x_max:.2f}, {M_max:.2f})', verticalalignment='bottom')
        
        offset += L
    
    plt.title('Diagramme des moments de flexion')
    plt.xlabel('Position le long de la poutre (m)')
    plt.ylabel('Moment de flexion (kN.m)')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    n_travees, longueurs, charges, EI = saisie_donnees()
    A, B, MT0, theta = calcul_trois_moments(n_travees, longueurs, charges, EI)
    moments_appuis = resolution_systeme(A, B)
    affichage_resultats(longueurs, charges, moments_appuis, MT0, theta, EI)

if __name__ == "__main__":
    main()