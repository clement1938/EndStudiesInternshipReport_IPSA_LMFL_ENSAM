import numpy as np
import matplotlib.pyplot as plt

# === Chargement des données ===
data = np.loadtxt("UpdatedCoefficients3.txt")

time = data[:, 0]
nrmse = data[:, 1]

# Les paramètres sont aux colonnes paires à partir de 2 (0-based)
params = data[:, 2::2]  # colonnes 2,4,6,..., jusqu'à 32
stds = data[:, 3::2]    # colonnes 3,5,7,..., jusqu'à 33

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