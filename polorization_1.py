import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Setup figure
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Wave parameters
wavelength = 2*np.pi
frequency = 0.5
amplitude = 1
k = 2*np.pi/wavelength  # wave number
omega = 2*np.pi*frequency  # angular frequency

# Create spatial coordinates
x = np.linspace(0, 3*wavelength, 100)
y = np.zeros_like(x)
z = np.zeros_like(x)
t_values = np.linspace(0, 2*np.pi/omega, 60)  # Time steps

# Initialize plots
E_line, = ax.plot([], [], [], 'r-', linewidth=2, label='Electric Field (E)')
B_line, = ax.plot([], [], [], 'b-', linewidth=2, label='Magnetic Field (B)')

# Select points for vector arrows
step = 5
arrow_points = np.arange(0, len(x), step)
arrow_x = x[arrow_points]
arrow_y = y[arrow_points]
arrow_z = z[arrow_points]

# Initialize quivers
E_arrows = ax.quiver(arrow_x, arrow_y, arrow_z, 
                    np.zeros_like(arrow_x), np.zeros_like(arrow_x), np.zeros_like(arrow_x),
                    color='red', length=0.3, normalize=False, arrow_length_ratio=0.3)

B_arrows = ax.quiver(arrow_x, arrow_y, arrow_z,
                    np.zeros_like(arrow_x), np.zeros_like(arrow_x), np.zeros_like(arrow_x),
                    color='blue', length=0.3, normalize=False, arrow_length_ratio=0.3)

# Configuration
ax.set_xlim(0, 3*wavelength)
ax.set_ylim(-1.5*amplitude, 1.5*amplitude)
ax.set_zlim(-1.5*amplitude, 1.5*amplitude)
ax.set_xlabel('Propagation direction (X)')
ax.set_ylabel('Electric field (Y)')
ax.set_zlabel('Magnetic field (Z)')
ax.set_title('EM Wave Propagation in 3D Space')
ax.legend()
ax.view_init(elev=25, azim=-45)
ax.grid(True)

def update(frame):
    t = t_values[frame]
    
    # Calculate field values
    phase = k*x - omega*t
    E_y = amplitude * np.sin(phase)
    B_z = amplitude * np.sin(phase)
    
    # Update field lines
    E_line.set_data_3d(x, E_y, z)
    B_line.set_data_3d(x, y, B_z)
    
    # Update vector fields
    E_arrows.set_segments(np.array([
        [ [x[i], y[i], z[i]], [x[i], E_y[i], z[i]] ] for i in arrow_points
    ]))
    
    B_arrows.set_segments(np.array([
        [ [x[i], y[i], z[i]], [x[i], y[i], B_z[i]] ] for i in arrow_points
    ]))
    
    return E_line, B_line, E_arrows, B_arrows

# Create animation
ani = FuncAnimation(fig, update, frames=len(t_values), interval=50, blit=False)

plt.tight_layout()
plt.show()