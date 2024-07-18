#!/usr/bin/env python3
import numpy as np

def get_input_data():
    num_travees = int(input("Entrez le nombre de travées : "))
    longueurs = []
    charges = []
    for i in range(1, num_travees + 1):
        longueur = float(input(f"Entrez la longueur de la travée {i} (en m) : "))
        charge = float(input(f"Entrez la charge uniformément répartie sur la travée {i} (en kN/m) : "))
        longueurs.append(longueur)
        charges.append(charge)
    return num_travees, longueurs, charges

def calculer_moments(num_travees, longueurs, charges):
    EI = 1  # On suppose que EI est constant et égal à 1 pour simplifier les calculs
    moments = [0] * (num_travees + 1)
    
    # Construction du système d'équations
    A = [[0 for _ in range(num_travees + 1)] for _ in range(num_travees + 1)]
    B = [0] * (num_travees + 1)
    
    for i in range(1, num_travees):
        Li = longueurs[i - 1]
        Li1 = longueurs[i]
        qi = charges[i - 1]
        qi1 = charges[i]
        
        A[i][i - 1] = Li
        A[i][i] = 2 * (Li + Li1)
        A[i][i + 1] = Li1
        
        B[i] = 6 * ((qi1 * Li1**2 / 24) + (qi * Li**2 / 24))
    
    # Appliquer les conditions aux limites pour rendre la matrice inversible
    A[0][0] = 1
    A[-1][-1] = 1
    
    # Résolution du système d'équations
    A = np.array(A)
    B = np.array(B)
    moments = np.linalg.solve(A, B)
    
    return moments

def main():
    num_travees, longueurs, charges = get_input_data()
    moments = calculer_moments(num_travees, longueurs, charges)
    print("Moments aux appuis (kN.m):")
    for i, moment in enumerate(moments):
        print(f"Appui {i}: {moment:.2f} kN.m")

if __name__ == "__main__":
    main()