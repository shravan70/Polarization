import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

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

# Add polarization trace to visualize the pattern
polarization_trace, = ax.plot([], [], [], 'g-', linewidth=1.5, alpha=0.7, label='Polarization Trace')

# Configuration
ax.set_xlim(0, 3 * wavelength)
ax.set_ylim(-1.5 * amplitude, 1.5 * amplitude)
ax.set_zlim(-1.5 * amplitude, 1.5 * amplitude)
ax.set_xlabel('Propagation direction (X)')
ax.set_ylabel('Electric field (Y)')
ax.set_zlabel('Electric field (Z)')
ax.set_title('Horizontally Polarized EM Wave')
ax.legend()
ax.view_init(elev=25, azim=-45)
ax.grid(True)

# Global variables
polarization_mode = "horizontal"  # Default to horizontal polarization
animation_running = True  # Animation state

# Parameters for elliptical polarization
amplitude_y = 1.0
amplitude_z = 0.5
phase_difference = np.pi / 4

# Select a specific point for the polarization trace
trace_index = 25
trace_length = 40

# Storage for trace points
trace_y = np.zeros(trace_length)
trace_z = np.zeros(trace_length)
trace_x = np.ones(trace_length) * x[trace_index]

def calculate_fields(frame):
    """Calculate field components based on polarization mode."""
    t = t_values[frame]
    phase = k * x - omega * t
    
    if polarization_mode == "horizontal":
        # Horizontal linear polarization
        E_y = amplitude * np.sin(phase)
        E_z = np.zeros_like(x)
        B_y = np.zeros_like(x)
        B_z = amplitude * np.sin(phase)
        
    elif polarization_mode == "vertical":
        # Vertical linear polarization
        E_y = np.zeros_like(x)
        E_z = amplitude * np.sin(phase)
        B_y = amplitude * np.sin(phase)
        B_z = np.zeros_like(x)
        
    elif polarization_mode == "circular":
        # Circular polarization
        E_y = amplitude * np.sin(phase)
        E_z = amplitude * np.sin(phase + np.pi/2)  # 90-degree phase shift
        B_y = -amplitude * np.sin(phase + np.pi/2)
        B_z = amplitude * np.sin(phase)
        
    elif polarization_mode == "elliptical":
        # Elliptical polarization
        E_y = amplitude_y * np.sin(phase)
        E_z = amplitude_z * np.sin(phase + phase_difference)
        B_y = -amplitude_z * np.sin(phase + phase_difference)
        B_z = amplitude_y * np.sin(phase)
    
    return E_y, E_z, B_y, B_z

def init():
    """Initialize the plot elements."""
    E_line.set_data([], [])
    E_line.set_3d_properties([])
    B_line.set_data([], [])
    B_line.set_3d_properties([])
    polarization_trace.set_data([], [])
    polarization_trace.set_3d_properties([])
    return E_line, B_line, polarization_trace

def update(frame):
    """Update the animation frame."""
    global trace_y, trace_z
    
    if not animation_running:
        return E_line, B_line, polarization_trace
    
    # Calculate fields based on current polarization mode
    E_y, E_z, B_y, B_z = calculate_fields(frame)
    
    # Update electric field line
    E_line.set_data(x, E_y)
    E_line.set_3d_properties(E_z)
    
    # Update magnetic field line
    B_line.set_data(x, B_y)
    B_line.set_3d_properties(B_z)
    
    # Update polarization trace
    trace_y = np.roll(trace_y, -1)
    trace_z = np.roll(trace_z, -1)
    trace_y[-1] = E_y[trace_index]
    trace_z[-1] = E_z[trace_index]
    polarization_trace.set_data(trace_x, trace_y)
    polarization_trace.set_3d_properties(trace_z)
    
    return E_line, B_line, polarization_trace

# Create buttons
button_height = 0.06
button_width = 0.15

# Polarization mode buttons
ax_button_horizontal = plt.axes([0.15, 0.05, button_width, button_height])
ax_button_vertical = plt.axes([0.35, 0.05, button_width, button_height])
ax_button_circular = plt.axes([0.55, 0.05, button_width, button_height])
ax_button_elliptical = plt.axes([0.75, 0.05, button_width, button_height])

# Create buttons
button_horizontal = Button(ax_button_horizontal, 'Horizontal')
button_vertical = Button(ax_button_vertical, 'Vertical')
button_circular = Button(ax_button_circular, 'Circular')
button_elliptical = Button(ax_button_elliptical, 'Elliptical')

# Button callback functions
def set_horizontal(event):
    global polarization_mode
    polarization_mode = "horizontal"
    ax.set_title('Horizontally Polarized EM Wave')

def set_vertical(event):
    global polarization_mode
    polarization_mode = "vertical"
    ax.set_title('Vertically Polarized EM Wave')

def set_circular(event):
    global polarization_mode
    polarization_mode = "circular"
    ax.set_title('Circularly Polarized EM Wave')

def set_elliptical(event):
    global polarization_mode
    polarization_mode = "elliptical"
    ax.set_title('Elliptically Polarized EM Wave')

# Assign callbacks to buttons
button_horizontal.on_clicked(set_horizontal)
button_vertical.on_clicked(set_vertical)
button_circular.on_clicked(set_circular)
button_elliptical.on_clicked(set_elliptical)

# Create animation
ani = FuncAnimation(fig, update, init_func=init, frames=len(t_values), interval=50, blit=True)

plt.tight_layout()
plt.show()
