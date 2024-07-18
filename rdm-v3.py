#!/usr/bin/env python3
class Travée:
    def __init__(self, numero):
        self.numero = numero
        self.L = float(input(f"Entrez la longueur de la travée {numero} (en m) : "))
        self.q = float(input(f"Entrez la charge uniformément répartie sur la travée {numero} (en kN/m) : "))
        self.MT0 = None  # Initialisation du moment MT0
        self.teta0 = None  # Initialisation de teta0

    def calculer_MT0(self):
        # Calcul de MT0 en fonction de L et q
        self.MT0 = self.q * self.L / 2

    def calculer_teta0(self):
        # Calcul de teta0 en utilisant la formule -D3*C3^3/24 (hypothétique)
        self.teta0 = -self.q * self.L**3 / 24

    def calculer_Ma(self, teta0_suivant):
        # Calculer 6 * (teta0(i+1) - teta0(i))
        delta_teta0 = teta0_suivant - self.teta0
        moment = 6 * delta_teta0
        return moment

# Demander le nombre de travées à l'utilisateur
nombre_travees = int(input("Entrez le nombre de travées : "))

# Créer les travées en fonction des entrées de l'utilisateur
travees = []
for i in range(1, nombre_travees + 1):
    travee = Travée(i)
    travees.append(travee)

# Calculer et afficher les résultats pour chaque travée
for i in range(len(travees)):
    if i < len(travees) - 1:
        teta_suivant = travees[i + 1].teta0
    else:
        teta_suivant = 0  # hypothétique, à ajuster selon la logique de votre modèle

    travee = travees[i]
    travee.calculer_MT0()
    travee.calculer_teta0()
    moment_Ma = travee.calculer_Ma(teta_suivant)
    print(f"Travée {travee.numero} de longueur {travee.L} m et charge {travee.q} KN/m :")
    print(f"MT0 calculé : {travee.MT0} KN.m")
    print(f"teta0 calculé : {travee.teta0}")
    print(f"Ma calculé : {moment_Ma} KN.m")
    print()