import numpy as np
import matplotlib.pyplot as plt
from random import random

# Simule un lancer de pièce biaisée avec une probabilité 'proba' pour True (Alice trouve un bloc)
# et '1-proba' pour False (Bob trouve un bloc)
def tos(proba):
    return np.random.choice((True, False), p=[proba, 1-proba])

# q : Taux de hachage d'Alice.
# z : Nombre de confirmations nécessaires.
# A : Seuil de tolérance.
# k : Nombre de blocs prémédités par Alice.
# v : Valeur de la double dépense
def Sim(q, z, A, k, v):
    H = 0  # Chaîne officielle (nombre de blocs honnêtes)
    AliceChain = k  # Nombre de blocs prémédités par Alice
    succesAttempt = 0  # Nombre de tentatives réussies par Alice
    # Boucle de simulation de l'attaque
    while (H - AliceChain) < A and H < z and AliceChain < z:
        piece = tos(q)
        if piece:
             # Alice trouve un bloc et le garde privé
            succesAttempt += 1
            AliceChain += 1
        else:
             # Bob trouve un bloc et l'ajoute à la chaîne honnête
            H += 1

    if AliceChain > H:
        succesAttempt += v
        H = AliceChain
        #La chaîne d'Alice devient la chaîne officielle
    else:
        #La chaîne d'Alice échoue et n'est pas la chaîne officielle
        succesAttempt = 0

    return [succesAttempt, H]

def simulate(N, q, z, A, k, v):
    Rn = 0  # Récompenses accumulées par Alice
    Hn = 0  # Nombre de blocs ajoutés à la chaîne honnête
    # Exécute 'N' simulations de l'attaque
    for _ in range(N):
        RH = Sim(q, z, A, k, v)
        Rn += RH[0]
        Hn += RH[1]
    # Calcule le rendement moyen (ratio des récompenses aux blocs ajoutés)
    return Rn / Hn if Hn != 0 else 0

def main_simulation(N):
    k = 0   # Nombre de blocs prémédités par Alice
    v = 1   # Valeur de la double dépense
    Hashrate = [p / 100 for p in range(1, 50)]
    EsperanceGains = [simulate(N, p / 100, 6, 3, k, v) for p in range(1, 50)]
    EsperanceGains6 = [simulate(N, p / 100, 6, 10, k, v) for p in range(1, 50)]
    EsperanceGains10 = [simulate(N, p / 100, 10, 3, k, v) for p in range(1, 50)]

    plt.figure(figsize=(10, 6))
    plt.plot(Hashrate, EsperanceGains, label='Simulation, confirmations=6, A=3')
    plt.plot(Hashrate, EsperanceGains6, label='Simulation, confirmations=6, A=10')
    plt.plot(Hashrate, EsperanceGains10, label='Simulation, confirmations=10, A=3')
    plt.plot(Hashrate, Hashrate, label='Honest')
    plt.xlabel('Hashrate')
    plt.ylabel('Esperance de gain')
    plt.title('DDouble Spending')
    plt.legend()
    plt.grid(linestyle='dotted')
    plt.show()

if __name__ == "__main__":
    N = 100000  # nombre de cycles d'attaque
    main_simulation(N)
