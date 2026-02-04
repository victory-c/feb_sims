import numpy as np

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
NUM_SEGS = 5

def split_nodes(seg_len): # Separating nodes for calculation
    nodes = np.array([0])
    nodes_len = 0
    while (nodes_len < seg_len):
        nodes_len += NODE_LEN
        if (nodes_len >= seg_len):
            nodes = np.append(nodes, seg_len)
        else:
            nodes = np.append(nodes, nodes_len)

    dx = [0]
    for i in range(1, len(nodes)):
        dx.append(int(nodes[i] - nodes[i-1]))

    return nodes, dx

nodes = []
dx = []
track_len = 0
for seg in TRACK:
    n, d = split_nodes(seg)
    nodes.append(n + track_len)
    dx.append(d)
    track_len += seg

# Vehicle
G = 9.81
MAX_ACCEL = 2 * G

# Apex Speeds
def apex_speed(r):
    assert isinstance(r, int), "radius must be an integer" 
    return np.sqrt(MAX_ACCEL * r)

turn1_speed = apex_speed(TURN1_RADIUS_LEN)
turn2_speed = apex_speed(TURN2_RADIUS_LEN)

# Velocities
str1_vel = np.zeros(len(nodes[0]))
turn1_vel = np.zeros(len(nodes[1]))
str2_vel = np.zeros(len(nodes[2]))
turn2_vel = np.zeros(len(nodes[3]))
str3_vel = np.zeros(len(nodes[4]))
vel = [str1_vel, turn1_vel, str2_vel, turn2_vel, str3_vel]

def set_apex_speed(vel_list, speed):
    for i in range(len(vel_list)):
        vel_list[i] = speed

set_apex_speed(turn1_vel, turn1_speed)
set_apex_speed(turn2_vel, turn2_speed)

print(vel)