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
    
    # Calculer d'abord tous les THETA0* sans DeltaTheta
    for i in range(n + 1):
        if i == 0:
            results.append({
                'x': 'x0',
                'Abs': abs_cumul,
                'L': '-',
                'q': '-',
                'MT0': '-',
                'THETA0*': '-',
                'THETA0**': '-',
                'DeltaTheta': '-'
            })
        else:
            MT0 = q[i-1] * L[i-1]**2 / 8
            theta_0_star = -q[i-1] * L[i-1]**3 / 24
            theta_0_star_star = -theta_0_star
            abs_cumul += L[i-1]
            
            results.append({
                'x': f'x{i}',
                'Abs': abs_cumul,
                'L': L[i-1],
                'q': q[i-1],
                'MT0': MT0,
                'THETA0*': theta_0_star,
                'THETA0**': theta_0_star_star,
                'DeltaTheta': '-'  # Sera calculé dans la prochaine étape
            })
    
    # Calculer DeltaTheta
    for i in range(len(results) - 1):
        if i == 0:
            results[i]['DeltaTheta'] = '-'
        else:
            delta_theta = 6 * (results[i+1]['THETA0*'] - results[i]['THETA0**'])
            results[i]['DeltaTheta'] = delta_theta
    
    return results

def print_results(results):
    print("\nAbs     L       q     MT0    THETA0*   THETA0**  DeltaTheta")
    print("        m     kN/m   kN.m   kN.m x EI  kN.m x EI  kN.m x EI")
    for r in results:
        if r['x'] == 'x0':
            print(f"{r['x']:<4} {r['Abs']:<7.2f} {r['L']:<7} {r['q']:<7} {r['MT0']:<7} {r['THETA0*']:<9} {r['THETA0**']:<9} {r['DeltaTheta']:<9}")
        else:
            print(f"{r['x']:<4} {r['Abs']:<7.2f} {r['L']:<7.2f} {r['q']:<7.2f} {r['MT0']:<7.2f} {r['THETA0*']:<9.2f} {r['THETA0**']:<9.2f} {r['DeltaTheta']:<9}")

def main():
    n, L, q = get_input()
    results = calculate_beam_properties(n, L, q)
    print_results(results)

if __name__ == "__main__":
    main()