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
    
    b = float(input("Entrez la largeur de la poutre (en m) : "))
    h = float(input("Entrez la hauteur de la poutre (en m) : "))
    d = float(input("Entrez la hauteur utile de la poutre (en m) : "))
    fc28 = float(input("Entrez la résistance caractéristique du béton à 28 jours (en MPa) : "))
    fe = float(input("Entrez la limite d'élasticité de l'acier (en MPa) : "))
    
    return n_travees, longueurs, charges, b, h, d, fc28, fe

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

def calcul_armatures_bael(moments, efforts_tranchants, b, h, d, fc28, fe):
    gamma_b, gamma_s = 1.5, 1.15
    fbu = 0.85 * fc28 / gamma_b
    sigma_s = fe / gamma_s

    armatures = []
    for moment, effort in zip(moments, efforts_tranchants):
        x, M = moment
        _, V = effort
        Mu = np.max(np.abs(M))
        z = 0.9 * d
        As = Mu / (sigma_s * z)
        Vu = np.max(np.abs(V))
        tau_u = Vu / (b * d)
        tau_lim = min(0.2 * fbu, 5)
        At_s = 0
        if tau_u > tau_lim:
            At_s = (tau_u - tau_lim) * b / (0.9 * fe / gamma_s)
        armatures.append((As, At_s))

    return armatures

def affichage_resultats(moments, efforts_tranchants, longueurs, armatures, b, h):
    plt.figure(figsize=(15, 15))

    # Diagramme des moments de flexion
    plt.subplot(3, 1, 1)
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
    plt.subplot(3, 1, 2)
    offset = 0
    for i, (x, V) in enumerate(efforts_tranchants):
        plt.plot(x + offset, V, label=f'Travée {i+1}')
        offset += longueurs[i]
    plt.title('Diagramme des efforts tranchants')
    plt.xlabel('Position le long de la poutre (m)')
    plt.ylabel('Effort tranchant (kN)')
    plt.legend()
    plt.grid(True)

    # Schéma des armatures
    plt.subplot(3, 1, 3)
    offset = 0
    for i, (As, At_s) in enumerate(armatures):
        L = longueurs[i]
        # Représentation de la poutre
        plt.fill_between([offset, offset+L], [-h/2, -h/2], [h/2, h/2], color='lightgray')
        
        # Armatures longitudinales
        plt.plot([offset, offset+L], [-h/2+0.05, -h/2+0.05], 'r-', linewidth=2)
        plt.plot([offset, offset+L], [h/2-0.05, h/2-0.05], 'r-', linewidth=2)
        
        # Armatures transversales (simplifiées)
        for x in np.linspace(offset, offset+L, num=int(L/0.2)):
            plt.plot([x, x], [-h/2+0.05, h/2-0.05], 'r-', linewidth=1)
        
        # Annotations
        plt.text(offset+L/2, 0, f'As={As*1e4:.2f}cm²\nAt/s={At_s*1e4:.2f}cm²/m', 
                 ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        offset += L

    plt.title('Schéma des armatures')
    plt.xlabel('Position le long de la poutre (m)')
    plt.ylabel('Hauteur de la poutre (m)')
    plt.ylim(-h, h)
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('resultats_poutre.png')
    print("Résultats sauvegardés dans 'resultats_poutre.png'")
    plt.show()

def main():
    print("Début de l'exécution")
    n_travees, longueurs, charges, b, h, d, fc28, fe = saisie_donnees()
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

    armatures = calcul_armatures_bael(moments, efforts_tranchants, b, h, d, fc28, fe)
    print("Armatures calculées")

    print("Tentative d'affichage des résultats")
    try:
        affichage_resultats(moments, efforts_tranchants, longueurs, armatures, b, h)
        print("Affichage réussi")
    except Exception as e:
        print(f"Erreur lors de l'affichage : {e}")

if __name__ == "__main__":
    main()