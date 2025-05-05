import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

theta = np.linspace(0, np.pi, 180)
phi = np.linspace(0, 2 * np.pi, 360)
theta, phi = np.meshgrid(theta, phi)

r = np.abs(np.sin(theta))  #𝑟(𝜃,𝜙)=∣sin(𝜃)|
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')
ax.set_title("3D Dipole Radiation Pattern")
plt.savefig("plots/shravan_dipole_3d_plot.png")
plt.show()
plt.close()