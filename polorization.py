import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Scale, HORIZONTAL, Frame

# Constants
apply_polarization = False  # Initial state - no polarization
polarization_angle = np.pi/4  # Default polarization angle (45 degrees)

# Create figure and 3D axis
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
ax.set_xlabel("Propagation Direction (z)")
ax.set_ylabel("Electric Field (Ex)")
ax.set_zlabel("Electric Field (Ey)")
ax.set_title("Light Wave Before and After Polarization (3D)")

# Initialize lines for electric field components
line_ex, = ax.plot([], [], [], label="Ex", color="blue", linewidth=2)
line_ey, = ax.plot([], [], [], label="Ey", color="red", linewidth=2)
line_combined, = ax.plot([], [], [], label="Combined", color="purple", linewidth=1)

# Add a polarizer plane
polarizer_x = np.linspace(-1.5, 1.5, 10)
polarizer_y = np.linspace(-1.5, 1.5, 10)
polarizer_X, polarizer_Y = np.meshgrid(polarizer_x, polarizer_y)
polarizer_Z = np.ones_like(polarizer_X) * np.pi  # Position the polarizer at π
polarizer = ax.plot_surface(polarizer_Z, polarizer_X, polarizer_Y, color='gray', alpha=0.3)

# Function to initialize the animation
def init():
    line_ex.set_data([], [])
    line_ex.set_3d_properties([])
    line_ey.set_data([], [])
    line_ey.set_3d_properties([])
    line_combined.set_data([], [])
    line_combined.set_3d_properties([])
    return line_ex, line_ey, line_combined

# Function to update the animation frame by frame
def update(frame):
    global apply_polarization, polarization_angle
    
    # Create a full wave from the start
    z = np.linspace(0, 2 * np.pi, 100)
    
    # Generate a circular/elliptical wave from the start
    ex = np.cos(z)
    ey = np.sin(z)
    
    # Apply polarization if the button has been clicked
    if apply_polarization:
        # Only apply polarization after the polarizer (z > π)
        mask = z > np.pi
        ex_after = ex.copy()
        ey_after = ey.copy()
        
        # Apply polarization effect
        ex_after[mask] = ex[mask] * np.cos(polarization_angle)
        ey_after[mask] = ey[mask] * np.sin(polarization_angle)
        
        # Update the lines
        line_ex.set_data(z, ex_after)
        line_ex.set_3d_properties(np.zeros_like(z))
        line_ey.set_data(z, np.zeros_like(z))
        line_ey.set_3d_properties(ey_after)
        line_combined.set_data(z, ex_after)
        line_combined.set_3d_properties(ey_after)
    else:
        # Without polarization, show the original wave
        line_ex.set_data(z, ex)
        line_ex.set_3d_properties(np.zeros_like(z))
        line_ey.set_data(z, np.zeros_like(z))
        line_ey.set_3d_properties(ey)
        line_combined.set_data(z, ex)
        line_combined.set_3d_properties(ey)
    
    # Rotate the view for better visualization
    ax.view_init(elev=20, azim=frame % 360)
    
    return line_ex, line_ey, line_combined

# Create animation
ani = FuncAnimation(fig, update, frames=360, init_func=init, interval=50, blit=False)

# Create Tkinter window
root = tk.Tk()
root.title("Polarization Animation")

# Create a canvas for the figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Function to toggle polarization
def toggle_polarization():
    global apply_polarization
    apply_polarization = not apply_polarization
    status_label.config(text=f"Polarization: {'ON' if apply_polarization else 'OFF'}")

# Function to update polarization angle
def update_angle(val):
    global polarization_angle
    polarization_angle = float(val) * np.pi / 180
    angle_label.config(text=f"Polarization Angle: {val}°")

# Create a frame for controls
control_frame = Frame(root)
control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Create a label to show polarization status
status_label = tk.Label(control_frame, text="Polarization: OFF")
status_label.pack(side=tk.TOP)

# Create a label for the angle
angle_label = tk.Label(control_frame, text="Polarization Angle: 45°")
angle_label.pack(side=tk.TOP)

# Create a slider for polarization angle
angle_slider = Scale(control_frame, from_=0, to=90, orient=HORIZONTAL, 
                     command=update_angle, length=200)
angle_slider.set(45)  # Default to 45 degrees
angle_slider.pack(side=tk.TOP)

# Button to apply/remove polarization
button = tk.Button(control_frame, text="Toggle Polarization", command=toggle_polarization)
button.pack(side=tk.BOTTOM, pady=10)

# Start the Tkinter main loop
root.mainloop()
