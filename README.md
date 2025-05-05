# Polarization Simulation Project - Bixbi

An antenna radiation pattern is representation of the strength of the signal and to study the strength of emmitted signals from the antenna and the reciever for the better communications.

# dipole.py

The dipole antenna is the simplest & most widely used antenna. A dipole antenna has two metal rods with AC applied at the center, making electrons oscillate and emit electromagnetic waves. The radiation is strongest sideways (like a donut shape) and weakest along the wire. Its pattern in 2D looks like a figure-eight due to the formula **𝑈(𝜃)∝∣sin⁡(𝜃)**.

# Run dipole.py

1. python code_path/dipole.py

# 3D_dipole.py

A 3D radiation pattern shows how an antenna spreads energy in all directions — like a glowing shape around it. Unlike 2D plots, it covers both elevation (θ) and azimuth (ϕ) angles, helping visualize real-world coverage. For a dipole, the signal is strongest at θ = 90° (sideways) and zero along the axis (θ = 0° or 180°), following the formula 𝑟(𝜃,𝜙)=∣sin(𝜃)|.

# Run 3D_dipole

1. python code_path/3D_dipole.py

# beamforming.py

Beamforming uses multiple antennas to focus the signal in one direction instead of spreading it everywhere — like pointing a beam of wireless energy. By adjusting phase shifts between antennas, the signals add up in the desired direction and cancel out elsewhere, forming a strong, steerable beam. The beam direction depends on the phase shift
β, and it's strongest at 𝜃=90° when β=0.

# Run 3D_dipole

1. python code_path/beamforming.py
