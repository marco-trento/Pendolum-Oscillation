import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Get user input for pendulum parameters
print("=== Pendulum Simulation with Air Resistance ===")
print("Enter the following parameters:")

# Pendulum parameters
g = 9.81       # acceleration due to gravity (m/s^2)

# User inputs
L = float(input("Length of pendulum (m) [default: 1.0]: ") or "1.0")
theta0_deg = float(input("Initial angle (degrees) [default: 45]: ") or "45")
theta0 = np.radians(theta0_deg)
omega0 = float(input("Initial angular velocity (rad/s) [default: 0.0]: ") or "0.0")
c = float(input("Damping coefficient (kg/s) [default: 0.5]: ") or "0.5")
dt = float(input("Time step (s) [default: 0.02]: ") or "0.02")
t_max = float(input("Simulation duration (s) [default: 20]: ") or "20")

print(f"\nSimulation parameters:")
print(f"Length: {L} m")
print(f"Initial angle: {theta0_deg}°")
print(f"Initial angular velocity: {omega0} rad/s")
print(f"Damping coefficient: {c} kg/s")
print(f"Time step: {dt} s")
print(f"Duration: {t_max} s")
print("Starting simulation...\n")

# Time array
t = np.arange(0, t_max, dt)

# Arrays to hold theta and omega
theta = np.zeros_like(t)
omega = np.zeros_like(t)
theta[0] = theta0
omega[0] = omega0

# Numerical integration (Euler) with air resistance
for i in range(1, len(t)):
    # Damped pendulum equation: d²θ/dt² + (c/m) * dθ/dt + (g/L) * sin(θ) = 0
    # where c is the damping coefficient
    omega[i] = omega[i-1] - (g / L) * np.sin(theta[i-1]) * dt - (c / L) * omega[i-1] * dt
    theta[i] = theta[i-1] + omega[i] * dt

# Convert theta to (x, y) coordinates of the pendulum bob
x = L * np.sin(theta)
y = -L * np.cos(theta)

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-L - 0.2, L + 0.2)
ax.set_ylim(-L - 0.2, 0.2)
ax.set_aspect('equal')
ax.axis('off')  # Hide axes

# Pendulum line and bob
line, = ax.plot([], [], 'o-', lw=3, markersize=15)

# Initialization function
def init():
    line.set_data([], [])
    return line,

# Update function for animation
def update(frame):
    # Convert to numpy arrays to fix type issues
    x_data = np.array([0, x[frame]])
    y_data = np.array([0, y[frame]])
    line.set_data(x_data, y_data)
    return line,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(t),
                              init_func=init, blit=True, interval=dt*1000)

plt.title(f"Pendulum Oscillation with Air Resistance\nL={L}m, θ₀={theta0_deg}°, c={c}kg/s")
plt.show()
