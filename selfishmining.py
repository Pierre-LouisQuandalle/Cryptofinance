import numpy as np
import matplotlib.pyplot as plt

def profil(proba):
    #simule un lancé de pièce biaisé
    return np.random.choice([True, False], p=[proba, 1 - proba])

def Sim(q, z, N):
    """Simule l'attaque de Selfish Mining."""
    alpha = q  # Taux de hachage d'Alice
    gamma = 0.5  # Probabilité qu'un bloc sur une chaîne bifurquée soit miné par Alice
    
    lead = 0
    alice_blocks = 0
    bob_blocks = 0

    for _ in range(N):
        if profil(alpha):  # Alice trouve un bloc
            lead += 1
        else:  # Bob trouve un bloc
            if lead == 0:
                bob_blocks += 1
            elif lead == 1:
                if profil(gamma):  # Bifurcation
                    alice_blocks += 1
                    lead -= 1
                else:
                    bob_blocks += 1
                    lead -= 1
            else:
                alice_blocks += 2
                lead -= 2
    
    return alice_blocks, bob_blocks

def simulate_selfish_mining(N, q_values, z):
    """Simule l'attaque de Selfish Mining pour différentes valeurs de q."""
    results = []

    for q in q_values:
        alice_blocks, bob_blocks = Sim(q, z, N)
        total_blocks = alice_blocks + bob_blocks
        rendement = alice_blocks / total_blocks if total_blocks > 0 else 0
        results.append(rendement)

    return results

def main_simulation_selfish_mining():
    q_values = np.linspace(0.01, 0.49, 15000)  # Probabilité de Alice
    N = 10000  # Nombre de cycles d'attaque
    z = 6  # Nombre de confirmations nécessaires (non utilisé dans cette simulation)

    rendement_values = simulate_selfish_mining(N, q_values, z)
    honest_values = q_values  # Rendement linéaire pour un minage honnête
    # Trouver l'intersection des courbes
    differences = np.array(rendement_values) - np.array(honest_values)
    idx = np.argwhere(np.diff(np.sign(differences))).flatten()


    plt.figure(figsize=(10, 6))
    plt.plot(q_values, rendement_values, label="Rendement de l'attaque Selfish Mining")
    plt.plot(q_values, honest_values, label="Minage honnête", linestyle='--')
    # Ajouter le point d'intersection
    if len(idx) > 0:
        intersection_x = q_values[idx[0]]
        intersection_y = rendement_values[idx[0]]
        plt.scatter(intersection_x, intersection_y, color='red')
        plt.annotate(f'Intersection: ({intersection_x:.2f})',
                     (intersection_x, intersection_y),
                     textcoords="offset points", xytext=(-15,-10), ha='center')
    plt.xlabel('Hashrate(q)')
    plt.ylabel('Rendement')
    plt.title("Rendement de l'attaque Selfish Mining en fonction de la probabilité de l'attaquant")
    plt.legend()
    plt.grid(linestyle='dotted')
    plt.show()

if __name__ == "__main__":
    main_simulation_selfish_mining()
