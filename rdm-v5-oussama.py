#!/usr/bin/env python3
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Utiliser un backend non-interactif
import matplotlib.pyplot as plt

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
        'L': 0,
        'q': 0,
        'MT0': 0,
        'THETA0*': 0,
        'THETA0**': 0,
        'DeltaTheta': 0,
        'Ma': 0
    })
    
    for i in range(n):
        MT0 = q[i] * L[i]**2 / 8
        theta_0_star = -q[i] * L[i]**3 / 24
        theta_0_star_star = -theta_0_star
        abs_cumul += L[i]
        
        results.append({
            'x': f'x{i+1}',
            'Abs': abs_cumul,
            'L': L[i],
            'q': q[i],
            'MT0': MT0,
            'THETA0*': theta_0_star,
            'THETA0**': theta_0_star_star,
            'DeltaTheta': 0,
            'Ma': 0
        })
    
    # Calculer DeltaTheta
    for i in range(1, len(results)):
        results[i]['DeltaTheta'] = 6 * (results[i]['THETA0*'] - results[i-1]['THETA0**'])
    
    return results

def calculate_support_moments(results):
    n = len(results) - 2  # nombre d'équations (nombre d'appuis intérieurs)
    
    # Construire la matrice A
    A = np.zeros((n, n))
    for i in range(n):
        if i > 0:
            A[i, i-1] = results[i+1]['L']
        A[i, i] = 2 * (results[i+1]['L'] + results[i+2]['L'])
        if i < n-1:
            A[i, i+1] = results[i+2]['L']
    
    print("\nMatrice de rigidité:")
    print(A)
    
    # Calculer l'inverse de A
    A_inv = np.linalg.inv(A)
    print("\nMatrice inverse:")
    print(A_inv)
    
    # Construire le vecteur b (DeltaTheta)
    b = np.array([results[i+1]['DeltaTheta'] for i in range(1, n+1)])
    print("\nVecteur DeltaTheta:")
    print(b)
    
    # Calculer les moments
    moments = np.dot(A_inv, b)
    print("\nMoments aux appuis (Ma) calculés:")
    print(moments)
    
    # Ajouter les moments aux résultats
    for i in range(len(results)):
        if i == 0 or i == len(results) - 1:
            results[i]['Ma'] = 0  # Moment nul aux appuis d'extrémité
        else:
            results[i]['Ma'] = moments[i-1]
    
    return results

def print_results(results):
    print("\nAbs     L       q       MT0      THETA0*     THETA0**    DeltaTheta   Ma")
    print("        m     kN/m     kN.m     kN.m x EI   kN.m x EI    kN.m x EI   kN.m")
    for r in results:
        if r['x'] == 'x0':
            print(f"{r['x']:<4} {r['Abs']:<7.2f} {'-':<7} {'-':<7} {'-':<9} {'-':<11} {'-':<11} {'-':<11} {r['Ma']:.2f}")
        else:
            print(f"{r['x']:<4} {r['Abs']:<7.2f} {r['L']:<7.2f} {r['q']:<7.2f} {r['MT0']:<9.2f} {r['THETA0*']:<11.2f} {r['THETA0**']:<11.2f} {r['DeltaTheta']:<11.2f} {r['Ma']:.2f}")

def plot_moments(results):
    x = [r['Abs'] for r in results]
    y = [r['Ma'] for r in results]
    
    plt.figure(figsize=(12, 6))
    plt.plot(x, y, 'bo-')
    plt.xlabel('Position sur la poutre (m)')
    plt.ylabel('Moment fléchissant (kN.m)')
    plt.title('Diagramme des moments fléchissants')
    plt.grid(True)
    
    # Ajout des annotations pour chaque point
    for i, (xi, yi) in enumerate(zip(x, y)):
        plt.annotate(f'{yi:.2f}', (xi, yi), textcoords="offset points", xytext=(0,10), ha='center')
    
    # Sauvegarder le graphique au lieu de l'afficher
    plt.savefig('moments_flechissants.png')
    print("Le graphique a été sauvegardé sous le nom 'moments_flechissants.png'")

def main():
    n, L, q = get_input()
    results = calculate_beam_properties(n, L, q)
    results = calculate_support_moments(results)
    print_results(results)
    plot_moments(results)

if __name__ == "__main__":
    main()