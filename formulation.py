#!/usr/bin/env python3
def obtenir_entree_numerique(prompt, min_val=None, max_val=None):
    while True:
        try:
            valeur = float(input(prompt))
            if (min_val is None or valeur >= min_val) and (max_val is None or valeur <= max_val):
                return valeur
            else:
                print(f"Veuillez entrer une valeur entre {min_val} et {max_val}.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def obtenir_entree_texte(prompt, options):
    while True:
        valeur = input(prompt).lower()
        if valeur in options:
            return valeur
        print(f"Veuillez choisir parmi : {', '.join(options)}")

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
        "ciment (kg/m³)": round(quantite_ciment, 2),
        "eau (litres/m³)": round(quantite_eau, 2),
        "sable (kg/m³)": round(quantite_sable, 2),
        "gros_agregats (kg/m³)": round(quantite_gros_agregats, 2),
        "rapport_eau_ciment": round(rapport_eau_ciment, 2),
        "classe_consistance": classe_consistance,
        "dosage_minimal_ciment (kg/m³)": max(300, round(quantite_ciment, 2)),
        "temps_malaxage (secondes)": temps_malaxage,
        "duree_prise (heures)": duree_prise,
        "resistance_estimee_7j (MPa)": round(resistance * 0.65, 2),
        "resistance_estimee_28j (MPa)": resistance
    }

    return resultats

# Programme principal
print("Bienvenue dans BétonCalc - Calculateur de mélange de béton")
print("Veuillez entrer les informations suivantes :")

resistance = obtenir_entree_numerique("Résistance à la compression souhaitée (MPa, entre 20 et 50) : ", 20, 50)
type_utilisation = obtenir_entree_texte("Type d'utilisation (fondations, dalle, murs) : ", ["fondations", "dalle", "murs"])
type_ciment = obtenir_entree_texte("Type de ciment (CPJ35, CPJ45, CPA55) : ", ["cpj35", "cpj45", "cpa55"])
taille_max_agregats = obtenir_entree_numerique("Taille maximale des agrégats (mm, entre 5 et 40) : ", 5, 40)
type_sable = obtenir_entree_texte("Type de sable (fin, moyen, grossier) : ", ["fin", "moyen", "grossier"])
temperature = obtenir_entree_numerique("Température ambiante (°C, entre 0 et 50) : ", 0, 50)
humidite = obtenir_entree_numerique("Humidité relative (%, entre 0 et 100) : ", 0, 100)
consistance = obtenir_entree_texte("Consistance souhaitée (ferme, plastique, très plastique, fluide) : ", 
                                   ["ferme", "plastique", "très plastique", "fluide"])

# Calculer et afficher les résultats
resultat = calculer_beton(
    resistance, type_utilisation, type_ciment, taille_max_agregats,
    type_sable, temperature, humidite, consistance
)

print("\nRésultats du calcul de mélange de béton :")
for key, value in resultat.items():
    print(f"{key}: {value}")

print("\nAttention : Ces résultats sont basés sur des calculs simplifiés et ne remplacent pas l'expertise d'un professionnel.")
print("Assurez-vous de respecter les normes marocaines en vigueur pour la formulation du béton.")