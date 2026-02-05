import numpy as np
import matplotlib.pyplot as plt
from FORMULAE import *
from TRACK import *
from VEHICLE import *
from SIMUL import *

# Track
STR1 = Segment(500, 0)
TURN1 = Segment(int(1/2 * 2 * np.pi * 50), 50)

TRACK = [STR1, TURN1]
TRACK_LEN = sum([len(track) for track in TRACK])
print(TRACK_LEN)



# Full code
nodes, dx_list = split_nodes(TRACK)
num_nodes = len(nodes)

# TODO: Optimize velocity flooring

vel_list = [] # Collecting apex speeds
for seg in TRACK:
    if seg.is_turn():
        vel_list.append(make_accel_list(seg, num_nodes, MAX_ACCEL, dx_list))
        vel_list.append(make_decel_list(seg, num_nodes, MAX_ACCEL, dx_list))
vel_list.append(straight_line_accel(MAX_ACCEL, num_nodes, dx_list))
vel_list = np.array(vel_list)

vels = []
for i in range(num_nodes): # Finding min velocity values
    vels.append(min(vel_list[:, i]))

time = 0
time_list = []
for i in range(num_nodes):
    if vels[i] != 0:
        time += dx_list[i] / vels[i]
    else:
        time += 0
    time_list.append(time)
print(f"Laptime: {time:.3f} seconds")



# Graphs
fig, ax = plt.subplots(ncols = 2)

ax[0].set(title="Velocity (m/s) vs. Time (s)",
       xlabel="Time (s)",
       ylabel="Velocity (m/s)")
ax[0].grid()
ax[0].plot(time_list, vels, 'o--b', ms=0.1)

ax[1].set(title="Velocity (m/s) vs. Time (s) (All values)",
       xlabel="Time (s)",
       ylabel="Velocity (m/s)")
ax[1].grid()
ax[1].plot(time_list, vel_list[0], 'g', label="Acceleration Velocity")
ax[1].plot(time_list, vel_list[1], 'r', label="Deceleration Velocity")
ax[1].plot(time_list, vel_list[2], 'b', label="Straight-Line Velocity")
ax[1].plot(time_list, vels, 'o-k', ms=2.5, label = "Final Velocity")
ax[1].legend()

plt.show()