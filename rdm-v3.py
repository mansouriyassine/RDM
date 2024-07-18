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
    A = np.zeros((n-1, n-1))
    b = np.zeros(n-1)
    
    for i in range(n-1):
        if i > 0:
            A[i, i-1] = L[i]
        A[i, i] = 2 * (L[i] + L[i+1])
        if i < n-2:
            A[i, i+1] = L[i+1]
        
        b[i] = 6 * (q[i+1]*L[i+1]**3/24 - q[i]*L[i]**3/24)
    
    M = np.linalg.solve(A, b)
    M = np.insert(M, 0, 0)
    M = np.append(M, 0)
    
    return M

def calculate_beam_properties(n, L, q, M):
    results = []
    abs_cumul = 0
    
    for i in range(n):
        MT0 = q[i] * L[i]**2 / 8  # Modification ici
        q0_star = M[i+1]
        q0_double_star = M[i]  # Modification ici
        x0 = L[i] / 2
        Ma = M[i] + (M[i+1] - M[i]) / 2 + q[i] * L[i]**2 / 8
        theta_0 = -q[i] * L[i]**3 / 24
        
        results.append({
            'Abs': abs_cumul,
            'L': L[i],
            'q': q[i],
            'MT0': MT0,
            'q0*': q0_star,
            'q0**': q0_double_star,
            'Ma': Ma,
            'x0': x0,
            'θ0': theta_0
        })
        
        abs_cumul += L[i]
    
    return results

def print_results(results):
    print("\nAbs   L     q    MT0    q0*    q0**   Ma     x0    θ0                        -   KN.m x EI")
    for r in results:
        print(f"{r['Abs']:<5.2f} {r['L']:<5.2f} {r['q']:<5.2f} {r['MT0']:<6.2f} {r['q0*']:<7.2f} {r['q0**']:<7.2f} {r['Ma']:<7.2f} {r['x0']:<6.2f} {r['θ0']:<7.2f}")

def main():
    n, L, q = get_input()
    M = solve_continuous_beam(n, L, q)
    results = calculate_beam_properties(n, L, q, M)
    print_results(results)

if __name__ == "__main__":
    main()