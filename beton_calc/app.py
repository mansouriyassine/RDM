#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def calculer_beton(resistance, type_utilisation, type_ciment, taille_max_agregats, type_sable, temperature, humidite, consistance):
    # Calculs simplifiés basés sur des formules empiriques
    rapport_eau_ciment = 0.5 - (resistance - 20) * 0.01
    quantite_ciment = resistance * 10
    quantite_eau = quantite_ciment * rapport_eau_ciment
    quantite_sable = 650
    quantite_gros_agregats = 1100

    # Ajustements basés sur les entrées
    if temperature > 30:
        quantite_eau += 10
    if humidite < 50:
        quantite_eau += 5
    if type_sable == "fin":
        quantite_sable += 50
    if taille_max_agregats > 20:
        quantite_gros_agregats += 100

    # Ajustements basés sur le type de ciment
    if type_ciment == "cpj45":
        quantite_ciment *= 0.95
    elif type_ciment == "cpa55":
        quantite_ciment *= 0.9

    # Calcul de la classe de consistance
    classes_consistance = {
        "ferme": "S1",
        "plastique": "S2",
        "très plastique": "S3",
        "fluide": "S4"
    }
    classe_consistance = classes_consistance.get(consistance, "S2")

    # Calcul du temps de malaxage et de la durée de prise
    temps_malaxage = 90  # secondes
    if taille_max_agregats > 20:
        temps_malaxage += 30
    
    duree_prise = 6  # heures
    if temperature > 30:
        duree_prise -= 1
    elif temperature < 10:
        duree_prise += 2

    # Résultats
    resultats = {
        "ciment": round(quantite_ciment, 2),
        "eau": round(quantite_eau, 2),
        "sable": round(quantite_sable, 2),
        "gros_agregats": round(quantite_gros_agregats, 2),
        "rapport_eau_ciment": round(rapport_eau_ciment, 2),
        "classe_consistance": classe_consistance,
        "dosage_minimal_ciment": max(300, round(quantite_ciment, 2)),
        "temps_malaxage": temps_malaxage,
        "duree_prise": duree_prise,
        "resistance_estimee_7j": round(resistance * 0.65, 2),
        "resistance_estimee_28j": resistance
    }

    return resultats

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/calculer', methods=['POST'])
def calculer():
    resistance = float(request.form['resistance'])
    type_utilisation = request.form['type_utilisation']
    type_ciment = request.form['type_ciment']
    taille_max_agregats = float(request.form['taille_max_agregats'])
    type_sable = request.form['type_sable']
    temperature = float(request.form['temperature'])
    humidite = float(request.form['humidite'])
    consistance = request.form['consistance']

    resultat = calculer_beton(
        resistance, type_utilisation, type_ciment, taille_max_agregats,
        type_sable, temperature, humidite, consistance
    )

    return render_template('resultats.html', resultat=resultat)

if __name__ == '__main__':
    app.run(debug=True)