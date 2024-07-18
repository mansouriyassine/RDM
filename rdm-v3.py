#!/usr/bin/env python3
# Fonction pour calculer les moments fléchissants
def calculer_moments(travees):
    moments = []
    for i in range(len(travees)):
        if i == 0:
            M_prev = 0  # Moment initial
        else:
            M_prev = moments[-1]
        
        L = travees[i]['longueur']
        q = travees[i]['charge']
        
        # Calculer le moment fléchissant selon l'équation
        Mi = M_prev + q * L
        
        # Ajouter le moment calculé à la liste des moments
        moments.append(Mi)
    
    return moments

# Demander les données d'entrée à l'utilisateur
def demander_donnees():
    nb_travees = int(input("Entrez le nombre de travees : "))
    travees = []
    
    for i in range(nb_travees):
        longueur = float(input(f"Entrez la longueur de la travee {i+1} (en m) : "))
        charge = float(input(f"Entrez la charge uniformement repartie sur la travee {i+1} (en kN/m) : "))
        travee = {'longueur': longueur, 'charge': charge}
        travees.append(travee)
    
    return travees

# Fonction principale pour exécuter le script
def main():
    travees = demander_donnees()
    
    # Supposons que EI = 1 pour cet exemple, à adapter selon votre cas
    EI = 1.0
    
    # Calculer les moments fléchissants
    moments_flechissants = calculer_moments(travees)
    
    # Afficher les résultats
    print("\nMoments fléchissants calculés :")
    for i, moment in enumerate(moments_flechissants):
        print(f"Travee {i+1}: {moment} kN·m")

# Appeler la fonction principale
if __name__ == "__main__":
    main()