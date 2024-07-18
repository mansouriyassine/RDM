#!/usr/bin/env python3
import numpy as np

def calculate_moments(spans, loads):
    n = len(spans)
    
    # Calcul des coefficients de la méthode de Clapeyron
    a = [0] + [spans[i-1] / 6 for i in range(1, n)] + [0]
    b = [spans[i] / 3 for i in range(n)]
    c = [0] + [spans[i] / 6 for i in range(n-1)] + [0]
    
    # Calcul des charges équivalentes
    q = [-loads[i] * spans[i]**2 / 12 for i in range(n)]
    
    # Construction de la matrice tridiagonale
    A = np.zeros((n, n))
    for i in range(n):
        A[i, i] = b[i]
        if i > 0:
            A[i, i-1] = a[i]
        if i < n-1:
            A[i, i+1] = c[i]
    
    # Conditions aux limites (appuis simples aux extrémités)
    A[0, 0] = A[n-1, n-1] = 1
    
    # Résolution du système d'équations
    moments = np.linalg.solve(A, q)
    
    return moments

def main():
    n = int(input("Entrez le nombre de travées : "))
    spans = []
    loads = []
    
    for i in range(n):
        span = float(input(f"Entrez la longueur de la travée {i+1} (en m) : "))
        load = float(input(f"Entrez la charge uniformément répartie sur la travée {i+1} (en kN/m) : "))
        spans.append(span)
        loads.append(load)
    
    moments = calculate_moments(spans, loads)
    
    print("\nMoments aux appuis (en kN·m) :")
    for i, moment in enumerate(moments):
        print(f"Appui {i}: {moment:.2f}")

if __name__ == "__main__":
    main()