import matplotlib.pyplot as plt
import numpy as np
import re

# Initialisation
times = []
param_values = [[] for _ in range(5)]
param_vars = [[] for _ in range(5)]

filename = "UpdatedCoefficients.txt"

with open(filename, "r") as f:
    for line in f:
        match = re.match(
            r"^\s*([\d.e+-]+)\s+Param1\s*:\s*([\d.e+-]+)\s+([\d.e+-]+)\s+"
            r"Param2\s*:\s*([\d.e+-]+)\s+([\d.e+-]+)\s+"
            r"Param3\s*:\s*([\d.e+-]+)\s+([\d.e+-]+)\s+"
            r"Param4\s*:\s*([\d.e+-]+)\s+([\d.e+-]+)\s+"
            r"Param5\s*:\s*([\d.e+-]+)\s+([\d.e+-]+)",
            line
        )
        if not match:
            print(f"Ligne incorrecte ignorée : {line.strip()}")
            continue

        nums = list(map(float, match.groups()))
        times.append(nums[0])
        for i in range(5):
            param_values[i].append(nums[1 + 2*i])
            param_vars[i].append(nums[2 + 2*i])

# Conversion en tableaux numpy
times = np.array(times)
param_values = np.array(param_values)
param_vars = np.array(param_vars)

# Suppression des 6 premières lignes
times = times[6:]
param_values = param_values[:, 6:]
param_vars = param_vars[:, 6:]

# Affichage pour debug
print("Temps :", times)
print("Valeurs des paramètres :", param_values)
print("Variances des paramètres :", param_vars)

# Affichage des courbes avec variance
fig, axs = plt.subplots(3, 2, figsize=(12, 10))
axs = axs.flatten()

for i in range(5):
    mean = param_values[i]
    std = param_vars[i] #np.sqrt(param_vars[i])  # 1 sigma = racine de la variance
    print(f"Param {i} std dev: {std}")
    axs[i].plot(times, mean, label=f'Param{i+1}', color='tab:red')
    axs[i].fill_between(times, mean - std, mean + std, alpha=0.5, color='tab:blue', label='±1σ')
    axs[i].set_title(f'Paramètre {i+1}')
    axs[i].set_xlabel('Temps')
    axs[i].set_ylabel('Valeur')
    axs[i].grid(True)
    axs[i].legend()

# Supprimer subplot vide
fig.delaxes(axs[5])
plt.tight_layout()
plt.show()
