import numpy as np

NODE_LEN = 50

STR1 = 250
TURN1 = 334 # 1/2 * 2 * np.pi * TURN1_RADIUS_LEN
STR2 = 500
TURN2 = 147 # 1/2 * 2 * np.pi * TURN2_RADIUS_LEN
STR3 = 250
TRACK = [STR1, TURN1, STR2, TURN2, STR3]

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

print(nodes)