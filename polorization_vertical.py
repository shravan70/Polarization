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

# Configuration
ax.set_xlim(0, 3 * wavelength)
ax.set_ylim(-1.5 * amplitude, 1.5 * amplitude)
ax.set_zlim(-1.5 * amplitude, 1.5 * amplitude)
ax.set_xlabel('Propagation direction (X)')
ax.set_ylabel('Electric field (Y)')
ax.set_zlabel('Magnetic field (Z)')
ax.set_title('EM Wave Propagation with Adjustable Polarization')
ax.legend()
ax.view_init(elev=25, azim=-45)
ax.grid(True)

# Polarization angle (initially set to vertical polarization)
polarization_angle = 90


def apply_polarization_filter(E_x, E_y, angle):
    """Apply polarization filter based on angle."""
    angle_rad = np.radians(angle)
    E_x_filtered = E_x * np.cos(angle_rad)  # Horizontal component scaled by angle
    E_y_filtered = E_y * np.sin(angle_rad)  # Vertical component scaled by angle
    return E_x_filtered, E_y_filtered


def init():
    """Initialize the plot elements."""
    E_line.set_data([], [])
    E_line.set_3d_properties([])
    B_line.set_data([], [])
    B_line.set_3d_properties([])
    return E_line, B_line


def update(frame):
    """Update the animation frame."""
    global polarization_angle
    t = t_values[frame]

    # Calculate field values
    phase = k * x - omega * t
    E_y = amplitude * np.sin(phase)  # Electric field in Y-direction
    E_x = amplitude * np.cos(phase)  # Electric field in X-direction for circular polarization
    B_z = amplitude * np.sin(phase)  # Magnetic field in Z-direction

    # Apply polarization filter to electric fields based on slider value
    E_x_filtered, E_y_filtered = apply_polarization_filter(E_x, E_y, polarization_angle)

    # Update electric field line (filtered components)
    E_line.set_data(x, E_y_filtered)
    E_line.set_3d_properties(z)

    # Update magnetic field line (no filtering applied here)
    B_line.set_data(x, y)
    B_line.set_3d_properties(B_z)

    return E_line, B_line


# Create slider for polarization angle
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
slider = Slider(ax_slider, 'Polarization Angle', valmin=0, valmax=90, valinit=polarization_angle)


def update_polarization(val):
    """Update global polarization angle based on slider value."""
    global polarization_angle
    polarization_angle = slider.val


slider.on_changed(update_polarization)

# Create animation
ani = FuncAnimation(fig, update, init_func=init, frames=len(t_values), interval=50, blit=True)

plt.tight_layout()
plt.show()
