import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import math

# params
R = 100   # radius of pulley (made slightly smaller for visual clarity)
m1 = 15    # mass of right block
m2 = 3  # mass of left block
g = 9.81  # acc due to gravity

# --- Coordinate System ---
# Pulley center is at (0, 0)
# Positive y is UP

# time
t_max = 5
dt = 0.05
ts = np.arange(0, t_max, dt)

# initial conditions
y1_initial = -500.0
y2_initial = -400.0
v0 = 0  # initial velocity (system starts from rest)

# check if initial conditions are physically possible
# string length below pulley = -y1_initial + -y2_initial
# if one mass moves down by dy, the other moves up by dy
# so -y1(t) - y2(t) should be constant.
# verify: -y1_initial - y2_initial = -(-2.0) - (-2.0) = 4.0

# acceleration of the system
a_system = g * (m1 - m2) / (m1 + m2)

# Calculate acceleration for each mass in our coordinate system (positive y = up)
a1 = -a_system  # m1 accelerates downwards if m1 > m2
a2 = +a_system  # m2 accelerates upwards if m1 > m2

# motion (equation of motion)
y1s = y1_initial + v0*ts + 0.5*a1*ts**2  # position of mass 1 (right)
y2s = y2_initial + v0*ts + 0.5*a2*ts**2  # position of mass 2 (left)


# plot set up
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_title("Atwood machine animation")

# Determine plot limits dynamically
min_y = min(np.min(y1s), np.min(y2s))
max_y = R # highest point is the top of the pulley
ax.set_xlim(-R*3, R*3)
ax.set_ylim(min_y-R, max_y+R) # some padding

# elements
# pulley
pulley_circle = plt.Circle((0, 0), R, color='gray', fill=False, lw=2)
ax.add_patch(pulley_circle)
# pulley axle
ax.plot(0, 0, '+k', markersize=10)
# string over the pulley (arc)
theta = np.linspace(0, np.pi, 40) # Angle from +x axis (right) to -x axis (left)
pulley_string_x = R*np.cos(theta)
pulley_string_y = R*np.sin(theta)
ax.plot(pulley_string_x, pulley_string_y, 'k') # plot static arc


# dynamic elements
mass1, = ax.plot([], [], 's', markersize=15, color='blue', label=f'm1={m1}kg')  # m1 (right)
mass2, = ax.plot([], [], 's', markersize=15, color='red', label=f'm2={m2}kg')   # m2 (left)
string1, = ax.plot([], [], 'k') # string for m1 (right)
string2, = ax.plot([], [], 'k') # string for m2 (left)

ax.legend(loc='upper right')

# init func
def init():
    mass1.set_data([], [])
    mass2.set_data([], [])
    string1.set_data([], [])
    string2.set_data([], [])
    return mass1, mass2, string1, string2

# anim func
def animate(i):
    # current pos
    y1_t = y1s[i]
    y2_t = y2s[i]

    # Update mass pos (horizontal positions are fixed at +- R)
    mass1.set_data([R], [y1_t])
    mass2.set_data([-R], [y2_t])

    # Update string
    # string 1 (right side): from pulley edge (R, 0) to mass1 (R,y1_t)
    string1.set_data([R, R], [0, y1_t])
    # String 2 (left side): from pulley edge (-R, 0) to mass2 (-R,y2_t)
    string2.set_data([-R, -R], [0, y2_t])

    #return tuple
    return mass1, mass2, string1, string2

# Run animation
ani = FuncAnimation(fig, animate, frames=len(ts), init_func=init,
                    blit=True, interval=dt*1000, repeat=False)

plt.ylabel("y/x position")
plt.grid(True)
plt.show()