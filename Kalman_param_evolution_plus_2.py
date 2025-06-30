
# Exemple d'appel : python Kalman_param_evolution_plus_2.py 1


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm

# === Chargement des données ===
data = np.loadtxt("UpdatedCoefficients21.txt", skiprows=1)  # Ignorer la première ligne qui contient les en-têtes
# 18 17 16 very good 

time = data[:, 0]
nrmse = data[:, 1:11]   # 10 colonnes de NRMSE
nrmse = nrmse # / np.max(nrmse, axis=0)  # Normalisation des NRMSE
# Les paramètres sont aux colonnes paires à partir de 2 (0-based)
params = data[:,11::2]  # colonnes 11,13,... → les 15 
colors = plt.cm.tab20(np.linspace(0, 1, params.shape[1]))
stds = data[:, 12::2]   # colonnes 12,14,... → les 15 stds


#################### Partie 1 ##################
    # === Affichage des NRMSE cumulés ===
def partie_1():
    print("Exécution de la partie 1...")
    plt.figure(figsize=(10, 6))
    plt.plot(time, np.sum(nrmse, axis=1), label='Somme des NRMSE', color='red')
    plt.xlabel('Time')
    plt.ylabel('Somme des NRMSE')
    plt.title('Somme des 10 NRMSE au cours du temps')
    plt.grid(True)
    plt.legend(loc='upper right', fontsize='small')
    plt.tight_layout()
    plt.show()


################## Partie 2 ##################
    # === Affichage des NRMSE individuellement ===
def partie_2():
    print("Exécution de la partie 2...")
    plt.figure(figsize=(12, 6))
    for i in range(nrmse.shape[1]):
        plt.plot(time, nrmse[:, i], label=f'NRMSE {i+1}', color=colors[i])
    plt.xlabel('Time')
    plt.ylabel('NRMSE')
    plt.title('Évolution individuelle des 10 NRMSE') 
    plt.grid(True)
    plt.legend(loc='upper right', fontsize='small', ncol=2)
    plt.tight_layout()
    plt.show()


################## Partie 3 ##################
    # === Affichage des 15 paramètres ===
def partie_3():
    print("Exécution de la partie 3...")
    plt.figure(figsize=(10, 6))
    for i in range(params.shape[1]):
        plt.plot(time, params[:, i], label=f'Param {i+1}', color=colors[i])
    plt.xlabel('Time')
    plt.ylabel('Paramètres')
    plt.title('Évolution des 15 paramètres')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    plt.tight_layout()
    plt.show()


################## Partie 4 ##################
    # === Affichage des écarts-types ===
def partie_4():
    print("Exécution de la partie 4...")
    plt.figure(figsize=(10, 6))
    for i in range(stds.shape[1]):
        plt.plot(time, stds[:, i], label=f'Std {i+1}', color=colors[i])
        # plt.plot(time, stds[:, i]/abs(params[:,i]), label=f'Std {i+1}', color=colors[i])
    plt.xlabel('Time')
    plt.ylabel('Écarts-types')
    plt.title('Évolution des 15 écarts-types')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    plt.tight_layout()
    plt.show()

################## Partie 5 ##################
    # === Affichage somme des stds ===
def partie_5():
    print("Exécution de la partie 5...")
    sum_std = np.sum(stds, axis=1)
    plt.figure(figsize=(6, 4))
    plt.plot(time, sum_std, label='Somme des stds', color='orange')
    plt.xlabel('Time')
    plt.ylabel('Σ Std')
    plt.title('Somme des 15 écarts-types au cours du temps')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


################## Partie 6 ##################
    # === Animation des 5 courbes quadratiques f(x) = ax² + bx + c ===
