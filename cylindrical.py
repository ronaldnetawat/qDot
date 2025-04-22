import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

#the params
R = 0.5                  # readius
k = 1                  # constant 
m = 1                
# omega_phi = 1          # 
omega_z = np.sqrt(k/m) # z-direction angular frequency

# angular momentum conservation
l = 1                  # Angular momentum (constant)
phi_dot = l / (m * R**2)  # Angular velocity due to conserved L

# time
t_max = 20
dt = 0.05
ts = np.arange(0, t_max, dt)

# Initial cond
A = 1
delta = 0            # Phase offset in z motion
phi_0 = 10            # Initial angle

# trajectory
z_vals = A * np.cos(omega_z * ts - delta)
phi_vals = phi_0 + phi_dot * ts

x_vals = R * np.cos(phi_vals)
y_vals = R * np.sin(phi_vals)

#figuring baby
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# # Draw the cylinder
# theta = np.linspace(0, 2*np.pi, 50)
# z_cylinder = np.linspace(-2, 2, 50)
# theta, z_cyl = np.meshgrid(theta, z_cylinder)
# x_cyl = R * np.cos(theta)
# y_cyl = R * np.sin(theta)

# draw the cylinder
theta = np.linspace(0, 2*np.pi, 50)
z_cylinder = np.linspace(-2, 2, 50)
theta_grid, z_grid = np.meshgrid(theta, z_cylinder)
x_cyl = R * np.cos(theta_grid)
y_cyl = R * np.sin(theta_grid)

ax.plot_wireframe(x_cyl, y_cyl, z_grid, color='gray', alpha=0.2)
ax.plot([0, 0], [0, 0], [-2, 2], color='black', lw=1)

# Particle marker
point, = ax.plot([], [], [], 'ro', markersize=6)

# Set limits and labels
ax.set_xlim([-R-1, R+1])
ax.set_ylim([-R-1, R+1])
ax.set_zlim([-2, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title("Particle confined to move on a cylinder")

# animation udpate
def update(i):
    point.set_data([x_vals[i]], [y_vals[i]])
    point.set_3d_properties([z_vals[i]])
    return point,

# Animate
ani = FuncAnimation(fig, update, frames=len(ts), interval=50, blit=False)
plt.show()
