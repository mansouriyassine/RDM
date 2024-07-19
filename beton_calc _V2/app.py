#!/usr/bin/env python3
from flask import Flask, render_template, request, send_file
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

def calculer_beton(resistance, type_utilisation, type_ciment, taille_max_agregats, type_sable, temperature, humidite, consistance):
    rapport_eau_ciment = 0.5 - (resistance - 20) * 0.01
    quantite_ciment = resistance * 10
    quantite_eau = quantite_ciment * rapport_eau_ciment
    quantite_sable = 650
    quantite_gros_agregats = 1100

    if temperature > 30:
        quantite_eau += 10
    if humidite < 50:
        quantite_eau += 5
    if type_sable == "fin":
        quantite_sable += 50
    if taille_max_agregats > 20:
        quantite_gros_agregats += 100

    if type_ciment == "cpj45":
        quantite_ciment *= 0.95
    elif type_ciment == "cpa55":
        quantite_ciment *= 0.9

    classes_consistance = {
        "ferme": "S1",
        "plastique": "S2",
        "très plastique": "S3",
        "fluide": "S4"
    }
    classe_consistance = classes_consistance.get(consistance, "S2")

    temps_malaxage = 90
    if taille_max_agregats > 20:
        temps_malaxage += 30
    
    duree_prise = 6
    if temperature > 30:
        duree_prise -= 1
    elif temperature < 10:
        duree_prise += 2

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

    return render_template('resultats.html', resultat=resultat, form_data=request.form)

@app.route('/telecharger_pdf')
def telecharger_pdf():
    resistance = float(request.args.get('resistance'))
    type_utilisation = request.args.get('type_utilisation')
    type_ciment = request.args.get('type_ciment')
    taille_max_agregats = float(request.args.get('taille_max_agregats'))
    type_sable = request.args.get('type_sable')
    temperature = float(request.args.get('temperature'))
    humidite = float(request.args.get('humidite'))
    consistance = request.args.get('consistance')

    resultat = calculer_beton(
        resistance, type_utilisation, type_ciment, taille_max_agregats,
        type_sable, temperature, humidite, consistance
    )

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Résultats du calcul de mélange de béton")
    p.setFont("Helvetica", 12)

    y = 700
    for key, value in resultat.items():
        p.drawString(50, y, f"{key}: {value}")
        y -= 20

    p.setFillColorRGB(1, 0, 0)
    p.drawString(50, y-40, "Attention: Ces résultats sont basés sur des calculs simplifiés")
    p.drawString(50, y-60, "et ne remplacent pas l'expertise d'un professionnel.")

    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='resultats_beton.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)