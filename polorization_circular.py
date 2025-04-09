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
ax.set_title('Polarized EM Wave')
ax.legend()
ax.view_init(elev=25, azim=-45)
ax.grid(True)

# Polarization angle (initially set to circular polarization)
polarization_angle = 90

def apply_polarization(frame, polarization_angle):
    """Calculate polarized electric and magnetic fields."""
    angle_rad = np.radians(polarization_angle)
    t = t_values[frame]
    
    # Electric field components
    E_y = amplitude * np.sin(k * x - omega * t) * np.cos(angle_rad)
    E_z = amplitude * np.sin(k * x - omega * t + np.pi / 2) * np.sin(angle_rad)

    # Magnetic field components (perpendicular to E)
    B_z = amplitude * np.sin(k * x - omega * t) * np.cos(angle_rad)
    B_y = -amplitude * np.sin(k * x - omega * t + np.pi / 2) * np.sin(angle_rad)

    return E_y, E_z, B_y, B_z

def init():
    """Initialize the plot elements."""
    E_line.set_data([], [])
    E_line.set_3d_properties([])
    B_line.set_data([], [])
    B_line.set_3d_properties([])
    return E_line, B_line

def update(frame):
    """Update the animation frame."""
    # Calculate fields with polarization angle
    E_y, E_z, B_y, B_z = apply_polarization(frame, polarization_angle)

    # Update electric field line
    E_line.set_data(x, E_y)
    E_line.set_3d_properties(E_z)

    # Update magnetic field line
    B_line.set_data(x, B_y)
    B_line.set_3d_properties(B_z)

    return E_line, B_line

# Create slider for polarization angle
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
slider = Slider(ax_slider, 'Polarization Angle', valmin=0, valmax=360, valinit=polarization_angle)

def update_polarization(val):
    """Update global polarization angle based on slider value."""
    global polarization_angle
    polarization_angle = slider.val

slider.on_changed(update_polarization)

# Create animation using updated function
ani = FuncAnimation(fig, update, init_func=init, frames=len(t_values), interval=50, blit=True)

plt.tight_layout()
plt.show()
