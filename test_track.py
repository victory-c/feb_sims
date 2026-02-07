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

# Creating all velocity lists

vel_list = []
vel_list.append(accelerate_from_rest(dx_list))

for seg in TRACK:
    if seg.is_turn():
        vel_list.append(negotiate_turns(seg, dx_list))
vel_list = np.array(vel_list)

vels = []
for i in range(num_nodes): # Finding min velocity values
    vels.append(min(vel_list[:, i]))

# Iterating through final velocity list for graph values

lat_long = []
power_list = []
rpm_list = []
torque_list = []
drag_roll_list = []
brake_indices = []

seg_list = iter(TRACK)
seg_iter = next(seg_list)

braking = False
for i in range(len(vels)):
    v = vels[i]

    if i > seg_iter.indices()[1]:
        seg_iter = next(seg_list)
    if i > 0 and v - vels[i-1] < 0:
        if not braking:
            braking = True
            brake_indices.append(i)
        ll_x = -1 * accel_x(v, seg_iter.rad())
    else:
        braking = False
        ll_x = accel_x(v, seg_iter.rad())

    lat_long.append([ll_x, accel_y(v, seg_iter.rad())])
    power_list.append(power(v, seg_iter.rad()))

    r = rpm(v)
    rpm_list.append(r)
    torque_list.append(torque_interp(r))

    drag_roll_list.append([F_drag(v), F_roll(v)])
lat_long = np.array(lat_long)
drag_roll_list = np.array(drag_roll_list)

# Determining time

time = 0
time_list = []
brake_time = []
for i in range(len(vels)):
    if vels[i] != 0:
        time += dx_list[i] / vels[i]
    else:
        time += 0

    if i in brake_indices:
        brake_time.append(time)
    time_list.append(time)
brake_point = [nodes[i] for i in brake_indices]

avg_velocity = sum(vels) / len(vels) 
max_power = max(power_list)
avg_power = sum(power_list) / len(power_list)
tot_energy = energy(power_list, time_list)



# Numerical Outputs

print(f"\nLaptime: {time:.3f} seconds")
print(f"Average Velocity: {avg_velocity:.3f} meters per second\n")

print("Brake Times: ", end="")
if len(brake_time) == 1:
    print(f"{brake_time[0]:.3f} ", end="")
else:
    for t in brake_time:
        print(f"{t:.3f}, ", end="")
print("seconds")

print("Brake Points: ", end="")
if len(brake_point) == 1:
    print(f"{brake_point[0]:.3f} ", end="")
else:
    for p in brake_point:
        print(f"{p:.3f}, ", end="")
print("meters\n")

print(f"Total Energy Consumed: {tot_energy:.3f} kilowatt-hours")
print(f"Max Power Output: {max_power:.3f} kilowatts")
print(f"Average Power Output: {avg_power:.3f} kilowatts\n")



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

ax[1][0].set(title="Power Output",
             xlabel="Time (s)",
             ylabel="Power (Kw)")
ax[1][0].grid()
ax[1][0].plot(time_list, power_list, 'y')
ax[1][0].axvline(x=brake_time, color='r', linestyle='--')

ax[1][1].set(title="Rotations per Minute",
             xlabel="Time (s)",
             ylabel="RPM")
ax[1][1].grid()
ax[1][1].plot(time_list, rpm_list, color='pink')
ax[1][1].axvline(x=brake_time, color='r', linestyle='--')

ax[1][2].set(title="Torque",
             xlabel="Time (s)",
             ylabel="Torque (Newton-meters)")
ax[1][2].grid()
ax[1][2].plot(time_list, torque_list, color='purple')
ax[1][2].axvline(x=brake_time, color='r', linestyle='--')

ax[1][3].set(title="Drag and Rolling Resistance",
             xlabel="Time (s)",
             ylabel="Force (Newtons)")
ax[1][3].grid()
ax[1][3].plot(time_list, drag_roll_list[:, 0], 'b', label='Drag Force')
ax[1][3].plot(time_list, drag_roll_list[:, 1], 'g', label='Rolling Resistance')
ax[1][3].axvline(x=brake_time, color='r', linestyle='--')
ax[1][3].legend()

plt.show()