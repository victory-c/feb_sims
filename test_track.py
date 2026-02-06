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



# Full code
nodes, dx_list = split_nodes(TRACK)
num_nodes = len(nodes)

# TODO: Optimize velocity flooring

vel_list = []
vel_list.append(accelerate_from_rest(dx_list))

for seg in TRACK:
    if seg.is_turn():
        vel_list.append(negotiate_turns(seg, dx_list))
vel_list = np.array(vel_list)

vels = []
for i in range(num_nodes): # Finding min velocity values
    vels.append(min(vel_list[:, i]))

lat_long = []
ll_list = iter(TRACK)
ll_seg = next(ll_list)
brake_index = 0
for i in range(len(vels)):
    if i > ll_seg.indices()[1]:
        ll_seg = next(ll_list)
    if i > 0 and vels[i] - vels[i-1] < 0:
        if brake_index == 0:
            brake_index = i
        ll_x = -1 * accel_x(vels[i], ll_seg.rad())
    else:
        ll_x = accel_x(vels[i], ll_seg.rad())
    lat_long.append([ll_x, accel_y(vels[i], ll_seg.rad())])
lat_long = np.array(lat_long)

time = 0
time_list = []
brake_time = 0
for i in range(len(vels)):
    if vels[i] != 0:
        time += dx_list[i] / vels[i]
    else:
        time += 0

    if i == brake_index:
        brake_time = time
    time_list.append(time)
brake_point = nodes[brake_index]


print(f"Laptime: {time:.3f} seconds")
print(f"Brake Time: {brake_time:.3f} seconds; Brake Point: {brake_point:.3f} meters")



# Graphs
fig, ax = plt.subplots(nrows = 2, ncols = 4)

ax[0][1].set(title="Velocity vs. Time",
             xlabel="Time (s)",
             ylabel="Velocity (m/s)")
ax[0][1].axvline(x=brake_time, color='r', linestyle='--')
ax[0][1].grid()
ax[0][1].plot(time_list, vels, '-k')

ax[0][0].set(title="Velocity vs. Distance",
             xlabel="Distance (m)",
             ylabel="Velocity (m/s)")
ax[0][0].axvline(x=brake_point, color='r', linestyle='--')
ax[0][0].grid()
ax[0][0].plot(nodes, vels, '-b')

ax[0][2].set(title="Velocity vs. Time (All lists)",
             xlabel="Time (s)",
             ylabel="Velocity (m/s)")
ax[0][2].grid()
ax[0][2].plot(time_list, vel_list[0], 'g', label="Accelerate from Rest")
ax[0][2].plot(time_list, vel_list[1], 'b', label="Negotiate Turn 1")
ax[0][2].plot(time_list, vels, 'k', ms=2.5, label = "Final Velocity")
ax[0][2].axvline(x=brake_time, color='r', linestyle='--')
ax[0][2].legend()

ax[0][3].set(title="Lateral and Longitudinal Acceleration",
             xlabel="Time (s)",
             ylabel="Acceleration (m/s^2)")
ax[0][3].grid()
ax[0][3].plot(time_list, lat_long[:, 0], 'b', label="Longitudinal Acceleration")
ax[0][3].plot(time_list, lat_long[:, 1], 'g', label="Lateral Acceleration")
ax[0][3].axvline(x=brake_time, color='r', linestyle='--')
ax[0][3].legend()

fig.tight_layout()
plt.show()