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

def calculate_beam_properties(n, L, q):
    results = []
    abs_cumul = 0
    
    for i in range(n):
        MT0 = q[i] * L[i]**2 / 8
        theta_0_star = -q[i] * L[i]**3 / 24
        
        results.append({
            'Abs': abs_cumul,
            'L': L[i],
            'q': q[i],
            'MT0': MT0,
            'THETA0*': theta_0_star
        })
        
        abs_cumul += L[i]
    
    return results

def print_results(results):
    print("\nAbs   L     q    MT0    THETA0*")
    print("                  kN.m   kN.m x EI")
    for r in results:
        print(f"{r['Abs']:<5.2f} {r['L']:<5.2f} {r['q']:<5.2f} {r['MT0']:<6.2f} {r['THETA0*']:<9.2f}")

def main():
    n, L, q = get_input()
    results = calculate_beam_properties(n, L, q)
    print_results(results)

if __name__ == "__main__":
    main()