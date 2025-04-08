import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# Paramètres
grid_size = 50  # Taille de la grille
scale = 10      # Échelle de la corrélation
sigma = 5       # Écart type pour le filtre gaussien

# Générer une grille de points aléatoires
np.random.seed(42)
field = np.random.rand(grid_size, grid_size)

# Appliquer un filtre gaussien pour introduire l'autocorrélation spatiale
field_smoothed = gaussian_filter(field, sigma=sigma)

# Afficher la grille originale et la grille corrélée
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Grille initiale
axs[0].imshow(field, cmap='viridis', interpolation='none')
axs[0].set_title('Grille initiale (sans corrélation)')

# Grille lissée
axs[1].imshow(field_smoothed, cmap='viridis', interpolation='none')
axs[1].set_title(f'Grille lissée (autocorrélation spatiale, sigma={sigma})')

plt.show()