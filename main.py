import numpy as np
import matplotlib.pyplot as plt

# Track
NODE_LEN = 50
TURN1_RADIUS_LEN = 100
TURN2_RADIUS_LEN = 50

STR1 = 250
TURN1 = 334 # 1/2 * 2 * np.pi * TURN1_RADIUS_LEN
STR2 = 500
TURN2 = 147 # 1/2 * 2 * np.pi * TURN2_RADIUS_LEN
STR3 = 250
TRACK = [STR1, TURN1, STR2, TURN2, STR3]

def split_nodes(): # Separating nodes for calculation
    nodes = [0]
    track_len = 0
    for seg in TRACK:
        seg_len = 0
        
        while (seg_len < seg):
            seg_len += NODE_LEN
            if (seg_len >= seg):
                nodes.extend([track_len + seg] * 2)
            else:
                nodes.append(track_len + seg_len)
        track_len += seg
    nodes = nodes[:-1]

    dx = [0]
    for i in range(1, len(nodes)):
        dx.append(nodes[i] - nodes[i-1])

    return nodes, dx

nodes, dx_list = split_nodes()

turn_indices = []
for i in range(1, len(nodes)):
    if nodes[i] == nodes[i-1]:
        turn_indices.append(i)

for i in range(len(turn_indices)):
    if i % 2:
        turn_indices[i] -= 1

# Vehicle
G = 9.81
MAX_ACCEL = 2 * G

# Formulas
def apex_speed(r):
    assert isinstance(r, int), "radius must be an integer" 
    return np.sqrt(MAX_ACCEL * r)

def accelerate(v_i, dx):
    return np.sqrt(v_i ** 2 + 2 * MAX_ACCEL * dx)

turn1_speed = apex_speed(TURN1_RADIUS_LEN)
turn2_speed = apex_speed(TURN2_RADIUS_LEN)

# Velocity Lists
num_nodes = len(nodes)

def make_accel_list(v, turn_num):
    idx = (turn_num - 1) * 2
    span = turn_indices[idx + 1] - turn_indices[idx] + 1
    shift = turn_indices[idx]

    accel = []
    for i in range(num_nodes):
        if i > span:
            if (i + shift) < num_nodes:
                v = accelerate(v, dx_list[i + shift])
            else:
                v = accelerate(v, dx_list[i + shift - num_nodes])
        accel.append(float(v))
    accel = accel[num_nodes - shift:] + accel[:num_nodes - shift]
    return accel

def make_decel_list(v, turn_num):
    idx = (turn_num - 1) * 2
    span = turn_indices[idx + 1] - turn_indices[idx] + 1
    shift = turn_indices[idx + 1] + 1

    decel = []
    for i in range(num_nodes):
        if i > span:
            if (shift - i) < 0:
                v = accelerate(v, dx_list[shift - i + num_nodes])
            else:
                v = accelerate(v, dx_list[shift - i])
        decel.append(float(v))
    decel = decel[::-1]
    decel = decel[num_nodes - shift:] + decel[:num_nodes - shift]
    return decel

turn1_accel = make_accel_list(turn1_speed, 1)
turn2_accel = make_accel_list(turn2_speed, 2)
turn1_decel = make_decel_list(turn1_speed, 1)
turn2_decel = make_decel_list(turn2_speed, 2)

vel = []
for i in range(num_nodes):
    vel.append(min(turn1_accel[i], turn2_accel[i], turn1_decel[i], turn2_decel[i]))

time = 0
for i in range(num_nodes):
    time += dx_list[i] / vel[i]
print(time)

"""fig = plt.figure()
ax = plt.axes()
ax.plot(vel)
plt.show()"""