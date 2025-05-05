import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(0, 2 * np.pi, 360)
r = np.abs(np.sin(theta))  #U(θ) ∝ |sin(θ)|

plt.figure(figsize=(6, 6))
plt.polar(theta, r)
plt.title("Dipole Antenna Radiation Pattern", pad=20)
plt.savefig("plots/shravan_dipole_polar_plot.png")
plt.show()
plt.close()