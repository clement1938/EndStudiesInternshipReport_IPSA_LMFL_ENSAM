import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Matplotlib config for LaTeX fonts
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 12
})

# Parameters
mu = 3
sigma = 0.5
lambda_k = 1.8
n_ens = 5

# Generate evenly spaced samples (to control spacing)
u = np.linspace(mu - 2*sigma, mu + 2*sigma, n_ens)
u_pdf = norm.pdf(u, mu, sigma)
u_inflated = mu + lambda_k * (u - mu)
u_inf_pdf = norm.pdf(u_inflated, mu, lambda_k * sigma)

# Plot setup
x_vals = np.linspace(mu - 4*sigma*lambda_k, mu + 4*sigma*lambda_k, 500)
pdf_before = norm.pdf(x_vals, mu, sigma)
pdf_after = norm.pdf(x_vals, mu, lambda_k * sigma)

fig, ax = plt.subplots(figsize=(10, 3))

# Plot both PDFs
ax.plot(x_vals, pdf_before, 'k--', label=r'Initial PDF: $\mathcal{N}(\mu, \sigma^2)$')
ax.plot(x_vals, pdf_after, 'k-', label=r'Inflated PDF: $\mathcal{N}(\mu, \lambda_k^2 \sigma^2)$')

# Mean line
ax.axvline(mu, color='black', linestyle=':', label=r'Mean $\bar{u}_k^a$')

# Scatter points on their respective PDFs
ax.scatter(u, u_pdf, color='blue', label='Original samples', zorder=5)
ax.scatter(u_inflated, u_inf_pdf, color='red', label='Inflated samples', zorder=5)

# Arrows from original to inflated samples
for x0, y0, x1, y1 in zip(u, u_pdf, u_inflated, u_inf_pdf):
    ax.annotate("",
                xy=(x1, y1), xycoords='data',
                xytext=(x0, y0), textcoords='data',
                arrowprops=dict(arrowstyle='->', color='gray', lw=1))

# Formatting
ax.set_ylim(bottom=0)
ax.set_yticks([])
ax.set_xlabel(r"Sample values $u_{i,k}^a$")
ax.set_title(r"Inflation around the mean: $u_{i,k}^a = \bar{u}_k^a + \lambda_k (u_{i,k}^a - \bar{u}_k^a)$")
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig("inflation_visualisation.pdf")
plt.show()
