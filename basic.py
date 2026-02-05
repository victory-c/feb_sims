import numpy as np
import matplotlib.pyplot as plt

# Vehicle
G = 9.81
MAX_ACCEL = 2 * G



# Formulas
def find_apex_speed(r): # Formula for apex speed
    assert isinstance(r, int), "radius must be an integer" 
    return np.sqrt(MAX_ACCEL * r)

def accelerate(v_i, dx): # Formula for acceleration
    return np.sqrt(v_i ** 2 + 2 * MAX_ACCEL * dx)



# Track
class Segment:
    length = 0
    radius = 0
    turn = False

    start_index = 0
    end_index = 0

    apex_speed = 0

    def __init__(self, l, r):
        assert isinstance(l, int), "first argument must be int"
        assert isinstance(r, int), "second argument must be int"
        self.length = l
        self.radius = r
        if self.radius != 0:
            self.turn = True
            self.apex_speed = find_apex_speed(self.radius)
    
    def set_start_index(self, i):
        self.start_index = i

    def set_end_index(self, i):
        self.end_index = i

    def len(self):
        return self.length
    
    def rad(self):
        return self.radius

    def is_turn(self):
        return self.turn
    
    def aps(self):
        return self.apex_speed
    
    def indices(self):
        return self.start_index, self.end_index

STR1 = Segment(250, 0)
TURN1 = Segment(334, 100) # 1/2 * 2 * np.pi * TURN1_RADIUS_LEN
STR2 = Segment(500, 0)
TURN2 = Segment(147, 50) # 1/2 * 2 * np.pi * TURN2_RADIUS_LEN
STR3 = Segment(250, 0)

TRACK = [STR1, TURN1, STR2, TURN2, STR3]

NODE_LEN = 1



# Helper Methods
def split_nodes(track): # Separating velocity tracking nodes
    nodes = [0]
    track_len = 0
    for seg in track:
        seg_len = 0
        
        while (seg_len < seg.len()):
            seg_len += NODE_LEN
            if (seg_len >= seg.len()):
                nodes.extend([track_len + seg.len()] * 2)
            else:
                nodes.append(track_len + seg_len)
        track_len += seg.len()
    nodes = nodes[:-1]

    dx = [0]
    for i in range(1, len(nodes)):
        dx.append(nodes[i] - nodes[i-1])

    return nodes, dx

def make_accel_list(seg): # Create list of accelerations from some apex point at every node
    span = seg.indices()[1] - seg.indices()[0]
    shift = seg.indices()[0]

    v = seg.aps()

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

def make_decel_list(seg): # Create list of decelerations from some apex point at every node
    span = seg.indices()[1] - seg.indices()[0]
    shift = seg.indices()[1] + 1

    v = seg.aps()

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



# Full code
nodes, dx_list = split_nodes(TRACK)
num_nodes = len(nodes)

track_turns = iter(TRACK) # Marking where each turn starts and ends
in_turn = False
for i in range(len(dx_list)): 
    if dx_list[i] == 0:
        if in_turn:
            seg.set_end_index(i-1)
            in_turn = False
        seg = next(track_turns)
        if seg.is_turn():
            in_turn = True
        if in_turn:
            seg.set_start_index(i)

vel_list = [] # Collecting apex speeds
for seg in TRACK:
    if seg.is_turn():
        vel_list.append(make_accel_list(seg))
        vel_list.append(make_decel_list(seg))
vel_list = np.array(vel_list)


vel = []
for i in range(num_nodes): # Finding min velocity values
    vel.append(min(vel_list[:, i]))

time = 0
for i in range(num_nodes):
    time += dx_list[i] / vel[i]
print(f"Laptime: {time:.3f} seconds")

fig = plt.figure()
ax = plt.axes()
ax.plot(vel)
plt.show()