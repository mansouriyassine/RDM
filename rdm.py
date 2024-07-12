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

def affichage_resultats(moments, longueurs):
    plt.figure(figsize=(12, 6))
    offset = 0
    for i, (x, M) in enumerate(moments):
        plt.plot(x + offset, M, label=f'Travée {i+1}')
        offset += longueurs[i]
    
    plt.title('Diagramme des moments de flexion')
    plt.xlabel('Position le long de la poutre (m)')
    plt.ylabel('Moment de flexion (kN.m)')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    n_travees, longueurs, charges = saisie_donnees()
    A, B = calcul_matrices(n_travees, longueurs, charges)
    moments_appuis = resolution_systeme(A, B)
    moments = calcul_moments(n_travees, longueurs, charges, moments_appuis)
    
    print("\nMoments aux appuis :")
    for i, moment in enumerate(moments_appuis):
        print(f"Appui {i+1}: {moment:.2f} kN.m")
    
    affichage_resultats(moments, longueurs)

if __name__ == "__main__":
    main()