def partie_6():
    print("Exécution de la partie 6...")

    # x pour les courbes
    x = np.linspace(0, 0.25, 300)

    # Préparation de la figure
    fig, axs = plt.subplots(5, 1, figsize=(8, 12), sharex=True)
    lines = []
    for ax in axs:
        line, = ax.plot([], [], lw=2)
        lines.append(line)
        ax.grid(True)

    axs[-1].set_xlabel("x")
    fig.suptitle("Évolution des 5 fonctions f(x) = ax² + bx + c", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Initialisation
    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    # Mise à jour par itération
    def update(frame):
        coeffs = params[frame]  # paramètres à cette itération

        for i in range(5):
            a, b, c = coeffs[3*i], coeffs[3*i+1], coeffs[3*i+2]
            fx = a * x**2 + b * x + c
            fx[x < 0.1] = a * 0.1**2 + b * 0.1 + c  # plateau à gauche
            # fx[x < 0.1] = a * 0.1**2 + b * 0.1 + c   : peut être inférieur à 0.

            lines[i].set_data(x, fx)
            axs[i].set_ylabel(f"f{i+1}(x)")
            axs[i].set_xlim(0, 0.25)
            axs[i].set_ylim(np.min(fx)-1e-2, np.max(fx)+1e-2)
            axs[i].legend([f"it={frame}, a={a:.2g}, b={b:.2g}, c={c:.2g}"], loc="best", fontsize="x-small")

        fig.suptitle(f"Itération {frame+1} — Pic = {time[frame]:.1f}", fontsize=14)
        return lines

    # Lancement animation
    ani = FuncAnimation(fig, update, frames=len(time), init_func=init, blit=False, interval=2000)
    plt.show()



# Mapping des parties
mapping = {
    1: partie_1,
    2: partie_2,
    3: partie_3,
    4: partie_4,
    5: partie_5,
    6: partie_6,
    #7: partie_7,
}

def main(PARTIE):
    if PARTIE in mapping:
        mapping[PARTIE]()
    else:
        print(f"Partie {PARTIE} non reconnue.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        print("Usage : python main_script.py <PARTIE>")











"""

# Somme des stds ligne par ligne
sum_std = np.sum(stds, axis=1)

# === Plot de tous les paramètres ===
plt.figure(figsize=(10, 6))
for i in range(params.shape[1]):
    plt.plot(time, params[:, i], label=f'Param {i+1}')
plt.xlabel('Time')
plt.ylabel('Paramètres')
plt.title('Évolution des paramètres vs Time')
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()
plt.show()

# === Plot de toutes les Std ===
plt.figure(figsize=(10, 6))
for i in range(stds.shape[1]):
    plt.plot(time, stds[:, i], label=f'Std {i+1}')
plt.xlabel('Time')
plt.ylabel('Écarts-types')
plt.title('Évolution des écarts-types (Std) vs Time')
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
plt.tight_layout()
plt.show()


# === PLOT ===
plt.figure(figsize=(12, 5))

# Plot NRMSE
plt.subplot(1, 2, 1)
plt.plot(time, nrmse, label='NRMSE')
plt.xlabel('Time')
plt.ylabel('NRMSE')
plt.title('NRMSE vs Time')
plt.grid(True)

# Plot somme des stds
plt.subplot(1, 2, 2)
plt.plot(time, sum_std, label='Σ Std', color='orange')
plt.xlabel('Time')
plt.ylabel('Somme des Std')
plt.title('Somme des Std vs Time')
plt.grid(True)

plt.tight_layout()
plt.show()


############ Visualisation des 5 fonctions f(x) = ax² + bx + c ################


# Dernière ligne = dernière estimation
final_params = params[-1, :]  # shape (15,)

# Génération de x : entre 0 et 0.25
x = np.linspace(0, 0.25, 300)

# Préparation des courbes f(x) = ax² + bx + c avec f(x) = f(0.1) pour x < 0.1
fig, axs = plt.subplots(5, 1, figsize=(8, 12), sharex=True)
fig.suptitle("Visualisation des 5 fonctions f(x) = ax² + bx + c", fontsize=14)

for i in range(5):
    a = final_params[3*i]
    b = final_params[3*i+1]
    c = final_params[3*i+2]

    fx = a * x**2 + b * x + c

    # On écrase les valeurs de fx pour x < 0.1 par f(0.1)
    f_plateau = a * 0.1**2 + b * 0.1 + c
    fx[x < 0.1] = f_plateau

    axs[i].plot(x, fx, label=f"f{i+1}(x) = {a:.2g}x² + {b:.2g}x + {c:.2g}")
    axs[i].set_ylabel(f"f{i+1}(x)")
    axs[i].grid(True)
    axs[i].legend(loc='best')

axs[-1].set_xlabel("x")
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()




#############################################

# Animation des 5 fonctions f(x) = ax² + bx + c


params = data[:, 2::2]  # Paramètres uniquement (shape: n_iter × 15)

# === Préparation de x pour tracer les courbes ===
x = np.linspace(0, 0.25, 300)

# === Création de la figure avec 5 subplots ===
fig, axs = plt.subplots(5, 1, figsize=(8, 12), sharex=True)
lines = []

for ax in axs:
    line, = ax.plot([], [], lw=2)
    lines.append(line)
    ax.grid(True)

axs[-1].set_xlabel("x")
fig.suptitle("Évolution des fonctions f(x) = ax² + bx + c au fil des itérations", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])

# === Fonction d'initialisation ===
def init():
    for line in lines:
        line.set_data([], [])
    return lines

# === Fonction de mise à jour à chaque frame ===
def update(frame):
    coeffs = params[frame]  # les 15 paramètres à une itération donnée

    for i in range(5):
        a = coeffs[3*i]
        b = coeffs[3*i+1]
        c = coeffs[3*i+2]

        fx = a * x**2 + b * x + c
        f_plateau = a * 0.1**2 + b * 0.1 + c
        fx[x < 0.1] = f_plateau

        lines[i].set_data(x, fx)
        axs[i].set_ylabel(f"f{i+1}(x)")
        axs[i].set_xlim(0, 0.25)
        axs[i].set_ylim(np.min(fx)-1e-2, np.max(fx)+1e-2)
        axs[i].legend([f"it={frame}, a={a:.2g}, b={b:.2g}, c={c:.2g}"], loc="best", fontsize="small")

    fig.suptitle(f"Itération {frame+1} — Time = {time[frame]:.1f}", fontsize=14)
    return lines

# === Lancement de l'animation ===
ani = FuncAnimation(fig, update, frames=len(time), init_func=init, blit=False, interval=1000)

plt.show()
"""