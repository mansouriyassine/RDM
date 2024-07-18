#!/usr/bin/env python3
import numpy as np

def get_input():
    n = int(input("Entrez le nombre de travées : "))
    L = []
    q = []
    for i in range(n):
        L.append(float(input(f"Entrez la longueur de la travée {i+1} (en m) : ")))
        q.append(float(input(f"Entrez la charge uniformément répartie sur la travée {i+1} (en kN/m) : ")))
    return n, L, q

def solve_continuous_beam(n, L, q):
    # Création de la matrice A et du vecteur b
    A = np.zeros((n-1, n-1))
    b = np.zeros(n-1)
    
    for i in range(n-1):
        if i > 0:
            A[i, i-1] = L[i]
        A[i, i] = 2 * (L[i] + L[i+1])
        if i < n-2:
            A[i, i+1] = L[i+1]
        
        b[i] = 6 * (q[i+1]*L[i+1]**3/24 - q[i]*L[i]**3/24)
    
    # Résolution du système
    M = np.linalg.solve(A, b)
    
    # Ajout des moments nuls aux extrémités
    M = np.insert(M, 0, 0)
    M = np.append(M, 0)
    
    return M

def print_results(M):
    print("\nMoments aux appuis (kN.m) :")
    for i, m in enumerate(M):
        print(f"M{i} = {m:.2f}")

def main():
    n, L, q = get_input()
    M = solve_continuous_beam(n, L, q)
    print_results(M)

if __name__ == "__main__":
    main()