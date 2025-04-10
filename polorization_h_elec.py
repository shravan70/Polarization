import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Setup figure
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Wave parameters
wavelength = 2 * np.pi
frequency = 0.5
amplitude = 1
k = 2 * np.pi / wavelength  # wave number
omega = 2 * np.pi * frequency  # angular frequency

# Create spatial coordinates
x = np.linspace(0, 3 * wavelength, 100)
y = np.zeros_like(x)
z = np.zeros_like(x)
t_values = np.linspace(0, 2 * np.pi / omega, 60)  # Time steps

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
ax.set_xlim(0, 3 * wavelength)
ax.set_ylim(-1.5 * amplitude, 1.5 * amplitude)
ax.set_zlim(-1.5 * amplitude, 1.5 * amplitude)
ax.set_xlabel('Propagation direction (X)')
ax.set_ylabel('Electric field (Y)')
ax.set_zlabel('Magnetic field (Z)')
ax.set_title('EM Wave Propagation in 3D Space with Polarization')
ax.legend()
ax.view_init(elev=25, azim=-45)
ax.grid(True)

# Polarization angle (initially 0 degrees)
polarization_angle = 0


def apply_polarization_filter(E_x, E_y, angle):
    """Apply polarization filter to the electric field."""
    angle_rad = np.radians(angle)
    # Combine components based on polarization angle
    E_x_filtered = E_x * np.cos(angle_rad)
    E_y_filtered = E_y * np.sin(angle_rad)
    return E_x_filtered, E_y_filtered


def update(frame):
    global polarization_angle
    t = t_values[frame]

    # Calculate field values
    phase = k * x - omega * t
    E_y = amplitude * np.sin(phase)  # Electric field in Y-direction
    E_x = amplitude * np.cos(phase)  # Electric field in X-direction for circular polarization
    B_z = amplitude * np.sin(phase)  # Magnetic field in Z-direction

    # Apply polarization filter to electric fields
    E_x_filtered, E_y_filtered = apply_polarization_filter(E_x, E_y, polarization_angle)

    # Update electric field line (filtered components)
    E_line.set_data_3d(x, E_y_filtered, z)

    # Update magnetic field line (no filtering applied here)
    B_line.set_data_3d(x, y, B_z)

    # Update vector fields for electric and magnetic fields
    E_arrows.set_segments(np.array([
        [[x[i], y[i], z[i]], [x[i], E_y_filtered[i], z[i]]] for i in arrow_points
    ]))
    
    B_arrows.set_segments(np.array([
        [[x[i], y[i], z[i]], [x[i], y[i], B_z[i]]] for i in arrow_points
    ]))

    return E_line, B_line, E_arrows, B_arrows


# Create slider for polarization angle
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
slider = Slider(ax_slider, 'Polarization Angle', 0, 90, valinit=polarization_angle)


def update_polarization(val):
    global polarization_angle
    polarization_angle = slider.val


slider.on_changed(update_polarization)

# Create animation
ani = FuncAnimation(fig, update, frames=len(t_values), interval=50, blit=False)

plt.tight_layout()
plt.show()
