# Beamforming Pattern for a Uniform Linear Array
# This code generates a polar plot of the beamforming pattern for a uniform linear array (ULA) antenna.
# The pattern is calculated based on the number of antennas, antenna spacing, and steering phase shift.
# The plot is saved as a PNG file in the "plots" directory.

import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(-np.pi, np.pi, 1000)
N = 8          # Number of antennas
d = 0.5        # Antenna spacing (λ/2)
k = 2 * np.pi  # Wave number
beta = 0       # Steering phase shift

psi = k * d * np.cos(theta) + beta
AF = np.abs(np.sin(N * psi / 2) / (N * np.sin(psi / 2)))
AF = AF / np.max(AF)  # Normalize

plt.figure(figsize=(6, 6))
plt.polar(theta, AF)
plt.title("Beamforming Pattern (Uniform Linear Array)", pad=20)
plt.savefig("plots/beamforming_pattern.png")
plt.show()
plt.close()