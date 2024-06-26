import numpy as np
import matplotlib.pyplot as plt

def calculate_ER(q, p):
    # Espérance de la récompense pour l'attaque 2+1
    return 3 * q**3 + 4 * p * q**2

def calculate_EH(q, p):
    # Espérance de la hauteur pour l'attaque 2+1
    return p + 3 * q**3 + 4 * p * q**2 + 2 * p**2 * q

def calculate_rendement(q, p):
    # Calcule le rendement comme le ratio E[R] / E[H]
    ER = calculate_ER(q, p)
    EH = calculate_EH(q, p)
    return ER / EH if EH != 0 else 0

def simulate_attack_2_plus_1():
    # Génère des valeurs de q (probabilité de Alice) de 0.01 à 0.99
    q_values = np.linspace(0.001, 0.999, 100000)
    # Calcule les rendements pour chaque valeur de q
    rendement_values = [calculate_rendement(q, 1 - q) for q in q_values]
    # Rendement linéaire pour un minage honnête (q)
    honest_values = q_values

    # Trouver l'intersection des courbes
    differences = np.array(rendement_values) - np.array(honest_values)
    idx = np.argwhere(np.diff(np.sign(differences))).flatten()


    # Crée une nouvelle figure pour le graphique
    plt.figure(figsize=(10, 6))
    # Trace la courbe de rendement pour l'attaque 2+1
    plt.plot(q_values, rendement_values, label="Rendement de l'attaque 2+1")
    # Trace la courbe de rendement pour le minage honnête
    plt.plot(q_values, honest_values, label="Rendement Minage honnête")
    # Ajouter le point d'intersection
    if len(idx) > 0:
        intersection_x = q_values[idx[0]]
        intersection_y = rendement_values[idx[0]]
        plt.scatter(intersection_x, intersection_y, color='red')
        plt.annotate(f'Intersection: ({intersection_x:.2f})',
                     (intersection_x, intersection_y),
                     textcoords="offset points", xytext=(-15,-10), ha='center')

    # Ajoute des labels et un titre au graphique
    plt.xlabel('Hashrate')
    plt.ylabel('Rendement')
    plt.title("Rendement de l'attaque 2+1 en fonction de la puissance de l'attaquant (q)")
    # Ajoute une légende et une grille en pointillés
    plt.legend()
    # Affiche le graphique
    plt.show()

# Point d'entrée principal
if __name__ == "__main__":
    simulate_attack_2_plus_1()
