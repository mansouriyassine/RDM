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
    
    MT0 = []
    theta0_star = []
    theta0_double_star = []
    
    for i in range(num_travees):
        Li = longueurs[i]
        qi = charges[i]
        
        # Moment de travée dû aux charges uniformément réparties
        MT0.append(qi * Li**2 / 8)
        
        # Calcul des rotations
        if i == 0:
            theta0_star.append(-MT0[-1] / (EI * Li))
            theta0_double_star.append(MT0[-1] / (EI * Li))
        else:
            Li_prev = longueurs[i - 1]
            MT0_prev = MT0[-2]
            
            theta0_star.append(-MT0[-1] / (EI * Li))
            theta0_double_star.append(MT0[-1] / (EI * Li))
    
    # Construction du système d'équations
    A = [[0 for _ in range(num_travees + 1)] for _ in range(num_travees + 1)]
    B = [0] * (num_travees + 1)
    
    for i in range(1, num_travees):
        Li = longueurs[i - 1]
        Li1 = longueurs[i]
        
        A[i][i - 1] = Li
        A[i][i] = 2 * (Li + Li1)
        A[i][i + 1] = Li1
        
        B[i] = 6 * (theta0_double_star[i] - theta0_star[i])
    
    # Appliquer les conditions aux limites pour rendre la matrice inversible
    A[0][0] = 1
    A[-1][-1] = 1
    
    # Résolution du système d'équations
    A = np.array(A)
    B = np.array(B)
    moments = np.linalg.solve(A, B)
    
    return moments, MT0, theta0_star, theta0_double_star

def main():
    num_travees, longueurs, charges = get_input_data()
    moments, MT0, theta0_star, theta0_double_star = calculer_moments(num_travees, longueurs, charges)
    
    print("Moments aux appuis (kN.m):")
    for i, moment in enumerate(moments):
        print(f"Appui {i}: {moment:.2f} kN.m")
    
    print("\nDétails des calculs intermédiaires :")
    for i in range(num_travees):
        print(f"Travée {i+1} : L = {longueurs[i]:.2f} m, q = {charges[i]:.2f} kN/m")
        print(f"  MT0 = {MT0[i]:.2f} kN.m")
        print(f"  θ0* = {theta0_star[i]:.2f}")
        print(f"  θ0** = {theta0_double_star[i]:.2f}")

if __name__ == "__main__":
    main()