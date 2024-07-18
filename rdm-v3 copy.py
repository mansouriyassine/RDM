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
    
    results.append({
        'x': 'x0',
        'Abs': abs_cumul,
        'L': '-',
        'q': '-',
        'MT0': '-',
        'THETA0*': '-',
        '6ΔΘ0': '-'
    })
    
    for i in range(n):
        MT0 = q[i] * L[i]**2 / 8
        theta_0_star = -q[i] * L[i]**3 / 24
        
        abs_cumul += L[i]
        
        results.append({
            'x': f'x{i+1}',
            'Abs': abs_cumul,
            'L': L[i],
            'q': q[i],
            'MT0': MT0,
            'THETA0*': theta_0_star,
            '6ΔΘ0': None  # Sera calculé après
        })
    
    # Calculer 6ΔΘ0
    for i in range(1, len(results)-1):
        delta_theta = 6 * (results[i+1]['THETA0*'] - results[i]['THETA0*'])
        results[i]['6ΔΘ0'] = delta_theta
    
    return results

def print_results(results):
    print("\nAbs     L       q     MT0    THETA0*   6ΔΘ0")
    print("        m     kN/m   kN.m   kN.m x EI  kN.m x EI")
    for r in results:
        if r['x'] == 'x0':
            print(f"{r['x']:<4} {r['Abs']:<7.2f} {r['L']:<7} {r['q']:<7} {r['MT0']:<7} {r['THETA0*']:<9} {r['6ΔΘ0']:<9}")
        else:
            delta_theta = r['6ΔΘ0']
            delta_theta_str = f"{delta_theta:.2f}" if delta_theta is not None else "-"
            print(f"{r['x']:<4} {r['Abs']:<7.2f} {r['L']:<7.2f} {r['q']:<7.2f} {r['MT0']:<7.2f} {r['THETA0*']:<9.2f} {delta_theta_str:<9}")

def main():
    n, L, q = get_input()
    results = calculate_beam_properties(n, L, q)
    print_results(results)

if __name__ == "__main__":
    main()