#!/usr/bin/env python3
from flask import Flask, render_template, request, send_file
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

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

    for i in range(1, len(results)):
        results[i]['DeltaTheta'] = 6 * (results[i]['THETA0*'] - results[i-1]['THETA0**'])

    return results

def calculate_support_moments(results):
    n = len(results) - 2

    A = np.zeros((n, n))
    for i in range(n):
        if i > 0:
            A[i, i-1] = results[i+1]['L']
        A[i, i] = 2 * (results[i+1]['L'] + results[i+2]['L'])
        if i < n-1:
            A[i, i+1] = results[i+2]['L']

    A_inv = np.linalg.inv(A)

    b = np.array([results[i+1]['DeltaTheta'] for i in range(1, n+1)])

    moments = np.dot(A_inv, b)

    for i in range(len(results)):
        if i == 0 or i == len(results) - 1:
            results[i]['Ma'] = 0
        else:
            results[i]['Ma'] = moments[i-1]

    return results

def calculate_span_moments(results):
    for i in range(1, len(results)):
        x = np.linspace(0, results[i]['L'], 100)
        M_left = results[i-1]['Ma']
        M_right = results[i]['Ma']
        q = results[i]['q']
        L = results[i]['L']
        
        M = M_left + (M_right - M_left) * x / L - q * x * (L - x) / 2
        
        results[i]['span_x'] = x + results[i-1]['Abs']
        results[i]['span_M'] = M
    
    return results

def plot_moments(results):
    plt.figure(figsize=(12, 6))
    
    # Tracer les moments aux appuis
    x_supports = [r['Abs'] for r in results]
    y_supports = [r['Ma'] for r in results]
    plt.plot(x_supports, y_supports, 'bo-', label='Moments aux appuis')
    
    # Tracer les moments en travées
    for i in range(1, len(results)):
        plt.plot(results[i]['span_x'], results[i]['span_M'], 'r-')
    
    plt.xlabel('Position sur la poutre (m)')
    plt.ylabel('Moment fléchissant (kN.m)')
    plt.title('Diagramme des moments fléchissants')
    plt.grid(True)
    plt.legend()
    
    # Annotations pour les moments aux appuis
    for i, (xi, yi) in enumerate(zip(x_supports, y_supports)):
        plt.annotate(f'{yi:.2f}', (xi, yi), textcoords="offset points", xytext=(0,10), ha='center')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

@app.route('/')
def home():
    return render_template('accueil.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    n = int(request.form['n'])
    L = [float(request.form[f'L{i}']) for i in range(n)]
    q = [float(request.form[f'q{i}']) for i in range(n)]

    results = calculate_beam_properties(n, L, q)
    results = calculate_support_moments(results)
    results = calculate_span_moments(results)

    app.results = results  # Stocke les résultats pour la génération du graphique

    return render_template('resultats.html', results=results, n=n)

@app.route('/get_plot')
def get_plot():
    img = plot_moments(app.results)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)